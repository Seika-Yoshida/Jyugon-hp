# Juygon Corp HP

# Dev on local
## Install pacakges 
```
python install -r src/requirements.txt
```
## Set env if needed
```
export SENDGRID_API_KEY='<API_KEY>'
export SENDGRID_FROM='<EMAIL>'
export SENDGRID_TO='<EMAIL>'
```
## Run web server on local
```
python src/main.py
```
## Browse
http://127.0.0.1:8080

# Deploy on GAE

## Install the gcloud CLI
see: https://cloud.google.com/sdk/docs/install

## Setup google App engine
see: https://cloud.google.com/appengine/docs/standard/python3/runtime

## Set app.yaml in src folder.
ex)
```
runtime: python311
app_engine_apis: true
inbound_services:
- mail
- mail_bounce

automatic_scaling:
  max_instances: 1

handlers:
- url: /media
  static_dir: media

- url: /js
  static_dir: js

- url: /en/js
  static_dir: js

- url: /.*
  script: main.app

env_variables:
  SENDGRID_API_KEY: '<API_KEY>'
  SENDGRID_FROM: '<EMAIL>'
  SENDGRID_TO: '<EMAIL>'
```

## Deploy onto GAE
```
gcloud app deploy
```