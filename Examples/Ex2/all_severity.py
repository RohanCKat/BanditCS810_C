
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
