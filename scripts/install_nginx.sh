#!/bin/bash

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

LOG_FILE="$PROJECT_ROOT/logs/provisioning.log"
SERVICE="nginx"

set -e

echo "Checking if $SERVICE is installed.."
if ! command -v nginx >/dev/null 2>&1; then
    echo "$SERVICE not found. installing.." >> $LOG_FILE
    sudo apt update
    sudo apt install -y nginx
    echo "$SERVICE installed successfully!" >> $LOG_FILE
else
    echo "$SERVICE already installed! Skipping installation" >> $LOG_FILE
fi

