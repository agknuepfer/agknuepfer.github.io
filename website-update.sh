#!/bin/bash
cd ~/mathe/verwaltung/Homepage
git add .
git commit -m "Update $(date '+%Y-%m-%d %H:%M')"
git push https://knuepfer:$(cat ~/mathe/verwaltung/Homepage/github-token.txt)@github.com/agknuepfer/agknuepfer.github.io.git
