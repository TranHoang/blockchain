#!/usr/bin/env bash

coverage run --source=.  -m unittest discover -s tests -p "*_test.py"
coverage report -m