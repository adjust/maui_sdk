#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import sys
from shutil import which

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ANDROID_SDK_BINDING = os.path.join(ROOT, 'android', 'AdjustSdk.AndroidBinding', 'AdjustSdk.AndroidBinding.csproj')
IOS_SDK_BINDING = os.path.join(ROOT, 'iOs', 'AdjustSdk.iOSBinding', 'AdjustSdk.iOSBinding.csproj')
SDK_CSPROJ = os.path.join(ROOT, 'AdjustSdk', 'AdjustSdk.csproj')

ANDROID_TESTAPP_BINDING = os.path.join(ROOT, 'android', 'TestLibrary.AndroidBinding', 'TestLibrary.AndroidBinding.csproj')
IOS_TESTAPP_BINDING = os.path.join(ROOT, 'iOs', 'TestLibrary.iOSBinding', 'TestLibrary.iOSBinding.csproj')
TESTAPP_CSPROJ = os.path.join(ROOT, 'testApp', 'TestApp.csproj')

EXAMPLE_APP_CSPROJ = os.path.join(ROOT, 'ExampleApp', 'ExampleApp.csproj')

def run(cmd):
    print('> ' + ' '.join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)

def build_bindings(targets, config):
    if 'sdk' in targets or 'all' in targets:
        build_sdk_bindings(targets, config)
    if 'testapp' in targets or 'all' in targets:
        build_testapp_bindings(targets, config)
def build_sdk_bindings(targets, config):
    if 'android' in targets or 'all' in targets:
        print('> Building Android SDK binding')
        run(['dotnet', 'build', ANDROID_SDK_BINDING, '--configuration', config])
    if 'ios' in targets or 'all' in targets:
        print('> Building iOS SDK binding')
        run(['dotnet', 'build', IOS_SDK_BINDING, '--configuration', config])
def build_testapp_bindings(targets, config):
    if 'android' in targets or 'all' in targets:
        print('> Building Android TestApp binding')
        run(['dotnet', 'build', ANDROID_TESTAPP_BINDING, '--configuration', config])
    if 'ios' in targets or 'all' in targets:
        print('> Building iOS TestApp binding')
        run(['dotnet', 'build', IOS_TESTAPP_BINDING, '--configuration', config])

def build_sdk(targets, config):
    build_sdk_bindings(targets, config)
    print('> Building SDK')
    run(['dotnet', 'build', SDK_CSPROJ, '--configuration', config])
def build_testapp(targets, config):
    build_testapp_bindings(targets, config)
    print('> Building TestApp')
    run(['dotnet', 'build', TESTAPP_CSPROJ, '--configuration', config])
def build_example(targets, config):
    print('> Building ExampleApp')
    run(['dotnet', 'build', EXAMPLE_APP_CSPROJ, '--configuration', config])
def build_all(targets, config):
    if 'sdk' in targets or 'all' in targets:
        build_sdk(targets, config)
    if 'testapp' in targets or 'all' in targets:
        build_testapp(targets, config)
    if 'example' in targets or 'all' in targets:
        build_example(targets, config)

def find_bin_obj_dirs_cmd():
    return ['find', ROOT, '-type', 'd', '(', '-name', 'bin', '-o', '-name', 'obj', ')', '-prune']
def clean(dry):
    if dry:
        print('> dry-run: listing bin/ and obj/ directories under $ROOT')
        subprocess.run(find_bin_obj_dirs_cmd() + ['-print'])
        return
    if which('trash'):
        print('> trash bin/ and obj/ directories under $ROOT')
        subprocess.run(find_bin_obj_dirs_cmd() + ['-exec', 'trash', '{}', '+'])
    else:
        print('> rm -rf bin/ and obj/ directories under $ROOT')
        subprocess.run(find_bin_obj_dirs_cmd() + ['-exec', 'rm', '-rf', '{}', '+'])

def main(argv=None):
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--release', action='store_true', help='Build in Release (default: Debug)')
    common.add_argument(
        'targets',
        nargs='*',
        choices=['sdk', 'testapp', 'example', 'android', 'ios', 'all'],
        help='Which targets (can specify multiple, default: all)'
    )
    common.add_argument('--dry', action='store_true', default=False, help='Perform a dry run (list bin/obj dirs only)')

    parser = argparse.ArgumentParser(description='Python3 build tool for Adjust Maui repo')
    sub = parser.add_subparsers(dest='command')
    sub.add_parser('bindings', help='Build specified bindings', parents=[common])
    sub.add_parser('build', help='Build specified targets', parents=[common])
    sub.add_parser('clean', help='Clean build artifacts (bin/obj dirs)', parents=[common])
    sub.add_parser('clean_bindings', help='Clean and build bindings', parents=[common])
    sub.add_parser('clean_build', help='Clean and build targets', parents=[common])

    args = parser.parse_args(argv)

    # Derive config and default targets
    config = 'Release' if getattr(args, 'release', False) else 'Debug'
    targets = args.targets if getattr(args, 'targets', None) else ['all']

    arg_found = False

    if args.command in ('clean', 'clean_bindings', 'clean_build'):
        clean(args.dry)
        arg_found = True
    if args.command in ('bindings', 'clean_bindings'):
        build_bindings(targets, config)
        arg_found = True
    if args.command in ('build', 'clean_build'):
        build_all(targets, config)
        arg_found = True

    if not arg_found:
        parser.print_help()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
