import subprocess
import os
import sys
import re
from enum import Enum
from datetime import datetime

server_directory = "./server"
config_file = "config.toml"

class PrintType(Enum):
    INFO = 'INFO'
    WARN = 'WARN'
    ERROR = 'ERROR'

def tprint(*args, t=PrintType.INFO, **kwargs):
    print(datetime.now().strftime("%H:%M:%S.%f")[:-3], t.value, "-", *args, **kwargs)

def ensure_module_installed(module_name, package=None):
    """Ensure a Python module is installed, installing it if necessary."""
    try:
        return __import__(module_name)
    except ImportError:
        package = package or module_name
        tprint(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return __import__(module_name)

# Ensure necessary modules are installed and import them
toml = ensure_module_installed('toml')
requests = ensure_module_installed('requests')
BeautifulSoup = ensure_module_installed('bs4', 'beautifulsoup4').BeautifulSoup

def is_java_installed():
    """Check if Java is installed and in the PATH."""
    try:
        subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT)
        return True
    except FileNotFoundError:
        return False

def get_latest_version():
    response = requests.get("https://github.com/SeleniumHQ/selenium/releases/latest")
    return response.url.split('/')[-1].replace('selenium-', '')

def get_version_from_file(file):
    version_match = re.search(r"\d+\.\d+\.\d+", file)
    return version_match.group(0) if version_match else None

def is_version_smaller(v1, v2):
    v1_parts = [int(part) for part in v1.split('.')]
    v2_parts = [int(part) for part in v2.split('.')]
    
    length_difference = len(v1_parts) - len(v2_parts)
    if length_difference > 0:
        v2_parts += [0] * length_difference
    elif length_difference < 0:
        v1_parts += [0] * (-length_difference)
    
    for i in range(len(v1_parts)):
        if v1_parts[i] < v2_parts[i]:
            return True
        elif v1_parts[i] > v2_parts[i]:
            return False
    
    return False

def get_max_version_file(files):
    max_file = None
    max_version = None
    for file, version in files.items():
        if max_version is None or is_version_smaller(max_version, version):
            max_version = version
            max_file = file
    return max_file

def find_or_download_selenium_server():
    """Find or download the latest Selenium server jar file."""
    latest_version = get_latest_version()

    files = {}
    for f in os.listdir(server_directory):
        if f.endswith(".jar"):
            files[f] = get_version_from_file(f)

    if len(files) > 0 and os.path.exists(server_directory):
        file = get_max_version_file(files)
        version = get_version_from_file(file)
        if is_version_smaller(version, latest_version):
            tprint(f"Your current Selenium version is {version}, however, latest version {latest_version} is now available", t=PrintType.WARN)
        return file
    return download_selenium_server()

def download_selenium_server():
    latest_version = get_latest_version()
    if os.path.exists(server_directory):
        for file in os.listdir(server_directory):
            if file.endswith(".jar"):
                version = get_version_from_file(file)
                if version == latest_version:
                     tprint(f"Your current Selenium version is already the latest {version}", t=PrintType.INFO)
                     return
    tprint("Downloading latest Selenium server. Please wait, it may take a few minutes...")
    file_name = f"selenium-server-{latest_version}.jar"
    download_url = f"https://github.com/SeleniumHQ/selenium/releases/download/selenium-{latest_version}/{file_name}"
    os.makedirs(server_directory, exist_ok=True)
    local_file_path = os.path.join(server_directory, file_name)
    response = requests.get(download_url)
    if response.status_code == 200:
        tprint("Successfully downloaded", file_name)
        with open(local_file_path, 'wb') as file:
            file.write(response.content)
        return file_name
    else:
        sys.exit("Failed to download the latest Selenium server.")

def load_configuration():
    """Load configuration, exiting if not found or invalid."""
    try:
        return toml.load(f'{config_file}')
    except FileNotFoundError:
        sys.exit(f"{config_file} not found")
    except toml.TomlDecodeError:
        sys.exit(f"Error parsing {config_file}")

def is_port_in_use(port):
    """Check if the specified port is already in use."""
    result = subprocess.run(["netstat", "-aon"], capture_output=True, text=True)
    return f":{port}" in result.stdout

def main():
    # Precheck
    if not is_java_installed():
        sys.exit("Java is not installed or not in PATH. Please install Java and ensure it is in PATH")

    # Check configuration
    config = load_configuration()
    port = config.get("port", 4444)
    if is_port_in_use(port):
        sys.exit(f"Port {port} is already in use")

    # Start server
    server_file = find_or_download_selenium_server()
    params = ["java", "-jar", f"{server_directory}/{server_file}", "standalone", "--config", f"./{config_file}"]
    tprint(f"Starting Selenium server... ({' '.join(params)})")
    subprocess.run(params)

if __name__ == "__main__":
    main()
