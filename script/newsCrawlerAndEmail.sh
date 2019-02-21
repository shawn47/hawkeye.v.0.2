#!/bin/bash
PYTHONPATH=/usr/local/lib/python3.7/site-packages 
/usr/local/Cellar/python3/3.7.2/bin/python3 /Users/xiaoyongbo/Documents/projects/hawkeye.v.0.2/Main.py emailNotification > /Users/xiaoyongbo/Documents/projects/hawkeye.v.0.2/logs/app.log 2>&1 & 
