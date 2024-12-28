# inspectra
Run yara rules on Chrome extension source code and/or extract URLs &amp; source code using Chrome extension IDs

### Installation
Clone the git repo - `git clone https://github.com/pratinavchandra/inspectra.git`
<br>
<br>
Build docker image - `docker build -t inspectra .`
<br>
<br>
Run analysis - `docker run -v /localpath/to/yara_rules:/app/yara_rules inspectra <extension ID>`
<br>
<br>
To Print source code to stdout used `--code`
<br>
`docker run -v /localpath/to/yara_rules:/app/yara_rules inspectra <extension ID> --code`

