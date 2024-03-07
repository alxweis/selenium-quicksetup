## Setup
### Download Selenium server
1. Download `selenium-server-<VERSION>.jar` from the Assets section at [Selenium Releases](https://github.com/SeleniumHQ/selenium/releases).
2. Place `selenium-server-<VERSION>.jar` in this directory.

### Use custom parameters
Simply add parameters to `params.toml` to start the Selenium Server with your desired configuration. You can find possible parameters you can use here: [CLI Options](https://www.selenium.dev/documentation/grid/configuration/cli_options/#distributor).

## Start Selenium server
1. Execute `start-selenium.bat` (e.g., by double-clicking it).
2. Wait until the Selenium server has started.
3. Now you can use `http://localhost:<PORT>/wd/hub` for testing.

## Stop Selenium server
Manually close the open terminal. Alternatively, press Ctrl+C and respond "Yes" to the prompt "Terminate batch job (Y/N)?" by typing Y and hitting Enter.