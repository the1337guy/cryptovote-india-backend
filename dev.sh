#!/bin/bash

CVI_MONGOURL='mongodb://127.0.0.1:27901' gunicorn -k gevent -b 127.0.0.1:9001 --reload main:__hug_wsgi__