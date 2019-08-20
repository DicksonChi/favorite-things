#!/usr/bin/env bash

npm install
npm run build
aws s3 cp dist/ $1 --recursive