#! /usr/bin/env python
################################################################################
##
##  recvfile.py
##
##  Copyright (C) by Steve King <steve@narbat.com> 2016
##  This code my be freely used or modified for any purpose.
##
################################################################################
import logging
import logging.handlers
import optparse
import os
import re
import subprocess
import sys
import time
import unittest
import base64
from cStringIO import StringIO
import tarfile
import json

################################################################################
##
##  Main
##
################################################################################
class Main(object):
    VERSION = '%prog 1.0'

    ############################################################################
    ##  _log_setup
    ############################################################################
    def _log_setup(self, loglevel=logging.INFO, stdout=True, stderr=False, syslog=False, logfile=None):
        class MainFormatter(logging.Formatter):
            _default = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            _debug   = logging.Formatter(fmt='%(asctime)s %(levelname)s (%(module)s:%(lineno)d) %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            def format(self, record):
                fmt = self._debug if record.levelno < logging.INFO else self._default
                return fmt.format(record)
            def add(self, log, hdl):
                hdl.setFormatter(self)
                log.addHandler(hdl)

        logging.addLevelName(logging.FATAL,   '[F]')
        logging.addLevelName(logging.ERROR,   '[E]')
        logging.addLevelName(logging.WARNING, '[W]')
        logging.addLevelName(logging.INFO,    '[I]')
        logging.addLevelName(logging.DEBUG,   '[D]')

        try:
            logging.captureWarnings(True)   # Doesn't exist before 2.7
        except AttributeError:
            pass

        global log
        log = logging.getLogger()
        fmt = MainFormatter()

        if stdout:  fmt.add(log, logging.StreamHandler(sys.stdout))
        if stderr:  fmt.add(log, logging.StreamHandler(sys.stderr))
        if syslog:  fmt.add(log, logging.handlers.SysLogFileHandler())
        if logfile: fmt.add(log, logging.FileHandler(logfile, mode='w'))

        log.setLevel(loglevel)
        log.info(self.parser.get_version())
        log.debug('Verbose logging enabled')

    ############################################################################
    ##  _opt_setup
    ############################################################################
    def _opt_setup(self):
        usage = '%prog [options]'
        descr = ''.strip()
        defaults = {
            'verbose' : False,
        }

        parser = optparse.OptionParser(usage=usage, description=descr, version=Main.VERSION)
        parser.set_defaults(**defaults)

        parser.add_option('-v', '--verbose',
                dest='verbose', action='store_true',
                help='Verbose output [def: %s]'%parser.defaults.get('verbose', None))

        return parser

    ############################################################################
    ##  __init__
    ############################################################################
    def __init__(self):
        self.parser = self._opt_setup()
        (self.opts, self.args) = self.parser.parse_args()
        level = logging.DEBUG if self.opts.verbose else logging.INFO
        self._log_setup(loglevel=level, stdout=False, logfile='/tmp/recvfile.log')

    ############################################################################
    ##  readline
    ############################################################################
    def readline(self):
        data = sys.stdin.readline().strip()
        self.lineno += 1
        log.debug('%5d: %r', self.lineno, data)
        return data

    ############################################################################
    ##  sanitize
    ############################################################################
    def sanitize(self, name):
        # Allow all printable ASCII except slash, backslash
        return re.sub(r'[^0-9A-Za-z !"#$%&\'()*+,-.:;<=>?@\[\]^_`{|}~]', '?', name)

    ############################################################################
    ##  main
    ############################################################################
    def main(self):
        self.lineno = 0
        data = ''
        parms = {}

        # First line is optional JSON object with parameters
        line = self.readline()
        try:
            parms = json.loads(line)
        except ValueError:
            pass
        else:
            line = ''
        log.info('parms=%r', parms)

        # Remainder is base64 encoded tar file
        while not re.search(r'[^A-Za-z0-9/+=]', line):
            data += base64.b64decode(line)
            line = self.readline()
        tar = tarfile.open(fileobj=StringIO(data))
        log.info('%r', tar.getnames())

        # Extract to ~/Downloads
        host = None
        if 'host' in parms:
            log.info('host=%r', parms['host'])
            host = self.sanitize(parms['host'])
        if not host:
            host = 'sendfile'
        savedir = os.path.join(os.path.expanduser("~/Downloads"), '%s.%s'%(host, time.strftime('%Y%m%d.%H%M%S')))
        os.mkdir(savedir)
        tar.extractall(path=savedir)

        return(0)

################################################################################
##
##  __main__
##
################################################################################
if __name__ == '__main__':
    main = Main()
    try:
        sys.exit(main.main())
    except (Exception, KeyboardInterrupt) as e:
        logging.getLogger().fatal('ERROR: %s %s', e.__class__.__name__, e, exc_info=True)
        sys.exit(1)
