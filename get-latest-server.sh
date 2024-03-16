#!/bin/bash

call python -c "from dev.main import download_selenium_server; download_selenium_server()"
read -p "Press any key..."