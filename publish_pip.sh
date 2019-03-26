#!/bin/bash


function print_help {
    echo ""
    echo "Usage: publish_pip <new_version_number>"
    echo ""
}

if [[ -z "$1" ]]
then
    echo "Version number not provided!"
    print_help
    exit 1
elif [[ $1 == "--help" ]]
then
    print_help
    exit 0
fi

echo "Cleanup previous versions"
rm -rf ./dist

echo "set version: $1"
python3 setup.py bdist_wheel
python3 -m twine upload dist/*
