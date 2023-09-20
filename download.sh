#!/bin/bash
wget -P ./MEaSUREs --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies --no-check-certificate --auth-no-challenge=on -r --reject "index.html*" -np -e robots=off -i ./MEaSUREs/files.txt
