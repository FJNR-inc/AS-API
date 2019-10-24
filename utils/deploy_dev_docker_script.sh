#!/usr/bin/env bash

echo -e "\e[32m\e[1mActivate virtualenv\e[0m"
. /opt/project/ve/bin/activate
zappa update dev
zappa manage dev migrate
zappa manage dev "collectstatic --noinput"