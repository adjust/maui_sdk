#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ADJUST_SDK_NUSPEC = os.path.join(ROOT, 'AdjustSdk.nuspec')

def run(cmd):
    print('> ' + ' '.join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)

def pack(config):
    run(['nuget', 'pack', ADJUST_SDK_NUSPEC, '-properties', 'Configuration=%s' % config])

def main():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--debug', action='store_true', default=False, help='Publish in Debug (default: Release)')

    parser = argparse.ArgumentParser(description='Publish the MAUI SDK')
    sub = parser.add_subparsers(dest='command')
    sub.add_parser('pack', help='Package nuget spec for the MAUI SDK', parents=[common])

    args = parser.parse_args()

    config = 'Debug' if getattr(args, 'debug', False) else 'Release'

    arg_found = False

    if args.command == 'pack':
        pack(config)
        arg_found = True

    if not arg_found:
        parser.print_help()
        return 1

    return 0

if __name__ == "__main__":
    main()