#!/bin/bash

# # запуск
python3 src/main.py

# чистка
find . -name '*.session' | while read f; do rm "$f"; done
find . -name '*journal' | while read f; do rm "$f"; done