#!/usr/bin/env python
#-*- encoding: utf8 -*-
import os
import re
import sys
import json
import textwrap

import requests

from cms.util import get_logger, User


class LIMS(object):
    base_url = 'http://lims.novogene.com/STARLIMS11.novogene'
    def __init__(self):
        pass

    def login(self, username, password):
        pass

    def search_project(self):
        pass


if __name__ == '__main__':
    main()
