# inspectra
Run yara rules on Chrome extension source code and/or extract URLs &amp; source code using Chrome extension IDs

### Installation
Clone the git repo - `git clone https://github.com/pratinavchandra/inspectra.git`
<br>
<br>
Navigate to cloned directory - `cd inspectra`
<br>
<br>
Build docker image - `docker build -t inspectra .`
<br>
<br>
Run analysis - `docker run -v ~/inspectra/yara_rules:/app/yara_rules inspectra <extension ID>`
<br>
<br>
<img width="909" alt="image" src="https://github.com/user-attachments/assets/9ce3e7a3-4587-44bc-9bd5-9536dfc1748f" />
<br>
<br>
To Print source code to stdout use `--code`
<br>
`docker run -v /localpath/to/yara_rules:/app/yara_rules inspectra <extension ID> --code`
<br>
<br>
<img width="1031" alt="image" src="https://github.com/user-attachments/assets/abeba0b9-f0ce-4548-99eb-b523b6e5c8ef" />

