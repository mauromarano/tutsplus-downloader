This is for paid user only!
===========================

Before anything else let's clarify that this script is  for paid users only.

This script will simply don't work if you don't provide a valid username and password. The account you provide must be a valid tutsplus premium's account.

Why this script?
================

Tutsplus already allow us to download their video. In fact in each lesson's page there is a shiny download button.

Because I watch their video mostly offline (during train travelling) I needed a way to bulk download the courses. This script just automates this process.

Installation
=============

1. Clone this repository
2. pip install -r requirements.txt


Example
========

```#! /usr/bin/env python
#-*- coding: utf-8 -*-

from Tutsplus import Tutsplus

username = 'my_username'
password = 'my_password'
courses_url = ['https://tutsplus.com/course/say-yo-to-yeoman/',
                'https://tutsplus.com/course/phone-gap-essentials/' ]

t = Tutsplus(username, password)
t.download_courses(courses_url)```
