#!/bin/bash

generateDatabaseSchema() {
  echo generating
#  python3 create_schema.py
}

startApplication() {
  echo starting
}

getHelpMessage() {
    echo -e "Bootstrapping script"
    echo -e "Common usage: ./start.sh [-g]"
    exit 0
}

while getopts 'g' flag; do
  case "${flag}" in
    g) generateDatabaseSchema ;;
    *) getHelpMessage
      exit 1 ;;
  esac
done

startApplication
