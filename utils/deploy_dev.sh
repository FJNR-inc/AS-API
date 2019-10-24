#!/bin/bash

if [ "$TRAVIS_BRANCH" == "develop" ] && [ "$TRAVIS_REPO_SLUG" == "FJNR-inc/Blitz-API" ] && [ "${TRAVIS_PULL_REQUEST}" = "false" ]; then

    docker-compose run --rm \
    -e AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY \
    api \
    bash -c "bash ./utils/deploy_dev.sh"
else
    echo "skip deploy since we are not on fjnr-inc/develop branch"
fi

{    "dev": {        "aws_region": "ca-central-1",        "certificate_arn": "",        "domain": "dev-api-as.fjnr.ca",        "route53_enabled": "false",        "django_settings": "artsouterrain.settings",        "project_name": "as-dev",        "memory_size": 1024,        "runtime": "python3.6",        "s3_bucket": "as-dev-api-zappa",        "aws_environment_variables": {            "SECRET_KEY": "%t_jo744sd@6u*w^wvt!k-((4q3e*mivszaf1!d1)_ru1-m(ld",            "DB_PASSWORD": "~{?*3Gmn6i(T&o3|S;AM[8&E",            "DB_USER": "root",            "DB_HOST": "as-dev-rds-postgres.ce3xbslg5njm.ca-central-1.rds.amazonaws.com",            "DB_PORT": "5432",            "DEBUG": "True",            "ALLOWED_HOSTS": "127.0.0.1, localhost, 39d8hos2hd.execute-api.ca-central-1.amazonaws.com",            "AWS_S3_REGION_NAME": "ca-central-1",            "AWS_STORAGE_STATIC_BUCKET_NAME": "as-dev-api-static",            "AWS_STORAGE_MEDIA_BUCKET_NAME": "as-dev-api-media",            "AWS_S3_STATIC_CUSTOM_DOMAIN": "as-dev-api-static.s3.ca-central-1.amazonaws.com",            "AWS_S3_MEDIA_CUSTOM_DOMAIN": "as-dev-api-media.s3.ca-central-1.amazonaws.com",            "STATIC_URL": "https://thesezvous-api-static.s3.ca-central-1.amazonaws.com/",            "STATICFILES_STORAGE": "artsouterrain.storage_backends.S3StaticStorage",            "MEDIA_URL": "https://as-dev-api-media.s3.ca-central-1.amazonaws.com/",            "MEDIA_ROOT": "https://as-dev-api-media.s3.ca-central-1.amazonaws.com/",            "DEFAULT_FILE_STORAGE": "artsouterrain.storage_backends.S3MediaStorage",            "DEFAULT_FROM_EMAIL": "support@fjnr.ca",            "ADMINS": "support@fjnr.ca",            "SERVER_EMAIL": "support@fjnr.ca",            "DATA_UPLOAD_MAX_MEMORY_SIZE": "5242880",            "FILE_UPLOAD_MAX_MEMORY_SIZE": "5242880"        },        "vpc_config" : {            "SubnetIds": [ "subnet-0ae4d7edd5f50af57","subnet-0a8d874c452703d5d" ],            "SecurityGroupIds": [ "sg-00febc0e65e364d0f" ]        }    }}