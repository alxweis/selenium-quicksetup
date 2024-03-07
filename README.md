# System Requirements

Ensure your system meets the following before proceeding:

- **Python 3.x**: Needed to run the script. Verify with `python --version`.
- **Java (JDK or JRE) 8+**: Critical for running the Selenium server. Check using `java -version`.
- **Available Port**: The port specified in `params.toml` (default is 4444) must be open and not in use.

# Setup Instructions

To prepare your environment for the Selenium server:

- **Download Selenium Server JAR**: Fetch the `selenium-server-<version>.jar` from [Selenium Releases](https://github.com/SeleniumHQ/selenium/releases) and save it in this directory.
- **Configure `params.toml`**: Populate `params.toml` with necessary parameters for your Selenium Server setup, as documented in [CLI Options](https://www.selenium.dev/documentation/grid/configuration/cli_options/#distributor).

# Starting the Selenium Server

Follow these steps to get the server running:

1. Run `start-selenium.bat` by double-clicking on it or through the command line.
2. Wait for the server to fully start up.
3. Access the server for testing at `http://localhost:<port>/wd/hub`.

# Stopping the Selenium Server

To stop the server, close the terminal window in which it's running. Alternatively, press `Ctrl+C` in the terminal and confirm the termination by typing `Y` when prompted with "Terminate batch job (Y/N)?", then press Enter.