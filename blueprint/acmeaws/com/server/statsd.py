from ConfigParser import NoOptionError, NoSectionError
import logging
import random
import socket
import sys

from blueprint import cfg

try:
    host, port = cfg.get('statsd', 'host'), cfg.getint('statsd', 'port')
except (NoOptionError, NoSectionError, ValueError):
    host = port = None


def timing(stat, time, sample_rate=1):
    _send({stat: '{0}|ms'.format(time)}, sample_rate)


def increment(stats, sample_rate=1):
    update(stats, 1, sample_rate)


def decrement(stats, sample_rate=1):
    update(stats, -1, sample_rate)


def update(stats, delta=1, sample_rate=1):
    if type(stats) is not list:
        stats = [stats]
    _send(dict([(stat, '{0}|c'.format(delta)) for stat in stats]), sample_rate)


def _send(data, sample_rate=1):
    """
    :type data: dict
    :type sample_rate int
    """
    if host is None or port is None:
        return
    sampled_data = {}
    if 1 > sample_rate:
        if random.random() <= sample_rate:
            for k, v in data.iteritems():
                sampled_data[k] = '{0}|@{1}'.format(v, sampled_data)
    else:
        sampled_data = data
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        for k, v in sampled_data.iteritems():
            s.sendto('{0}:{1}'.format(k, v), (host, port))
    except:
        logging.error(repr(sys.exc_info()))
