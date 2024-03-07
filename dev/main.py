import toml
import os
import subprocess
import re

error = False

server = None
for file in os.listdir('.'):
    if re.match(r'selenium-server-\d{1,2}\.\d{1,2}\.\d{1,2}\.jar', file):
        server = file
        break

if server is None:
    print("No Selenium server as a .jar file was found in the directory.\nThe program will not start.")
    error = True

param_dict = toml.load('params.toml')
param_list = []
for key, value in param_dict.items():
    param_list.append("--" + key.lower())
    param_list.append(str(value).lower())
port = param_dict.get("port", 4444)

result = subprocess.run(["netstat", "-aon"], capture_output=True, text=True)
if f":{port}" in result.stdout:
    print(f"Port {port} is already in use.\nThe program will not start.")
    error = True

if error:
    while True:
        pass
else:        
    subprocess.run(["java", "-jar", server, "standalone"] + param_list)