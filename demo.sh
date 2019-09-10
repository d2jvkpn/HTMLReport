#! /bin/bash
set -eu

python3 report_process.py -i template.html  -ini project.ini -o report.html
