# -*- coding: utf-8 -*-

"""
"""

from plumbum import cli
import pkg_resources  # part of setuptools


class RawTool(cli.Application):
    """
    Command line tool.
    """

    PROGNAME = 'rt'
    VERSION = pkg_resources.require('rawtools')[0].version

    def main(self, *args):
        pass


@RawTool.subcommand('decode')
class RTdecode(cli.Application):
    "cobs decode package stream"

    def main(self, *args):
        print('Not implemented, yet. Stay tuned!', *args)


def main():
    RawTool.run()
