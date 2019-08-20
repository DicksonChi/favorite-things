#!/usr/bin/env bash

npm install
npm run build

# use awscli to copy the built app to the bucket
aws s3 cp dist/ $1 --recursive

echo "Your have successully deployed the frontend now go and copy the Url from the buckett end point and enjoy!"