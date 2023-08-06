django-jauth
============

Simple OAuth2 authentication client library for Django and Django REST framework projects. Django 3.0 support. Unit test coverage 51%.


Features
========

* Supports simple integration both to single page apps (via postMessage) and traditional Django apps (via redirect)

* Does not require any JavaScript libraries

This is by no means comprehensive OAuth2 package but simple and serves single purpose.

## Supported / Tested OAuth2 Providers

* Facebook

* AccountKit

* Google

## Other Features

* Supports deauthorize and delete Facebook callbacks
 

Configuration
=============

settings.JAUTH_AUTHENTICATION_SUCCESS_REDIRECT:

* Set this as URL of user home page after login. Set as None for single-page apps which open separate dialog for login (Value None causes postMessage to be called for the parent window with authentication result)

settings.JAUTH_AUTHENTICATION_ERROR_REDIRECT:

* Set this as URL of login page with querystring parameter "error" as error message. Can be None for single page apps.


Install
=======

* pip install django-jauth

