#!/bin/bash
cd ~/mathe/verwaltung/Homepage
git add .
git commit -m "Update $(date '+%Y-%m-%d %H:%M')"
git push
