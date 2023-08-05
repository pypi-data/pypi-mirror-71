#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Created by Swen Vermeul on Feb 26th 2018
Copyright (c) 2018 ETH Zuerich All rights reserved.
"""

import os
import pwd
import re

from jupyterhub.auth import LocalAuthenticator
from sudospawner import SudoSpawner
import pamela
from tornado import gen
from traitlets import Unicode, Bool

from pybis.pybis import Openbis



class OpenbisAuthenticator(LocalAuthenticator):
    server_url = Unicode(
        config=True,
        help='URL of openBIS server to contact'
    )

    kerberos_domain = Unicode(
        config=True,
        help='The domain to authenticate against to obtain a kerberso ticket'
    )

    verify_certificates = Bool(
        config=True,
        default_value=True,
        help='Should certificates be verified? Normally True, but maybe False for debugging.'
    )

    valid_username_regex = Unicode(
        r'^[a-z][.a-z0-9_-]*$',
        config=True,
        help="""Regex to use to validate usernames before sending to openBIS."""
    )


    @gen.coroutine
    def authenticate(self, handler, data):
        """Checks username and password against the given openBIS instance.
        If authentication is successful, it not only returns the username but
        a data structure:
        {
            "name": username,
            "auth_state": {
                "token": openBIS.token,
                "url"  : openBIS.url
            }
        }
        """
        username = data['username']
        password = data['password']

        # Protect against invalid usernames as well as LDAP injection attacks
        if not re.match(self.valid_username_regex, username):
            self.log.warn('Invalid username')
            return None

        # No empty passwords!
        if password is None or password.strip() == '':
            self.log.warn('Empty password')
            return None


        openbis = Openbis(self.server_url, verify_certificates=self.verify_certificates)
        try:
            # authenticate against openBIS and store the token (if possible)
            openbis.login(username, password)

            # creating user if not found on the system, custom logic
            if self.create_system_users:
                try:
                    user = pwd.getpwnam(username)
                except KeyError:
                    self.create_user(username)

            # instead of just returning the username, we return a dict
            # containing the auth_state as well
            kerberos_username = username
            if getattr(self, 'kerberos_domain', None):
               kerberos_username = username + '@' + self.kerberos_domain

            return {
                "name": kerberos_username,
                "auth_state": {
                    "token": openbis.token,
                    "url": openbis.url,
                    "kerberos_username": kerberos_username,
                    "kerberos_password": password,

                }
            }
        except ValueError as err:
            self.log.warn(str(err))
            return None


    @gen.coroutine
    def pre_spawn_start(self, user, spawner):
        """Pass openbis token to spawner via environment variable"""
        auth_state = yield user.get_auth_state()
        if not auth_state:
            # auth_state not enabled
            return

        # Write the openBIS token to the users' environment variables
        spawner.environment['OPENBIS_URL']       = auth_state['url']
        spawner.environment['OPENBIS_TOKEN']     = auth_state['token']
        spawner.environment['KERBEROS_USERNAME'] = auth_state['kerberos_username']
        spawner.environment['KERBEROS_PASSWORD'] = auth_state['kerberos_password']


    def get_new_uid_for_home(self, os_home):
        id_sequence = 999; # Linux uids start at 1000
        for file in next(os.walk(os_home))[1]:
            home_info = os.stat(os_home + file)
            if home_info.st_uid > id_sequence:
                id_sequence = home_info.st_uid
            if home_info.st_gid > id_sequence:
                id_sequence = home_info.st_gid
        if id_sequence is None:
            return None
        else:
            return { "uid" : id_sequence + 1 }

    def create_user(self, username):
        os_home = "/home/" # Default CentOS home as used at the ETHZ
        home = os_home + username
        useradd = "useradd " + username
        if os.path.exists(home): # If the home exists
            home_info = os.stat(home)
            home_uid = home_info.st_uid
            useradd = useradd + " --uid " + str(home_uid) + " -G jupyterhub"
        elif os.path.exists(os_home):
            new_uid = self.get_new_uid_for_home(os_home)
            if new_uid is not None:
                useradd = useradd + " --uid " + str(new_uid["uid"]) + " -G jupyterhub"
        os.system(useradd)


class KerberosSudoSpawner(SudoSpawner):
    """Specialized SudoSpawner which defines KERBEROS_USERNAME and KERBEROS_PASSWORD
    for the global environment variables. These variables are later used by the
    sudospawner-singleuser script to log in to Active Director to obtain a valid Kerberos ticket
    """

    def get_env(self):
        env = super().get_env()

        spawner_env = getattr(self.user.spawner, 'environment', None)
        if not spawner_env:
            # auth_state was probably not enabled
            return env
        env['KERBEROS_USERNAME'] = spawner_env['KERBEROS_USERNAME']
        env['KERBEROS_PASSWORD'] = spawner_env['KERBEROS_PASSWORD']
        return env
