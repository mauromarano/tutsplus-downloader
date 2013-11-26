#! /usr/bin/env python
#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os

class Tutsplus:

    login_url= 'https://tutsplus.com/amember/login.php'

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
        login_attempt_id =  soup.find_all(attrs={"name": "login_attempt_id"})[0]['value']

        data = {
            "amember_login":self.username,
            "amember_pass":self.password,
            "remember_login":1,
            'login_attempt_id' : login_attempt_id
        }

        print data

        self.s.post(self.login_url, data = data)
        return True

    # Download all video from a course url
    def download_course(self, url):

        # Variable needed to increment the video number
        self.video_number = 1

        source = self.get_source(url)

        soup = BeautifulSoup(source)

        # the course's name
        self.course_title = soup.select('.title-text')[0].string
        os.makedirs(self.course_title)

        # array who stores the information about a course
        course_info = self.get_info_from_course(soup)

        for video in course_info:
            self.download_video(video)
            self.video_number = self.video_number + 1


    def download_courses(self,courses):

        for course in courses:

            self.download_course(course)

    # pass in the info of the lesson and it will download the video
    # lesson = {
    #   "titolo": 'video title',
    #   "link" : 'http://link_to_download'
    # }
    def download_video(self,lesson):

        source = self.get_source(lesson['link'])

        soup = BeautifulSoup(source)

        download_link= soup.select('.post-buttons > a')

        # If it finds more than 1 download link it will skip
        # the video files and will download the video only
        if len(download_link) == 1:
            download_link = download_link[0]
        else:
            download_link = download_link[1]

        # String name of the file
        name = self.course_title + '/[' + str(self.video_number) + '] ' + lesson['titolo']
        self.download_file(download_link['href'],name)

        print '[*] Downloaded > ' + lesson['titolo']

    # Function who downloads the file itself
    def download_file(self,url, name):
        # name = url.split('/')[-1]
        # NOTE the stream=True parameter
        name = name + '.mp4'
        r = self.s.get(url, stream=True)
        with open(name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        return name

    # return an array with all the information about a video (title, url)
    def get_info_from_course(self, soup):
        arr = []
        videos = soup.select('.section-title > a')

        for video in videos:
            if video.string is not None:
                titolo = video.string
                link = video['href']

                info = {
                    "titolo":titolo,
                    "link":link
                }
                arr.append(info)

        return arr
