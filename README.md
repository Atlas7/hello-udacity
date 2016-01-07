# Intro

I use this repos to experiments with the exercises as layed out in the [Udacity Web Development Course - CS253](https://www.udacity.com/course/web-development--cs253).

Tech Stack:

- Development and Deployment Environment: Google App Engine Python SDK
- Web Framework: Python WebApp2 Framework.
- Web Template Engine: Python Jinja2

## Pre-requisit

Download the Google App Engine (GAE) Python SDK onto your Mac. See [here](https://cloud.google.com/appengine/docs/python/#download_the_app_engine_sdk_for_python) more more info.

All Web Applications are stored in the `/apps' directory.

# Instructions

The fundamentals (development and deployment) are covered in this very neat 5-minute [Hello World](https://cloud.google.com/appengine/docs/python/) Google App Engine Example.

## Test Web Applications

Testing on `localhost:8080` is very simple. Simply navigate to the `/apps' directory, and submit this one-line command:

```
dev_appserver.py folder-name/
```

Navigate to [localhost:8080](localhost:8080) to view the corresponding web application.

Note: The `app.yaml` is the configuration file that shows the main python file.

# Deploy

Navigate to the `/apps' directory, and submit this one-line command:

```
appcfg.py -A YOUR_PROJECT_ID update folder-name/
```

The web app is now deployed to:

```
http://YOUR_PROJECT_ID.appspot.com
```