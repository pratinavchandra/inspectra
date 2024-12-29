# Inspectra

Inspectra is a powerful tool for analyzing Chrome extensions with minimal setup. It enables you to:

- Run YARA rules on Chrome extension source code.
- Extract URLs and source code using Chrome extension IDs.

---

## 🚀 Features
- **Customizable YARA Rules**: Add your own YARA rules for tailored analysis.
- **Raw Source Code**: Extract and print extension source code to stdout for quick analysis.

---

## 📥 Installation

Follow these steps to set up Inspectra:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/pratinavchandra/inspectra.git
   ```

2. **Navigate to the Directory**:
   ```bash
   cd inspectra
   ```

3. **Build the Docker Image**:
   ```bash
   docker build -t inspectra .
   ```

4. **Add YARA Rules**:
   - Place your YARA rules in the `yara_rules` folder within the `inspectra` directory.
   - Alternatively, mount a local directory containing YARA rules.

---

## 🛠️ Usage
```
   inspectra.py [-h] [--code] [--scan] extension_ids [extension_ids ...]

   arguments:
      extension_ids  List of Chrome extension IDs to process.
      --code         Print source code if specified.
      --scan         Run yara rules and perform analysis on the extension if specified.
   ```
### Analyze Chrome Extensions
Run the following command to analyze a Chrome extension by its ID:
```bash
docker run -v ~/inspectra/yara_rules:/app/yara_rules inspectra <extension ID> --scan
```

<img width="887" alt="image" src="https://github.com/user-attachments/assets/8aae0d04-2477-4150-8225-2618b356a6a3" />


### Get Raw Source Code to Stdout
To display the source code of the extension, use the `--code` flag:
```bash
docker run -v /localpath/to/yara_rules:/app/yara_rules inspectra <extension ID> --code
```

<img width="887" alt="image" src="https://github.com/user-attachments/assets/d601c473-8172-4c64-b3d0-476116c68263" />


---

## 🤝 Contributing
Contributions are welcome! Feel free to submit issues or pull requests to improve Inspectra.
Building a library of yara rules tailored to Chrome extensions would be awesome!

---

Happy Inspecting! 🔍
