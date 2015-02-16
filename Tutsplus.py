#! /usr/bin/env python
#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import re

class Tutsplus:

    login_url= 'https://tutsplus.com/sign_in'
    login_post = 'https://tutsplus.com/sessions'
    home_url = 'https://tutsplus.com'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login()

    # Return the html source for a specified url
    def get_source(self, url):
        r = self.s.get(url)
        return r.content

    # It logs in and store the session for the future requests
    def login(self):
        self.s = requests.session()
        soup = BeautifulSoup(self.get_source(self.login_url))
        self.token = soup.find(attrs={"name":"csrf-token"})['content']

        data = {
            "session[login]": self.username,
            "session[password]": self.password,
            "authenticity_token": self.token,
            "utf8": "✓"
        }

        self.s.post(self.login_post, data = data)
        return True

    # Download all video from a course url
    def download_course(self, url):
        # Variable needed to increment the video number
        video_number = 1

        # update csrf token for each course
        soup = BeautifulSoup(self.get_source(url))
        self.token = soup.find(attrs={"name":"csrf-token"})['content']

        # the course's name
        course_title = soup.select('h1')[0].string.replace('/','-')
        print "######### " + course_title + " #########"
        if not os.path.exists(course_title) :
            os.makedirs(course_title)

        # if the course includes sourcefiles download them first
        sourcefile = soup.select('.course-actions__download-button')
        if sourcefile:
            print "[+] Downloading source files"
            filename = course_title + '/sources.zip'
            link = sourcefile[0]['href']
            self.download_file(link, filename)

        # array who stores the information about a course
        course_info = self.get_info_from_course(soup)

        for video in course_info:
            print "[+] Downloading " + video['titolo'].encode("utf-8")
            filename = course_title + '/[' + str(video_number).zfill(2) + '] ' + re.sub('[[^A-Za-z0-9 ]+, ' ', video['titolo']) + '.mp4'
            self.download_video(video['link'], filename)
            video_number = video_number + 1


    def download_courses(self, courses):
        for course in courses:
            self.download_course(course)

    def download_video(self, url, filename):
        # the trick for video links is not to follow the redirect, but to fetch the download link manually
        # otherwise we'll get an SignatureDoesNotMatch error from S3
        data = {
            "authenticity_token": self.token,
            "_method": 'post'
        }
        soup = BeautifulSoup(self.s.post(url, data = data, allow_redirects=False).content)
        url = soup.find_all('a')[0]['href']
        self.download_file(url, filename)

    # Function who downloads the file itself
    def download_file(self, url, filename):
        r = self.s.get(url, stream=True)
        if not os.path.isfile(filename) :
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()

    # return an array with all the information about a video (title, url)
    def get_info_from_course(self, soup):
        arr = []
        videos = soup.select('.lesson-index__lesson')

        for video in videos:

            titolo = video.select('.lesson-index__lesson-title')[0].string
            link = video.select('a')[0]['href']

            info = {
                "titolo": titolo,
                "link": link,
            }
            arr.append(info)

        return arr
