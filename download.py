#! /usr/bin/env python
#-*- coding: utf-8 -*-

from Tutsplus import Tutsplus

username = 'my_username'
password = 'my_password'
courses_url = ['https://tutsplus.com/course/say-yo-to-yeoman/',
                'https://tutsplus.com/course/phone-gap-essentials/' ]

t = Tutsplus(username, password)
t.download_courses(courses_url)
