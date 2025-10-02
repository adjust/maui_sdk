#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import sys
from shutil import which

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ANDROID_BINDING_SUBMODULE_ROOT = os.path.join(ROOT, 'android')
ANDROID_SDK_BINDING_SUBMODULE_ROOT = os.path.join(ANDROID_BINDING_SUBMODULE_ROOT, 'AdjustSdk.AndroidBinding')
ANDROID_SDK_BINDING_CSPROJ = os.path.join(ANDROID_SDK_BINDING_SUBMODULE_ROOT, 'AdjustSdk.AndroidBinding.csproj')

IOS_BINDING_SUBMODULE_ROOT = os.path.join(ROOT, 'iOs')
IOS_SDK_BINDING_SUBMODULE_ROOT = os.path.join(IOS_BINDING_SUBMODULE_ROOT, 'AdjustSdk.iOSBinding')
IOS_SDK_BINDING_CSPROJ = os.path.join(IOS_SDK_BINDING_SUBMODULE_ROOT, 'AdjustSdk.iOSBinding.csproj')

ANDROID_TESTAPP_BINDING_SUBMODULE_ROOT = os.path.join(ANDROID_BINDING_SUBMODULE_ROOT, 'TestLibrary.AndroidBinding')
ANDROID_TESTAPP_BINDING_CSPROJ = os.path.join(ANDROID_TESTAPP_BINDING_SUBMODULE_ROOT, 'TestLibrary.AndroidBinding.csproj')

IOS_TESTAPP_BINDING_SUBMODULE_ROOT = os.path.join(IOS_BINDING_SUBMODULE_ROOT, 'TestLibrary.iOSBinding')
IOS_TESTAPP_BINDING_CSPROJ = os.path.join(IOS_TESTAPP_BINDING_SUBMODULE_ROOT, 'TestLibrary.iOSBinding.csproj')


SDK_SUBMODULE_ROOT = os.path.join(ROOT, 'AdjustSdk')
SDK_CSPROJ = os.path.join(SDK_SUBMODULE_ROOT, 'AdjustSdk.csproj')

TESTAPP_SUBMODULE_ROOT = os.path.join(ROOT, 'testApp')
TESTAPP_CSPROJ = os.path.join(TESTAPP_SUBMODULE_ROOT, 'TestApp.csproj')

EXAMPLE_APP_SUBMODULE_ROOT = os.path.join(ROOT, 'ExampleApp')
EXAMPLE_APP_CSPROJ = os.path.join(EXAMPLE_APP_SUBMODULE_ROOT, 'ExampleApp.csproj')
EXAMPLE_APP_CSPROJ_NUGET = os.path.join(EXAMPLE_APP_SUBMODULE_ROOT, 'ExampleApp-Nuget.csproj')

def run(cmd):
    print('> ' + ' '.join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)

def build_bindings(targets, config):
    if 'test' not in targets:
        print('> Build SDK bindings')
        build_sdk_bindings(targets, config)
    if 'sdk' not in targets:
        print('> Build TestApp bindings')
        build_testapp_bindings(targets, config)
def build_sdk_bindings(targets, config):
    if 'ios' not in targets:
        print('> Building Android SDK binding')
        run(['dotnet', 'build', ANDROID_SDK_BINDING_CSPROJ, '--configuration', config])
    if 'android' not in targets:
        print('> Building iOS SDK binding')
        run(['dotnet', 'build', IOS_SDK_BINDING_CSPROJ, '--configuration', config])
def build_testapp_bindings(targets, config):
    if 'ios' not in targets:
        print('> Building Android TestApp binding')
        run(['dotnet', 'build', ANDROID_TESTAPP_BINDING_CSPROJ, '--configuration', config])
    if 'android' not in targets:
        print('> Building iOS TestApp binding')
        run(['dotnet', 'build', IOS_TESTAPP_BINDING_CSPROJ, '--configuration', config])

def build_sdk(config):
    print('> Building SDK')
    run(['dotnet', 'build', SDK_CSPROJ, '--configuration', config])

def build_apps(targets, config):
    if 'example' not in targets:
        build_testapp(config)
    if 'test' not in targets:
        build_example(targets, config)
def build_testapp(config):
    print('> Building TestApp')
    run(['dotnet', 'build', TESTAPP_CSPROJ, '--configuration', config])
def build_example(targets, config):
    print('> Building ExampleApp')
    if 'nuget' in targets:
        run(['dotnet', 'build', EXAMPLE_APP_CSPROJ_NUGET, '--configuration', config])
    else:
        run(['dotnet', 'build', EXAMPLE_APP_CSPROJ, '--configuration', config])

def build_all(targets, config):
    build_bindings(targets, config)
    build_sdk(config)
    build_apps(targets, config)

    """
        if 'sdk' in targets or 'all' in targets:
            build_sdk_bindings(targets, config)
            build_sdk(targets, config)
        if 'test' in targets or 'all' in targets:
            build_testapp_bindings(targets, config)
            build_testapp(config)
        if 'example' in targets or 'all' in targets:
            build_example(targets, config)
    """

def clean(targets, dry):
    if 'all' in targets:
        clean_target(dry, ROOT)
    if 'bindings' in targets:
        clean_bindings(targets, dry)
    if 'sdk' in targets:
        clean_target(dry, SDK_SUBMODULE_ROOT)
    if 'test' in targets:
        clean_target(dry, TESTAPP_SUBMODULE_ROOT)
    if 'example' in targets:
        clean_target(dry, EXAMPLE_APP_SUBMODULE_ROOT)

def clean_bindings(targets, dry):
    if 'sdk' not in targets:
        clean_testapp_bindings(targets, dry)
    if 'test' not in targets:
        clean_sdk_bindings(targets, dry)

def clean_testapp_bindings(targets, dry):
    if 'android' not in targets:
        clean_target(dry, IOS_TESTAPP_BINDING_SUBMODULE_ROOT)
    if 'ios' not in targets:
        clean_target(dry, ANDROID_TESTAPP_BINDING_SUBMODULE_ROOT)

def clean_sdk_bindings(targets, dry):
    if 'android' not in targets:
        clean_target(dry, IOS_SDK_BINDING_SUBMODULE_ROOT)
    if 'ios' not in targets:
        clean_target(dry, ANDROID_SDK_BINDING_SUBMODULE_ROOT)

def find_bin_obj_dirs_cmd(subdir=None):
    search_root = os.path.join(ROOT, subdir) if subdir else ROOT
    return ['find', search_root, '-type', 'd', '(', '-name', 'bin', '-o', '-name', 'obj', ')', '-prune']

def clean_target(dry, subdir=None):
    if dry:
        print('> dry-run: listing bin/ and obj/ directories under %s' % subdir)
        subprocess.run(find_bin_obj_dirs_cmd(subdir) + ['-print'])
        return
    if which('trash'):
        print('> trash bin/ and obj/ directories under %s' % subdir)
        subprocess.run(find_bin_obj_dirs_cmd(subdir) + ['-exec', 'trash', '{}', '+'])
    else:
        print('> rm -rf bin/ and obj/ directories under %s' % subdir)
        subprocess.run(find_bin_obj_dirs_cmd(subdir) + ['-exec', 'rm', '-rf', '{}', '+'])

def main(argv=None):
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--release', action='store_true', help='Build in Release (default: Debug)')
    common.add_argument(
        'targets',
        nargs='*',
        choices=['sdk', 'test', 'example', 'nuget', 'android', 'ios', 'bindings', 'all'],
        help='Which targets (can specify multiple, default: all)'
    )
    common.add_argument('--dry', action='store_true', default=False, help='Perform a dry run (list bin/obj dirs only)')

    parser = argparse.ArgumentParser(description='Python3 build tool for Adjust Maui repo')
    sub = parser.add_subparsers(dest='command')
    sub.add_parser('clean', help='Clean build artifacts (bin/obj dirs)', parents=[common])
    sub.add_parser('clean_bindings', help='Clean and build bindings', parents=[common])
    sub.add_parser('clean_sdk', help='Clean and build SDK', parents=[common])
    sub.add_parser('clean_apps', help='Clean and build apps', parents=[common])
    sub.add_parser('clean_all', help='Clean and build all targets', parents=[common])

    sub.add_parser('bindings', help='Build specified bindings', parents=[common])
    sub.add_parser('sdk', help='Build maui sdk', parents=[common])
    sub.add_parser('apps', help='Build maui apps', parents=[common])

    args = parser.parse_args(argv)

    # Derive config and default targets
    config = 'Release' if getattr(args, 'release', False) else 'Debug'
    targets = args.targets if getattr(args, 'targets', None) else ['all']

    arg_found = False

    print('targets: %s' % targets)

    if args.command in ('clean', 'clean_bindings', 'clean_sdk', 'clean_apps', 'clean_all'):
        clean(targets, args.dry)
        arg_found = True
    if args.command in ('bindings', 'clean_bindings'):
        build_bindings(targets, config)
        arg_found = True
    if args.command in ('sdk', 'clean_sdk'):
        build_sdk(config)
        arg_found = True
    if args.command in ('apps', 'clean_apps'):
        build_apps(targets, config)
        arg_found = True
    if args.command in ('all', 'clean_all'):
        build_all(targets, config)
        arg_found = True

    if not arg_found:
        parser.print_help()
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
