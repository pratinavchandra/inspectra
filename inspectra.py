import os
import shutil
import zipfile
import requests
import sys
import json
import re
import yara
import argparse

nacl_arch = "x86-64" #Change as needed

def get_latest_chrome_version():
    """Gets the latest chrome version"""
    url = 'https://chromiumdash.appspot.com/fetch_releases?channel=Stable&platform=Windows'
    response = requests.get(url)
    data = json.loads(response.text)
    
    if data and len(data) > 0:
        return data[0]['version']
    return None
    
def download_extension(extension_id, output_dir):
    """Downloads a Chrome extension CRX file."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    chrome_version = get_latest_chrome_version()
    crx_url = (
        "https://clients2.google.com/service/update2/crx?"
        "response=redirect&"
        f"prodversion={chrome_version}&"
        f"x=id%3D{extension_id}%26installsource%3Dondemand%26uc&"
        f"nacl_arch={nacl_arch}&"
        "acceptformat=crx2,crx3"
    )
    crx_path = os.path.join(output_dir, f"{extension_id}.crx")

    response = requests.get(crx_url, stream=True)
    if response.status_code == 200:
        with open(crx_path, 'wb') as crx_file:
            crx_file.write(response.content)
        return crx_path
    else:
        raise Exception(f"Failed to download CRX file: {response.status_code}")

def extract_crx(crx_path, extract_to):
    """Extracts a CRX file."""
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    with zipfile.ZipFile(crx_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def print_source_code(source_dir):
    """Prints only code files (HTML, CSS, JS, JSON, TXT) in the directory."""
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(('.js', '.json', '.html', '.css', '.txt')):  # Filter for JS, JSON, HTML, CSS, and TXT files
                file_path = os.path.join(root, file)
                with open(file_path, 'r', errors='ignore') as f:
                    print(f"\n--- {file_path} ---\n")
                    print(f.read())

def print_manifest_fields(manifest_path):
    """Prints specific fields from the manifest.json file."""
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r', errors='ignore') as f:
                manifest = json.load(f)
                
                # Print relevant fields from manifest.json
                print("\n--- manifest.json Fields ---")
                print(f"manifest_version: {manifest.get('manifest_version', 'N/A')}")
                print(f"permissions: {manifest.get('permissions', 'N/A')}")
                print(f"background: {manifest.get('background', 'N/A')}")
                print(f"content_scripts: {manifest.get('content_scripts', 'N/A')}")
                print(f"host_permissions: {manifest.get('host_permissions', 'N/A')}")
                print(f"declarative_net_request: {manifest.get('declarative_net_request', 'N/A')}")
        except json.JSONDecodeError:
            print("Error decoding manifest.json")
    else:
        print("manifest.json not found")

def extract_urls(text):
    """Extracts all valid URLs from the given text."""
    # Regex to match valid http(s) URLs with proper domains and optional paths or queries
    URL_PATTERN = re.compile(r'https?://[a-zA-Z0-9.-]+(?:/[^\s,]*)?')
    
    # Extract URLs
    urls = URL_PATTERN.findall(text)
    
    # Filter out incomplete URLs (e.g., 'http://n')
    valid_urls = [url for url in urls if len(url) > 7 and not url.endswith(('.', '/', ':'))]  # Minimum length and valid format
    return valid_urls

def print_urls_from_code(source_dir):
    """Prints all unique URLs found in the code files."""
    print("\n---- URLs found in code ----")
    seen_urls = set()  # Create a set to store unique URLs
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(('.js', '.json', '.html', '.css', '.txt')):  # Filter for relevant file formats
                file_path = os.path.join(root, file)
                with open(file_path, 'r', errors='ignore') as f:
                    content = f.read()
                    urls = extract_urls(content)
                    for url in urls:
                        # Exclude unwanted patterns such as wildcards or placeholders
                        if not re.search(r'https?://\*{2}/', url) and url not in ['http://', 'https://']:
                            # Normalize the URL (strip unwanted characters)
                            cleaned_url = url.split('"')[0].split(',')[0]
                            if cleaned_url not in seen_urls:
                                seen_urls.add(cleaned_url)
                                print(cleaned_url)

def run_yara_rules(source_dir, yara_rules_dir):
    """Runs YARA rules against the extension code."""
    print("\n---- YARA rule matches ----")
    
    # Compile YARA rules, considering both .yara and .yar extensions
    yara_rules = yara.compile(filepaths={rule_name: os.path.join(yara_rules_dir, rule_name) 
                                        for rule_name in os.listdir(yara_rules_dir) 
                                        if rule_name.endswith(('.yara', '.yar'))})
    
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(('.js', '.json', '.html', '.css', '.txt')):  # Filter for relevant file formats
                file_path = os.path.join(root, file)
                with open(file_path, 'r', errors='ignore') as f:
                    content = f.read()
                    matches = yara_rules.match(data=content.encode())
                    for match in matches:
                        print(f"Match found in {file_path}: {match.rule}")

def clean_up(paths):
    """Deletes specified files and directories."""
    for path in paths:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

def get_extension_name(source_dir):
    """Gets the name of the extension from its manifest.json."""
    manifest_path = os.path.join(source_dir, "manifest.json")
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r', errors='ignore') as f:
                manifest = json.load(f)
                return manifest.get('name', 'Unknown Extension')
        except json.JSONDecodeError:
            return 'Invalid manifest.json'
    return 'Manifest not found'

def main():
    parser = argparse.ArgumentParser(description="Download, extract, and analyze Chrome extensions.")
    parser.add_argument('extension_ids', nargs='+', help="List of Chrome extension IDs to process.")
    parser.add_argument('--code', action='store_true', help="Print source code if specified.")
    
    args = parser.parse_args()

    # Check if no flags are passed
    if not args.code and not args.scan:
        print("No analysis options provided. Please use --code to print source code or --scan to perform analysis.")
        return

    output_dir = "./chrome_extension"
    yara_rules_dir = "/app/yara_rules"  # Mounted folder for YARA rules

    for extension_id in args.extension_ids:
        print(f"\nProcessing extension ID: {extension_id}")
        try:
            # Download CRX
            crx_path = download_extension(extension_id, output_dir)

            # Extract CRX
            source_dir = os.path.join(output_dir, "source")
            extract_crx(crx_path, source_dir)

            # Get and print extension name
            extension_name = get_extension_name(source_dir)
            print(f"Extension Name: {extension_name}")

            # Print source code if --code is specified
            if args.code:
                print_source_code(source_dir)

            if args.scan:
                # Print manifest fields
                manifest_path = os.path.join(source_dir, "manifest.json")
                print_manifest_fields(manifest_path)

                # Print URLs found in the code
                print_urls_from_code(source_dir)

                # Run YARA rules
                run_yara_rules(source_dir, yara_rules_dir)

        finally:
            # Clean up files
            clean_up([output_dir])

if __name__ == "__main__":
    main()
