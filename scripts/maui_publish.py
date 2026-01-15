#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import shutil
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ADJUST_CORE_NUSPEC = os.path.join(ROOT, 'AdjustSdk.nuspec')
ADJUST_OAID_NUSPEC = os.path.join(ROOT, 'AdjustOaid.nuspec')
ADJUST_META_REFERRER_NUSPEC = os.path.join(ROOT, 'AdjustMetaReferrer.nuspec')
ADJUST_GOOGLE_LVL_NUSPEC = os.path.join(ROOT, 'AdjustGoogleLVL.nuspec')

# dotnet nuget add source ~/.nuget/local --name LocalSource
# nuget sources Add -Name "LocalSource" -Source ~/.nuget/local
DOT_NUGET = os.path.join(os.path.expanduser('~'), '.nuget')
NUGET_LOCAL_SOURCE = os.path.join(DOT_NUGET, 'local')
ARTIFACTS_OUTPUT_DIR = os.path.join(ROOT, '.artifacts')

ADJUST_CORE_NUGET_INSTALLED = os.path.join(DOT_NUGET, 'packages', 'adjust.maui.sdk')
ADJUST_OAID_NUGET_INSTALLED = os.path.join(DOT_NUGET, 'packages', 'adjust.maui.sdk.oaid')
ADJUST_META_REFERRER_NUGET_INSTALLED = os.path.join(DOT_NUGET, 'packages', 'adjust.maui.sdk.meta.referrer')
ADJUST_GOOGLE_LVL_NUGET_INSTALLED = os.path.join(DOT_NUGET, 'packages', 'adjust.maui.sdk.google.lvl')

def run(cmd):
    print('> ' + ' '.join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)

def delete_file(path):
    # Prefer the macOS `trash` command when available so files go to the Trash
    # instead of being permanently removed. Fallback to `rm -rf` otherwise.
    if shutil.which('trash') is not None:
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

def pack(config, target):
    if target == 'core' or target == 'all':
        print('> Packing Core SDK')
        run(['nuget', 'pack', ADJUST_CORE_NUSPEC, '-properties', 'Configuration=%s' % config])
    if target == 'oaid' or target == 'all':
        print('> Packing OAID SDK plugin')
        run(['nuget', 'pack', ADJUST_OAID_NUSPEC, '-properties', 'Configuration=%s' % config])
    if target == 'meta_referrer' or target == 'all':
        print('> Packing Meta Referrer SDK plugin')
        run(['nuget', 'pack', ADJUST_META_REFERRER_NUSPEC, '-properties', 'Configuration=%s' % config])
    if target == 'google_lvl' or target == 'all':
        print('> Packing Google LVL SDK plugin')
        run(['nuget', 'pack', ADJUST_GOOGLE_LVL_NUSPEC, '-properties', 'Configuration=%s' % config])

def copy(target):
    if target == 'core' or target == 'all':
        print('> Copying Core SDK')
        run(['cp', 'Adjust.Maui.Sdk.%s.nupkg' % read_version(ADJUST_CORE_NUSPEC), NUGET_LOCAL_SOURCE])
    if target == 'oaid' or target == 'all':
        print('> Copying OAID SDK plugin')
        run(['cp', 'Adjust.Maui.Sdk.Oaid.%s.nupkg' % read_version(ADJUST_OAID_NUSPEC), NUGET_LOCAL_SOURCE])
    if target == 'meta_referrer' or target == 'all':
        print('> Copying Meta Referrer SDK plugin')
        run(['cp', 'Adjust.Maui.Sdk.Meta.Referrer.%s.nupkg' % read_version(ADJUST_META_REFERRER_NUSPEC), NUGET_LOCAL_SOURCE])
    if target == 'google_lvl' or target == 'all':
        print('> Copying Google LVL SDK plugin')
        run(['cp', 'Adjust.Maui.Sdk.Google.LVL.%s.nupkg' % read_version(ADJUST_GOOGLE_LVL_NUSPEC), NUGET_LOCAL_SOURCE])

def clean(target):
    if target == 'core' or target == 'all':
        print('> Cleaning Core SDK')
        delete_file(ADJUST_CORE_NUGET_INSTALLED)
    if target == 'oaid' or target == 'all':
        print('> Cleaning OAID SDK plugin')
        delete_file(ADJUST_OAID_NUGET_INSTALLED)
    if target == 'meta_referrer' or target == 'all':
        print('> Cleaning Meta Referrer SDK plugin')
        delete_file(ADJUST_META_REFERRER_NUGET_INSTALLED)
    if target == 'google_lvl' or target == 'all':
        print('> Cleaning Google LVL SDK plugin')
        delete_file(ADJUST_GOOGLE_LVL_NUGET_INSTALLED)

def main():
    parser = argparse.ArgumentParser(description='Publish the MAUI SDK')
    sub = parser.add_subparsers(dest='command')

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--debug', action='store_true', default=False, help='Publish in Debug (default: Release)')

    common.add_argument(
        'target',
        nargs='?',
        choices=['core', 'oaid', 'meta_referrer', 'google_lvl', 'all'],
        help='Which target to publish (default: core)'
    )

    sub.add_parser('pack', help='Package nuget spec for the MAUI SDK', parents=[common])
    sub.add_parser('copy', help='Copy nuget package to the local source', parents=[common])
    sub.add_parser('clean', help='Clean the local source', parents=[common])
    sub.add_parser('all', help='Publish all targets', parents=[common])

    args = parser.parse_args()

    print(args)

    config = 'Debug' if getattr(args, 'debug', False) else 'Release'
    target = args.target if getattr(args, 'target', None) else 'core'

    print(target)
    arg_found = False

    if args.command in ('pack', 'all'):
        pack(config, target)
        arg_found = True
    if args.command in ('copy', 'all'):
        copy(target)
        arg_found = True
    if args.command in ('clean', 'all'):
        clean(target)
        arg_found = True

    if not arg_found:
        parser.print_help()
        return 1

    return 0

if __name__ == "__main__":
    main()