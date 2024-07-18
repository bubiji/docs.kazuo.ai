#!/usr/bin/env bash

find docs -name '*.md' | while read F;do python upload_file.py $F; done
