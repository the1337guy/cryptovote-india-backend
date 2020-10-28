#!/bin/bash

gunicorn -k gevent -b 127.0.0.1:9001 --reload main:__hug_wsgi__