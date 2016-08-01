#! /bin/sh
_now=$(date +"%Y-%m-%d")
python3 nhk-today.py
kindlegen "$_now.opf"
