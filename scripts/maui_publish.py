#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ADJUST_SDK_NUSPEC = os.path.join(ROOT, 'AdjustSdk.nuspec')

# dotnet nuget add source ~/.nuget/local --name LocalSource
# nuget sources Add -Name "LocalSource" -Source ~/.nuget/local
DOT_NUGET = os.path.join(os.path.expanduser('~'), '.nuget')
NUGET_LOCAL_SOURCE = os.path.join(DOT_NUGET, 'local')
ADJUST_NUGET_INSTALLED = os.path.join(DOT_NUGET, 'packages', 'adjust.maui.sdk')

def run(cmd):
    print('> ' + ' '.join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)

def delete_file(path):
    if run('command -v trash >/dev/null 2>&1') == 0:
        run(['trash', path])
    else:
        run(['rm', '-rf', path])

'''
def load_env():
    p = Path('.env.local')
    if not p.exists():
        return
    with p.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip("'").strip('"')
            if key in os.environ:
                continue
            os.environ[key] = val

def read_env(key):
    return os.environ.get(key, '')
'''

def read_version(nuspec_file):
    with open(nuspec_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("<version>") and line.endswith("</version>"):
                # parse the middle content
                return line[len("<version>") : -len("</version>")].strip()
    return ''

def pack(config):
    run(['nuget', 'pack', ADJUST_SDK_NUSPEC, '-properties', 'Configuration=%s' % config])

def copy():
    run(['cp', 'Adjust.Maui.Sdk.%s.nupkg' % read_version(ADJUST_SDK_NUSPEC), NUGET_LOCAL_SOURCE])

def clean():
    delete_file(ADJUST_NUGET_INSTALLED)

def main():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--debug', action='store_true', default=False, help='Publish in Debug (default: Release)')

    parser = argparse.ArgumentParser(description='Publish the MAUI SDK')
    sub = parser.add_subparsers(dest='command')
    sub.add_parser('pack', help='Package nuget spec for the MAUI SDK', parents=[common])
    sub.add_parser('copy', help='Copy nuget package to the local source', parents=[common])
    sub.add_parser('clean', help='Clean the local source', parents=[common])

    args = parser.parse_args()

    config = 'Debug' if getattr(args, 'debug', False) else 'Release'
    all = args.command is None

    arg_found = False

    if args.command in ('pack') or all:
        pack(config)
        arg_found = True
    if args.command in ('copy') or all:
        copy()
        arg_found = True
    if args.command in ('clean') or all:
        clean()
        arg_found = True

    if not arg_found:
        parser.print_help()
        return 1

    return 0

if __name__ == "__main__":
    main()