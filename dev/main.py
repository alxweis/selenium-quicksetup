import subprocess
import os
import sys

def ensure_module_installed(module_name, package=None):
    """Ensure a Python module is installed, installing it if necessary."""
    try:
        return __import__(module_name)
    except ImportError:
        package = package or module_name
        print(f"Installing {package}...")
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

def find_or_download_selenium_server(target_directory="./selenium-server"):
    """Find or download the latest Selenium server jar file."""
    if os.path.exists(target_directory):
        for file in os.listdir(target_directory):
            if file.endswith(".jar"):
                return os.path.join(target_directory, file)

    print("Downloading latest Selenium server. Please wait, it may take a few minutes...")
    response = requests.get("https://github.com/SeleniumHQ/selenium/releases/latest")
    latest_version = response.url.split('/')[-1].replace('selenium-', '')
    download_url = f"https://github.com/SeleniumHQ/selenium/releases/download/selenium-{latest_version}/selenium-server-{latest_version}.jar"
    os.makedirs(target_directory, exist_ok=True)
    file_name = f"selenium-server-{latest_version}.jar"
    local_file_path = os.path.join(target_directory, file_name)
    response = requests.get(download_url)
    if response.status_code == 200:
        with open(local_file_path, 'wb') as file:
            file.write(response.content)
        print("Successfully downloaded", file_name)
        return local_file_path
    else:
        sys.exit("Failed to download the latest Selenium server.")

def load_configuration():
    """Load configuration from 'config.toml', exiting if not found or invalid."""
    try:
        return toml.load('config.toml')
    except FileNotFoundError:
        sys.exit("config.toml not found.")
    except toml.TomlDecodeError:
        sys.exit("Error parsing config.toml.")

def is_port_in_use(port):
    """Check if the specified port is already in use."""
    result = subprocess.run(["netstat", "-aon"], capture_output=True, text=True)
    return f":{port}" in result.stdout

def main():
    if not is_java_installed():
        sys.exit("Java is not installed or not in PATH. Please install Java and ensure it is in PATH.")

    server_path = find_or_download_selenium_server()
    config = load_configuration()

    port = config.get("port", 4444)
    if is_port_in_use(port):
        sys.exit(f"Port {port} is already in use.")

    print("Starting Selenium server...")
    params = ["java", "-jar", server_path, "standalone"] + [param for item in config.items() for param in ("--" + item[0].lower(), str(item[1]).lower())]
    subprocess.run(params)

if __name__ == "__main__":
    main()
