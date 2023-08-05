#!/usr/bin/env python
# -*- encoding: utf8 -*-
import os
import re
import sys
import json
import time
import binascii
import textwrap

import requests

from cms.util import get_logger, User


class LIMS(object):
    base_url = 'http://lims.novogene.com/STARLIMS11.novogene'
    def __init__(self, logger=None):
        self.logger = logger or get_logger()
        self.session = requests.session()

    def login(self, username, password):
        # step1: get user info
        url = self.base_url + '/Authentication.GetUserInfoHtml.lims'

        username = username.upper()

        password = [binascii.b2a_hex(each.encode()).decode() for each in password]
        password = ''.join(list(map('{:0>4}'.format, password))).upper()

        payload = [username, password]
        user_info = self.session.post(url, json=payload).json()

        if not user_info:
            self.logger.error('login failed, please check your username and password!')
            return False

        self.logger.info('login successful!')
        dept = user_info[0]['Tables'][0]['Rows'][0]['Dept']
        role = user_info[1]['Tables'][0]['Rows'][0]['ROLE']

        url = self.base_url + '/Authentication.LoginMobile.lims'
        payload = {
            'user': username,
            'password': password,
            'dept': dept,
            'role': role,
            'platforma': 'HTML',
        }
        result = self.session.get(url, params=payload).text
        print result



def main(**args):

    start_time = time.time()

    logger = get_logger('LIMS', verbose=args['verbose'])
    print args

    user = User(section='lims', **args)
    username, password = user.get_user_pass()

    print username, password

    lims = LIMS(logger=logger)

    if lims.login(username, password):
        user.save(username, password)



def parser_add_lims(parser):

    parser.description = __doc__
    parser.epilog = textwrap.dedent('''
        \033[36mexamples:
            %(prog)s ...
        \033[0m
    ''')

    parser.add_argument('-u', '--username', help='the username to login lims')
    parser.add_argument('-p', '--password', help='the password to login lims')

    parser.add_argument('-debug', '--verbose',
                        help='logging in debug mode', action='store_true')

    parser.set_defaults(func=main)
