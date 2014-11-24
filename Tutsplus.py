#! /usr/bin/env python
#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os

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

    # It logs in and store the sesson for the future requests
    def login(self):
        self.s = requests.session()
        soup = BeautifulSoup(self.get_source(self.login_url))

        data = {
            "session[login]":self.username,
            "session[password]":self.password,
            "authenticity_token": soup.find(attrs={"name":"csrf-token"})['content'],
            "utf8":"✓"
        }

        self.s.post(self.login_post, data = data)
        return True

    # Download all video from a course url
    def download_course(self, url):

        # Variable needed to increment the video number
        self.video_number = 1

        source = self.get_source(url)

        soup = BeautifulSoup(source)

        # the course's name
        self.course_title = soup.select('h1')[0].string
        if not os.path.exists(self.course_title) :
            os.makedirs(self.course_title)

        # array who stores the information about a course
        course_info = self.get_info_from_course(soup)

        for video in course_info:
            print "[+] Downloading " + video['titolo']
            name = self.course_title + '/[' + str(self.video_number) + '] ' + video['titolo']
            self.download_file(video['link'],name)
            self.video_number = self.video_number + 1


    def download_courses(self,courses):

        for course in courses:

            self.download_course(course)

    # pass in the info of the lesson and it will download the video
    # lesson = {
    #   "titolo": 'video title',
    #   "link" : 'http://link_to_download'
    # }

    # Function who downloads the file itself
    def download_file(self,url, name):
        # name = url.split('/')[-1]
        # NOTE the stream=True parameter
        name = name + '.mp4'
        r = self.s.get(url, stream=True)
        if not os.path.isfile(name) :
            with open(name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
        return name

    # return an array with all the information about a video (title, url)
    def get_info_from_course(self, soup):
        arr = []
        videos = soup.select('.lesson-index__lesson')

        for video in videos:

            titolo = video.select('.lesson-index__lesson-title')[0].string
            link = video.select('a')[0]['href']

            info = {
                "titolo":titolo,
                "link":link,
            }
            arr.append(info)

        return arr

