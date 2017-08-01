#!/bin/bash

ACCESS_TOKEN=b626ac6c59744e5ba7ddd088a0075893
ENVIRONMENT=production
LOCAL_USERNAME=`puruckertom`
REVISION=`git log -n 1 --pretty=format:"%H"`

curl https://api.rollbar.com/api/1/deploy/ \
  -F access_token=$ACCESS_TOKEN \
  -F environment=$ENVIRONMENT \
  -F revision=$REVISION \
  -F local_username=$LOCAL_USERNAME