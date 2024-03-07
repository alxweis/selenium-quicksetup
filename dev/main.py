import subprocess
import os
import re
import sys

# Attempt to import the toml module, installing it if necessary
try:
    import toml
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "toml"])
    import toml  # Ensure toml is imported after installation

def check_java_installed():
    try:
        subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT)
    except FileNotFoundError:
        print("Java is not installed or not in PATH. Please install Java and ensure it is in the PATH.")
        sys.exit(1)

def find_selenium_server_jar():
    for file in os.listdir('.'):
        if re.match(r'selenium-server-\d+\.\d+\.\d+\.jar', file):
            return file
    print("No Selenium server JAR file found in the directory.")
    sys.exit(1)

def load_params():
    try:
        return toml.load('params.toml')
    except FileNotFoundError:
        print("params.toml not found.")
        sys.exit(1)
    except toml.TomlDecodeError:
        print("Error parsing params.toml.")
        sys.exit(1)

def check_port_in_use(port):
    result = subprocess.run(["netstat", "-aon"], capture_output=True, text=True)
    if f":{port}" in result.stdout:
        print(f"Port {port} is already in use.")
        sys.exit(1)

def main():
    check_java_installed()

    server = find_selenium_server_jar()
    param_dict = load_params()
    param_list = []
    for key, value in param_dict.items():
        param_list.append("--" + key.lower())
        param_list.append(str(value).lower())
    check_port_in_use(param_dict.get("port", 4444))

    subprocess.run(["java", "-jar", server, "standalone"] + param_list)

if __name__ == "__main__":
    main()
