from os.path import dirname, realpath
import os
from ConfigParser import SafeConfigParser
import ConfigParser
import argparse
import pymongo
from queries import query_list

#log = logging.getLogger(__name__)


def load_config():
    parent = dirname(dirname(realpath(__file__)))
    conf_file = os.path.join(parent, 'conf/settings.ini')
    assert os.path.isfile(conf_file), "missing %s" % conf_file
    config = SafeConfigParser()
    config.optionxform = str
    config.readfp(open(conf_file))
    return config

