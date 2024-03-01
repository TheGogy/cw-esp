#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: $0 <deep | shallow>"
elif [ "$1" = "deep" ]; then
	rm -rfv Users Models build dist Profiles.yml main.spec
elif [ "$1" = "shallow" ]; then
	rm -rfv Users/*/ Models/*/ build dist Profiles.yml main.spec
else
	echo "Usage: $0 <deep | shallow>"
fi
