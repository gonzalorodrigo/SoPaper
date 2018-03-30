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

HOSTNAME = 'pubs.rsc.org/'

# not working right now
@register_parser(name='pubs.rsc.org/',
                 urlmatch='pubs.rsc.org/',
                 meta_field=[],
                 priority=8)
class WILEY(ScienceDirect):
    def _do_pre_parse(self):

        """self.text = requests.get(self.url).text.encode('utf-8')
                                with open("/tmp/b.html", 'w') as f:
                                    f.write(self.text)
                                #text = open("/tmp/b.html").read()
                                self.soup = BeautifulSoup(self.text, "html.parser")"""


    def _get_url(self, url):
        print("RSC")
        inter_wait=2
        display = Display(visible=0, size=(800, 600))
        display.start()
        browser = webdriver.Firefox()
        browser.get(url)
        main_window = browser.current_window_handle
        pdf_url =""
        elements = browser.find_elements_by_tag_name("a")
        for elem in elements:
            title = elem.get_attribute("title")
            if title=="Link to PDF version":
                pdf_url = elem.get_attribute("href")
                break
        
        browser.quit()
        display.stop()
        print("rsc.org parser, url: {}".format(pdf_url))
        if pdf_url=="":
            raise RecoverableErr("No available download at {0}".format(
                                 self.url))
        return pdf_url

    def _do_download(self, updater):
        
        return direct_download(self._get_url(self.url), updater)

    def _do_get_title(self):
        """class="hlFld-Title" """
        return ""
        titles = self.soup.findAll(attrs={'class': 'hlFld-Title'})
        if titles:
            return titles[0]['content']
        return ""

    def _do_get_meta(self):
        meta = {}
        return meta