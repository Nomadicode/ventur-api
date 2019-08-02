#!/usr/bin/env bash

git pull

pip install -r requirements.txt

sudo systemctl stop nginx
sudo systemctl stop uwsgi

sudo systemctl start uwsgi
sudo systemctl start nginx