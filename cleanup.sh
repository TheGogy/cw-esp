#!/bin/bash

# Removes the files that project creates

find ./Users ! -name 'ExampleUserCSS.css' -type f -exec rm -f {} +
rm -rf Profiles.yml
