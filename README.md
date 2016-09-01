[![Build Status](https://travis-ci.org/nikhilRP/framework.svg?branch=master)](https://travis-ci.org/nikhilRP/framework)

# Framework

Framework used for rapid application development at hackathons

## Dependencies:

    docker
    docker-compose

## Setup instructions for OS X:

  Follow the instructions to setup of the application

    docker-machine create -d virtualbox dev
    eval "$(docker-machine env dev)"

  Build and get the application running

    cd framework
    docker-compose build
    docker-compose up -d

  Create data models if there are any

    docker-compose run --rm -d web python create_db.py
