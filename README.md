# Bandit Security Tutorial

1. [Introduction](#1-introduction)
2. [Installation](#2-installation)
3. [Usage](#3-usage)
    *  [3.1. Test Plugins](#31-test-plugins)
4. [Examples](#4-examples)
    * [4.1. Example One: Hardcoded Password](#41-example-one-hardcoded-password)
    * [4.2. Example Two: Severity Examples](#42-example-two-severity-examples)
    * [4.3. Example Three: my_app](#43-example-three-my_app)
    * [4.4. Example Four: Legacy Code Base](#44-example-four-legacy-code-base)
5. [Future use and Limitations](#5-future-use-and-limitations)

# 1. Introduction

Bandit is a static analyzer designed to find common security issues in Python code. To do this, Bandit processes each file, builds an Abstract Syntax Tree (AST) from the Python code, and runs plugs to detect vulnerabilities. Originally developed within the OpenStack Security Project to audit large cloud infrastructure codebases, it has since re homed to PyCQA and becae a cornerstone of the ecosystem. This tool is widely used in modern software development to automate the detection of vulnerabilities such as hardcoded passwords, insecure function calls, and weak cryptographic configurations. This tutorial covers the fundamentals of using Bandit, detailing installation and basic use cases.
# 2. Installation
Note: If using older version of python, you may need to use ```pip``` or `python`.

Installing bandit is easy using Python Package Index. You can use PIP to install it globally or to a specific environment
```bash
pip install bandit
```
It is highly recommended to use a ```venv``` to create a custom environment to prevent package conflicts. 
### Linux 
```bash
python3 -m venv bandit_env
source bandit_env/bin/activate
```
### Windows 
```powershell
python3 -m venv bandit_env
bandit_env/bin/activate
```
To deactivate the environment, run `deactivate` in the environment
```bash
deactivate
```
Once the virtual environment is active, you can install the tool directly from the PIP command
```bash
pip install bandit
```
# 3. Usage

Using Bandit involves pointing it at a specific file or an entire directory of source code. The tool provides a detailed report of every potential vulnerability it discovers, categorized by severity and confidence levels. You can access the comprehensive manual and a full list of available commands by using the help flag.

To call bandit to a file, use 
```bash
bandit path/to/your/code
```

## Common Command-Line Flags
| Flag | Name | Description |
| :--- | :--- | :--- |
| `-r` | `--recursive` | Scans the specified directory and all subdirectories|
| `-f` | `--format` | Specifies the output format such as JSON or YAML|
| `-o` | `--output` | Writes the security report to a specified file. |
| `-t` | `--tests` | Runs only the specific test IDs provided in a list. |
| `-s` | `--skip` | Skips specific test IDs during the scan. |
| `-l` | `--level` | Filters findings by a specific severity level. |
| `-n` | `--number` | Limits the number of code lines displayed for each issue. |
| `N/A` | `--baseline` | Ignores existing issues using a path to a previous report. |
| `-h` | `--help` | Displays the manual and all available commands |

The recursive flag is a required command for checking entire Python projects.
```bash
bandit -r path/to/your/code
```
Integrating bandit scans with other tools is done by combining the format and output flags to generate file types that other programs can iterate through. 
```bash
# Example of a recursive scan with JSON output
bandit -r path/to/your/code -f json -o security_report.json
```
If you need to isolate a specific class of vulnerability, the tests flag allows for targeted analysis of certain test IDs. 
```bash
# Run only the test for hardcoded passwords (B105) on the current directory
bandit -t B105 .

# Run multiple specific tests (B101 and B608) on a specific file
bandit -t B101,B608 app.py
```
`--baseline` allows for developers to filter old bugs
```bash
bandit -r . -f json -o initial_baseline.json
bandit -r . --baseline initial_baseline.json
``` 

## 3.1. Test Plugins

Custom test plugins allow you to extend Bandit to catch errors with external libraries or code snippets. A plugin is essentially a function that looks for a pattern within the AST.

```python
import bandit
from bandit.core import test_properties as test

@test.checks('Call')
@test.test_id('B999')
def custom_security_check(context):
    if context.call_function_name_qual == 'my_lib.unsafe_call':
        return bandit.Issue(
            severity=bandit.HIGH,
            confidence=bandit.HIGH,
            text="Detected a call to a forbidden internal function."
        )
```

To install custom plugins, you can navigate to the internal directory of your installed package. You must locate the site-packages directory within your virtual environment and move your plugin script into bandit's plugins folder.

```bash
cp my_custom_plugin.py bandit_env/lib/python3.x/site-packages/bandit/plugins/
```

# 4. Examples

## 4.1. Example One: Hardcoded Password
The provided script contains a hardcoded password and uses the input function, both of which are flagged by security scanners as potential risks in various deployment contexts.
```python
dbms_pass = "123"
get_cred = input()
if (dbms_pass == get_cred.trim()):
    print("Logged In!")
else:
	print ("Incorrect Password.")
```
To run bandit, use the following command
```bash
bandit Examples/Ex1/pass.py
```
Example Output:
```bash
Test results:
>> Issue: [B105:hardcoded_password_string] Possible hardcoded password: '123'
   Severity: Low   Confidence: Medium
   CWE: CWE-259 (https://cwe.mitre.org/data/definitions/259.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b105_hardcoded_password_string.html
   Location: .\Examples/Ex1/pass.py:1:12
1       dbms_pass = "123"
2       get_cred = input()
3       if (dbms_pass == get_cred.trim()):

--------------------------------------------------

Code scanned:
        Total lines of code: 6
        Total lines skipped (#nosec): 0

Run metrics:
        Total issues (by severity):
                Undefined: 0
                Low: 1
                Medium: 0
                High: 0
        Total issues (by confidence):
                Undefined: 0
                Low: 0
                Medium: 1
                High: 0
Files skipped (0):
```
## 4.2. Example Two: Severity Examples
The provided script has all the different types of severity
```python
# LOW Severity (B404: blacklist)
import os
import random
import subprocess

# LOW Severity (B311: blacklist)
def generate_rand_token():
    return random.random()

# MEDIUM Severity (B108: hardcoded_tmp_directory)
def write_temp_config(data):
    with open("/tmp/config.txt", "w") as f:
        f.write(data)

# HIGH Severity (B602: subprocess_popen_with_shell_equals_true)
def ping(ip):
    subprocess.call(f"ping -c 1 {ip}", shell=True)
ping("8.8.8.8")
```
To run bandit, use the following command
```bash
bandit Examples/Ex2/all_severity.py
```
Example Output:
```bash
Test results:
>> Issue: [B404:blacklist] Consider possible security implications associated with the subprocess module.
   Severity: Low   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_imports.html#b404-import-subprocess
   Location: .\Examples/Ex2/all_severity.py:5:0
4       import random
5       import subprocess
6

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: .\Examples/Ex2/all_severity.py:9:11
8       def generate_rand_token():
9           return random.random()
10

--------------------------------------------------
>> Issue: [B108:hardcoded_tmp_directory] Probable insecure usage of temp file/directory.
   Severity: Medium   Confidence: Medium
   CWE: CWE-377 (https://cwe.mitre.org/data/definitions/377.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b108_hardcoded_tmp_directory.html
   Location: .\Examples/Ex2/all_severity.py:13:14
12      def write_temp_config(data):
13          with open("/tmp/config.txt", "w") as f:
14              f.write(data)

--------------------------------------------------
>> Issue: [B602:subprocess_popen_with_shell_equals_true] subprocess call with shell=True identified, security issue.
   Severity: High   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b602_subprocess_popen_with_shell_equals_true.html
   Location: .\Examples/Ex2/all_severity.py:18:4
17      def ping(ip):
18          subprocess.call(f"ping -c 1 {ip}", shell=True)
19

--------------------------------------------------

Code scanned:
        Total lines of code: 11
        Total lines skipped (#nosec): 0

Run metrics:
        Total issues (by severity):
                Undefined: 0
                Low: 2
                Medium: 1
                High: 1
        Total issues (by confidence):
                Undefined: 0
                Low: 0
                Medium: 1
                High: 3
Files skipped (0):
```
Blacklists are usually low severity, indicating a possible vulnerability but not necessarily becoming one.
 
The medium severity issue is from temp files, potentially allowing an attacker to modify the temp file generated to find out sensitive information or attack another part of the program

The high severity issue is `shell=True` in a subprocess, allowing an attacker direct access to the shell.
## 4.3. Example Three: my_app
Bandit has the capabilities to scan an entire folder at once, and everything in it using the -r flag.
Scan the entire my_app directory in examples using
```
bandit -r Examples/Ex3/my_app
```
Example output:
```bash
Test results:
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Low
   CWE: CWE-89 (https://cwe.mitre.org/data/definitions/89.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b608_hardcoded_sql_expressions.html
   Location: Examples/Ex3/my_app\DB\connector.py:5:14
4       def get_user(username):
5           query = f"SELECT * FROM users WHERE name = '{username}'"
6           return query

--------------------------------------------------
>> Issue: [B324:hashlib] Use of weak MD5 hash for security. Consider usedforsecurity=False
   Severity: High   Confidence: High
   CWE: CWE-327 (https://cwe.mitre.org/data/definitions/327.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b324_hashlib.html
   Location: Examples/Ex3/my_app\auth.py:5:11
4       def insecure_hash_password(password):
5           return hashlib.md5(password.encode()).hexdigest()

--------------------------------------------------
>> Issue: [B105:hardcoded_password_string] Possible hardcoded password: 'pass123'
   Severity: Low   Confidence: Medium
   CWE: CWE-259 (https://cwe.mitre.org/data/definitions/259.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b105_hardcoded_password_string.html
   Location: Examples/Ex3/my_app\config.py:3:14
2       API_KEY = "sk-1234567890abcdef1234567890"
3       DB_PASSWORD = "pass123"

--------------------------------------------------
>> Issue: [B113:request_without_timeout] Call to requests without timeout
   Severity: Medium   Confidence: Low
   CWE: CWE-400 (https://cwe.mitre.org/data/definitions/400.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b113_request_without_timeout.html
   Location: Examples/Ex3/my_app\utils.py:5:11
4       def get_api_data(url):
5           return requests.get(url)

--------------------------------------------------

Code scanned:
        Total lines of code: 12
        Total lines skipped (#nosec): 0

Run metrics:
        Total issues (by severity):
                Undefined: 0
                Low: 1
                Medium: 2
                High: 1
        Total issues (by confidence):
                Undefined: 0
                Low: 2
                Medium: 1
                High: 1
Files skipped (0):
```
Some Notable vulnerabilities include
* Possible SQL injection
  * SQL injection is possible by taking user input and creating a SQL prompt from it  
* Weak MD5 Hash
  * MD5 is a weak hash for cryptography, being able to be cracked with relative ease. As such, it allows attackers access to the content inside.
## 4.4. Example Four: Legacy Code base
Bandits a useful tool when parsing long files. The file `legacy.py` contains a fake legacy code that has a multitude of vulnerabilities
To run bandit, use the following command
```bash
bandit Examples/Ex4/legacy.py
```
However, we will see that the example output is massive! Additionally, we can see that a lot of vulnerabilities are low severity and low confidence
Example output:
```bash
Test Results:
...
Code scanned:
        Total lines of code: 60
        Total lines skipped (#nosec): 0

Run metrics:
        Total issues (by severity):
                Undefined: 0
                Low: 9
                Medium: 6
                High: 2
        Total issues (by confidence):
                Undefined: 0
                Low: 2
                Medium: 2
                High: 13
Files skipped (0):
```
Ideally, we only see the high severity, and address those problems first. this can be done from using the `-l` flag
```bash
bandit -lll Examples/Ex4/legacy.py
```
Example Output:
```bash
Test results:
>> Issue: [B324:hashlib] Use of weak SHA1 hash for security. Consider usedforsecurity=False
   Severity: High   Confidence: High
   CWE: CWE-327 (https://cwe.mitre.org/data/definitions/327.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b324_hashlib.html
   Location: .\Examples/Ex4/legacy.py:23:11
22
23          return hashlib.sha1(content.encode()).hexdigest()
24

--------------------------------------------------
>> Issue: [B501:request_with_no_cert_validation] Call to requests with verify=False disabling SSL certificate checks, security issue.
   Severity: High   Confidence: High
   CWE: CWE-295 (https://cwe.mitre.org/data/definitions/295.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b501_request_with_no_cert_validation.html
   Location: .\Examples/Ex4/legacy.py:61:11
60      def load_environment_config(config_url):
61          resp = requests.get(config_url, verify=False)
62

--------------------------------------------------

Code scanned:
        Total lines of code: 60
        Total lines skipped (#nosec): 0

Run metrics:
        Total issues (by severity):
                Undefined: 0
                Low: 9
                Medium: 6
                High: 2
        Total issues (by confidence):
                Undefined: 0
                Low: 2
                Medium: 2
                High: 13
Files skipped (0):
```
A new vulnerability is the `verify=false` flag in requests, disabling security verification when doing a request
# 5. Future use and Limitations

## 5.1. Future use
The future of Bandit is bright. Static Analyzers have been pushed deeper into the DevSecOps lifecycle. Industry practices are evolving to a "shifting left" methodology, inheriting automated security scanning as a prerequisite to pusing code, instead of a final check at the end of development. This trend is supported by tools like Bandit, allowing easy and quick security scanning to be performed without interrupting workflow. Furthermore, the emergence of Large Language Models is changing how static analysis reports are processed. Modern research indicates that AI-powered agents are being used to sift through the noise of static analysis to identify and filter out false positives, which significantly reduces alert fatigue for development teams. In some experimental frameworks, Bandit is already being utilized as a feedback mechanism for self-healing code, where it checks AI-generated scripts and provides the prompts for the AI to patch its own security flaws. Additionally, institutional standards from organizations such as NIST are codifying the requirement for pre-runtime vulnerability identification, ensuring that tools like Bandit remain a regulatory necessity for cloud-native applications.

## 5.2. Limitations

As a static analyzer, this tool has inherent limitations. It can only analyze the code as it exists on the disk and cannot account for the state of the program during execution. This means it might flag code that is safe in its specific runtime context or miss runtime vulnerabilities. Furthermore, static analysis is prone to false positives, requiring a human developer to review findings and determine if a reported issue is a genuine threat or a safe edge case, which can result in alert fatigue. Furthermore, bandit isn't all inclusive in the errors it catches, furthering the necessity of a suite of tools to check code with.
