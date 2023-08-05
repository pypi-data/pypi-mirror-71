#-*- encoding: utf8 -*-
import os
import logging
import getpass

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser


logging.getLogger("requests.packages.urllib3").propagate = 0


def get_logger(name=None, verbose=False):
    logging.basicConfig(
        format='[%(asctime)s %(funcName)s %(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO)
    logger = logging.getLogger(name)

    if verbose:
        logger.level = logging.DEBUG

    return logger


class User(object):
    def __init__(self, username=None, password=None, configfile=None, **kwargs):
        self.username = username
        self.password = password
        self.configfile = configfile
        self.conf = ConfigParser()

    def get_user_pass(self):
        if self.username and self.password:
            username, password = self.username, self.password
        elif self.configfile and os.path.exists(self.configfile):
            username, password = self.read()
        else:
            username, password = None, None

        if not all([username, password]):
            print('Please input your username and password')
            username = raw_input('> username: ')
            password = getpass.getpass('> password: ')

        return username, password

    def read(self):
        self.conf.read(self.configfile)
        username = password = None

        if self.conf.has_section('cms'):
            if self.username:
                username = self.username
                password = self.conf.get('cms', self.username)
            elif len(self.conf.options('cms')) == 1:
                username = self.conf.options('cms')[0]
                password = self.conf.get('cms', username)

        return username, password

    def save(self, username, password):
        if not self.conf.has_section('cms'):
            self.conf.add_section('cms')
        self.conf.set('cms', username, password)

        with open(self.configfile, 'w') as out:
            self.conf.write(out)


