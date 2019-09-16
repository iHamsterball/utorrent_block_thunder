#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# μTorrent Thunder Auto-block Script
# Copyright (C) 2019 Cother
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import json
import logging
import os
import re
import requests
import sched
import sys
import time
import timeit

from bs4 import BeautifulSoup
from logging.handlers import TimedRotatingFileHandler
from requests.auth import HTTPBasicAuth
from requests.cookies import RequestsCookieJar

# Logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(),
                              TimedRotatingFileHandler('filter.log', when='midnight')])
logger = logging.getLogger(__name__)

# Settings
protocal = 'http'
domain = 'localhost'
port = 43202
path = '/gui'
user = 'root'
password = 'toor'
ipfilter_path = os.path.join(os.getenv('appdata'), 'uTorrent', 'ipfilter.dat')
interval = 30


class Torrent():
    def __init__(self, list):
        self.hash = list[0]
        self.status = list[1]  # Binary
        self.name = list[2]
        self.size = list[3]  # Integer in bytes
        self.progress = list[4]  # Integer in per mils
        self.downloaded = list[5]  # Integer in bytes
        self.uploaded = list[6]  # Integer in bytes
        self.ratio = list[7]  # Integer in per mils
        self.upload_speed = list[8]  # Integer in bytes per second
        self.download_speed = list[9]  # Integer in bytes per second
        self.eta = list[10]  # Integer in seconds
        self.label = list[11]
        self.peers_connected = list[12]
        self.peers_in_swarm = list[13]
        self.seeds_connected = list[14]
        self.seeds_in_swarm = list[15]
        self.availability = list[16]  # Integer in 1/65535ths
        self.torrent_queue_order = list[17]
        self.remaining = list[18]  # Integer in bytes


class Peer():
    def __init__(self, list):
        self.country = list[0]
        self.ip = list[1]
        self.host = list[2]
        # list[3] unknown
        self.port = list[4]
        self.client = list[5]
        self.flags = list[6]
        self.progress = list[7]  # Integer in per mils
        self.download_speed = list[8]  # Integer in bytes per second
        self.upload_speed = list[9]  # Integer in bytes per second
        self.download_request = list[10]
        self.upload_request = list[11]
        self.connected_time = list[12]
        self.peer_downloaded = list[13]
        self.peer_uploaded = list[14]
        # list[15] unclear
        self.peer_download_speed = list[16]
        # list[17] unknown
        # list[18] unknown
        # list[19] unknown
        # list[20] unknown
        # list[21] unknown

        # End of list
        self.torrent_size = list[len(list)-1]


class FilterProcesser():
    def __init__(self):
        self.base = '{}://{}:{}{}'.format(protocal, domain, port, path)
        self.root = '{}/'.format(self.base)
        response = requests.get(self.root, auth=HTTPBasicAuth(user, password))
        self.cookie_jar = response.cookies
        self.token = self._get_token()
        self.cache_id = None
        logger.info('Root URL: {}'.format(self.root))
        logger.info('Token: {}'.format(self.token))

    # Get CSRF Token
    def _get_token(self):
        response = requests.get(url='{}/token.html'.format(self.base),
                                auth=HTTPBasicAuth(user, password),
                                cookies=self.cookie_jar)
        return BeautifulSoup(response.content, features='lxml').html.div.text

    # Get torrent list
    def _get_torrents(self):
        params = dict(token=self.token, list=1, cid=self.cache_id)
        response = requests.get(url=self.root,
                                params=params,
                                auth=HTTPBasicAuth(user, password),
                                cookies=self.cookie_jar)
        # Torrent/Labels List Definition
        # http://help.utorrent.com/customer/portal/articles/1573947
        content = json.loads(response.content)
        self.cache_id = content.get('torrentc')
        logging.debug('Torrent response: {}'.format(content))
        logging.debug('Cache ID: {}'.format(self.cache_id))
        return [Torrent(item) for item in content.get('torrents', content.get('torrentp', []))]

    # Check torrent status
    def _check_torrent(self, torrent):
        # torrent[12]: peers connected
        return torrent.peers_connected > 0

    # Get peers list by torrent hash
    def _get_peers(self, torrent):
        params = dict(token=self.token,
                      action='getpeers',
                      hash=torrent.hash,
                      t=int(time.time()))
        response = requests.get(url=self.root,
                                params=params,
                                auth=HTTPBasicAuth(user, password),
                                cookies=self.cookie_jar)
        struct = json.loads(response.content).get('peers')
        logging.debug('Peers of torrent {}: {}'.format(torrent.hash, struct))
        return [item+[torrent.size] for item in struct[1]] if len(struct) == 2 else []

    # Check peer avalibility
    def _check_peer(self, peer):
        strict = r'(-XL0012-)|(Xunlei)|(^7\.)|(QQDownload)|(Xfplay)|(dandanplay)'
        grace = r'(FDM)|(go\.torrent)|(Mozilla\/)'
        return peer.peer_downloaded < peer.torrent_size * (2 if re.search(grace, peer.client) is None else 1) and \
            re.search(strict, peer.client) is None or peer.peer_uploaded > 0

    # Get complete peers list
    def _get_all_peers(self):
        peers = dict()
        for torrent in self._get_torrents():
            if self._check_torrent(torrent):
                for peer in self._get_peers(torrent):
                    peer = Peer(peer)
                    peers[peer.ip] = peer
        logging.debug('Complete peers list: {}'.format(peers))
        return peers

    # Reload IPFilter
    def _reload_ipfilter(self):
        params = dict(token=self.token,
                      action='setsetting',
                      s='ipfilter.enable',
                      v=1)
        response = requests.get(url=self.root,
                                params=params,
                                auth=HTTPBasicAuth(user, password),
                                cookies=self.cookie_jar)
        return response.ok

    # Write block list to ipfilter file
    def _write_ipfilter(self, block_list):
        with open(ipfilter_path, mode='a+') as file:
            if not self._check_newline(file):
                file.write('\n')
            file.writelines(map(lambda s: s + '\n', block_list))

    # Check if ipfilter file is properly ended with newline
    def _check_newline(self, file):
        file.seek(file.tell() - 1, os.SEEK_SET)
        char = file.read()
        if char == '\r' or char == '\n':
            logging.debug('Target file ends with newline')
            return True
        logging.debug('Target file ends without newline')
        return False

    # Working loop
    def loop(self):
        block_list = set()
        for ip, peer in self._get_all_peers().items():
            if not self._check_peer(peer):
                block_list.add(ip)
        self._write_ipfilter(block_list)
        if len(block_list) > 0:
            logger.info('IPs to be blocked: {}'.format(block_list))
            self._reload_ipfilter()
        else:
            logger.debug('Nothing found')


if __name__ == "__main__":
    def loop():
        processer.loop()
        schedule.enter(delay=interval, priority=1, action=loop)
    processer = FilterProcesser()
    schedule = sched.scheduler(timeit.default_timer, time.sleep)
    schedule.enter(delay=0, priority=1, action=loop)
    try:
        schedule.run()
    except (KeyboardInterrupt, SystemExit):
        logging.info('Shutting down...')
        sys.exit()
