#!/bin/bash

# This script installs nginx on the system
# It checks if nginx is already installed
# If not installed it installs it
# All logs are written into logs/provisioning.log


PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_FILE="$PROJECT_ROOT/logs/provisioning.log"
SERVICE="nginx"

set -e

echo "Checking if $SERVICE is installed.." >> $LOG_FILE

# If nginx exists skip installation
if command -v nginx >/dev/null 2>&1; then
    echo "$SERVICE already installed! Skipping installation" >> $LOG_FILE
    exit 0
    fi

# If nginx does NOT exist install it.
echo "$SERVICE not found. installing.." >> $LOG_FILE
    sudo apt update
    sudo apt install -y nginx
    echo "$SERVICE installed successfully!" >> $LOG_FILE


