#!/usr/bin/env bash

# run python static validation
prospector  --profile-path=. --profile=.prospector.yml --path=favorite_things

# run bandit - A security linter from OpenStack Security
bandit -r favorite_things
