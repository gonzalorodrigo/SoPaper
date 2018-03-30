#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: nih.py
# Date: 一 6月 09 17:06:26 2014 +0000
# Author: Gonzalo Rodrigo <gprodrigoalvarez@lbl.gov>

import re
from . import register_parser, RecoverableErr
from .base import FetcherBase, direct_download
from ..uklogger import *
from .. import ukconfig
from .sciencedirect import ScienceDirect

from urlparse import urlparse
import requests
from bs4 import BeautifulSoup

from pyvirtualdisplay import Display
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

HOSTNAME = 'onlinelibrary.wiley.com/'

# not working right now
@register_parser(name='onlinelibrary.wiley.com/',
                 urlmatch='onlinelibrary.wiley.com/',
                 meta_field=[],
                 priority=8)
class WILEY(ScienceDirect):
    def _do_pre_parse(self):
        self.text = requests.get(self.url).text.encode('utf-8')
        with open("/tmp/b.html", 'w') as f:
            f.write(self.text)
        #text = open("/tmp/b.html").read()
        self.soup = BeautifulSoup(self.text, "html.parser")


    def _get_url(self, url):
        inter_wait=2
        display = Display(visible=0, size=(800, 600))
        display.start()
        browser = webdriver.Firefox()
        browser.get(url)
        main_window = browser.current_window_handle
        
        elements = browser.find_elements_by_tag_name("a")
        pdf_url=""
        print("WILEY")
        for elem in elements:
            alt_att =  elem.get_attribute("title")
            if alt_att == "Article ePDF":
                href = elem.get_attribute("href")
                print("SECOND URL", href)

                split_url = href.split("epdf")
                href = "pdf".join(split_url)
                pdf_url=href
                break
        
        browser.quit()
        display.stop()
        print("wiley.com parser, url: {}".format(pdf_url))
        if pdf_url=="":
            raise RecoverableErr("No available download at {0}".format(
                                 self.url))
        return pdf_url

    def _do_download(self, updater):
        
        return direct_download(self._get_url(self.url), updater)

    def _do_get_title(self):
        """class="hlFld-Title" """
        titles = self.soup.findAll(attrs={'class': 'hlFld-Title'})
        return titles[0]['content']

    def _do_get_meta(self):
        meta = {}
        return meta
