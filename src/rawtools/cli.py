# -*- coding: utf-8 -*-

"""
"""

from plumbum import cli
import pkg_resources
from sys import stdout, stdin, exit
import os
import numpy as np
import json
from rawtools import decobs, unpack


class NumpyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()

        return super(NumpyJSONEncoder, self).default(obj)


def write_to_stdout(items):

    try:
        for item in items:
            stdout.write(item + os.linesep)
    except BrokenPipeError:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, stdout.fileno())
        exit(1)


class RawTool(cli.Application):
    """
    Command line tool.
    """

    PROGNAME = 'rt'
    VERSION = pkg_resources.require('rawtools')[0].version

    def main(self):
        pass


@RawTool.subcommand('decobs')
class RTdecode(cli.Application):
    """COBS-decode binary packets from named file."""

    @cli.positional(cli.ExistingFile)
    def main(self, filename=None):
        if filename is None:
            source = stdin.buffer  # binary mode
        else:
            source = open(filename, 'rb')

        with source as f:
            msgs = decobs(f.read())
            write_to_stdout([msg.hex() for msg in msgs])


@RawTool.subcommand('unpack')
class RTunpack(cli.Application):
    """
    Convert raw messages to frames.

    Frames having .logid, .timestamp, .samplecount, and .payload.
    """

    @cli.positional(cli.ExistingFile)
    def main(self, filename=None):
        if filename is None:
            source = stdin  # text mode
        else:
            source = open(filename, 'r')

        with source as f:
            hexlines = f.readlines()
            msgs = [bytes.fromhex(line) for line in hexlines]
            frames = unpack(msgs)
            write_to_stdout([frame.as_json() for frame in frames])


@RawTool.subcommand('dehex')
class RTdehex(cli.Application):
    """Convert hex string to numbers of a certain type."""

    strip = cli.Flag('strip', help='Strip quotes at ends of lines')
    concat = cli.Flag('concat', help='Concatenate output into single list')

    @cli.positional(str, cli.ExistingFile)
    def main(self, datatype, filename=None):
        if filename is None:
            source = stdin  # text mode
        else:
            source = open(filename, 'r')

        with source as f:
            hexlines = f.readlines()
            stripchars = '"\'\n' if self.strip else '\n'
            binaries = [bytes.fromhex(line.strip(stripchars))
                        for line in hexlines]
            dt = np.dtype(datatype)
            dt.newbyteorder('<')
            arrays = [np.frombuffer(binary, dtype=dt) for binary in binaries]

            if self.concat:
                if len(arrays) > 0:
                    array = np.concatenate(arrays)
                else:
                    array = np.empty((0, ), dtype=dt)
                write_to_stdout([json.dumps(array, cls=NumpyJSONEncoder)])
            else:
                write_to_stdout([json.dumps(array, cls=NumpyJSONEncoder)
                                 for array in arrays])


def main():
    RawTool.run()
