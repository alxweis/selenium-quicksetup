# System Requirements

Ensure your system meets the following before proceeding:

- **Python 3.x**: Needed to run the script. Verify with `python --version`.
- **Java (JDK or JRE) 8+**: Critical for running the Selenium server. Check using `java -version`.
- **Available Port**: The port specified in `params.toml` (default is 4444) must be open and not in use.

# Setup Guide

For setting up your Selenium server environment, follow these steps:

- **Selenium Server JAR**: Optionally, manually download a `selenium-server-<version>.jar` from [Selenium Releases](https://github.com/SeleniumHQ/selenium/releases) and place it in `./selenium-server`. If not found, the script auto-downloads the latest version.
- **Configure Parameters**: Fill in `params.toml` with required parameters for Selenium Server, as detailed in [CLI Options](https://www.selenium.dev/documentation/grid/configuration/cli_options/#distributor).

# Starting the Selenium Server

Follow these steps to get the server running:

## Windows
1. Run `start-selenium.bat` by double-clicking on it or through the command line.
2. Wait for the server to fully start up.
3. Access the server for testing at `http://localhost:<port>/wd/hub`.

## Linux or MacOS
1. Run `start-selenium.sh` by double-clicking on it or through the command line.
2. Wait for the server to fully start up.
3. Access the server for testing at `http://localhost:<port>/wd/hub`.

# Stopping the Selenium Server

To stop the server, close the terminal window in which it's running. Alternatively, you can stop it by pressing `Ctrl+C` within the terminal. For Windows users, you'll need to confirm termination by typing `Y` and hitting Enter when you see the prompt "Terminate batch job (Y/N)?".