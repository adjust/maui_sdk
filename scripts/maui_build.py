#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import sys
from shutil import which

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ANDROID_BINDING_SUBMODULE_ROOT = os.path.join(ROOT, 'android')
IOS_BINDING_SUBMODULE_ROOT = os.path.join(ROOT, 'iOs')

ANDROID_CORE_BINDING_SUBMODULE_ROOT = os.path.join(ANDROID_BINDING_SUBMODULE_ROOT, 'AdjustSdk.AndroidBinding')
ANDROID_CORE_BINDING_CSPROJ = os.path.join(ANDROID_CORE_BINDING_SUBMODULE_ROOT, 'AdjustSdk.AndroidBinding.csproj')
IOS_CORE_BINDING_SUBMODULE_ROOT = os.path.join(IOS_BINDING_SUBMODULE_ROOT, 'AdjustSdk.iOSBinding')
IOS_CORE_BINDING_CSPROJ = os.path.join(IOS_CORE_BINDING_SUBMODULE_ROOT, 'AdjustSdk.iOSBinding.csproj')

ANDROID_TEST_BINDING_SUBMODULE_ROOT = os.path.join(ANDROID_BINDING_SUBMODULE_ROOT, 'TestLibrary.AndroidBinding')
ANDROID_TEST_BINDING_CSPROJ = os.path.join(ANDROID_TEST_BINDING_SUBMODULE_ROOT, 'TestLibrary.AndroidBinding.csproj')
IOS_TEST_BINDING_SUBMODULE_ROOT = os.path.join(IOS_BINDING_SUBMODULE_ROOT, 'TestLibrary.iOSBinding')
IOS_TEST_BINDING_CSPROJ = os.path.join(IOS_TEST_BINDING_SUBMODULE_ROOT, 'TestLibrary.iOSBinding.csproj')

ANDROID_OAID_BINDING_SUBMODULE_ROOT = os.path.join(ANDROID_BINDING_SUBMODULE_ROOT, 'AdjustOaid.AndroidBinding')
ANDROID_OAID_BINDING_CSPROJ = os.path.join(ANDROID_OAID_BINDING_SUBMODULE_ROOT, 'AdjustOaid.AndroidBinding.csproj')

ANDROID_META_REFERRER_BINDING_SUBMODULE_ROOT = os.path.join(ANDROID_BINDING_SUBMODULE_ROOT, 'AdjustMetaReferrer.AndroidBinding')
ANDROID_META_REFERRER_BINDING_CSPROJ = os.path.join(ANDROID_META_REFERRER_BINDING_SUBMODULE_ROOT, 'AdjustMetaReferrer.AndroidBinding.csproj')

ANDROID_GOOGLE_LVL_BINDING_SUBMODULE_ROOT = os.path.join(ANDROID_BINDING_SUBMODULE_ROOT, 'AdjustGoogleLVL.AndroidBinding')
ANDROID_GOOGLE_LVL_BINDING_CSPROJ = os.path.join(ANDROID_GOOGLE_LVL_BINDING_SUBMODULE_ROOT, 'AdjustGoogleLVL.AndroidBinding.csproj')

CORE_SDK_SUBMODULE_ROOT = os.path.join(ROOT, 'AdjustSdk')
CORE_SDK_CSPROJ = os.path.join(CORE_SDK_SUBMODULE_ROOT, 'AdjustSdk.csproj')

PLUGINS_SUBMODULE_ROOT = os.path.join(ROOT, 'plugins')

OAID_SDK_SUBMODULE_ROOT = os.path.join(PLUGINS_SUBMODULE_ROOT, 'AdjustOaid')
OAID_SDK_CSPROJ = os.path.join(OAID_SDK_SUBMODULE_ROOT, 'AdjustOaid.csproj')

META_REFERRER_SDK_SUBMODULE_ROOT = os.path.join(PLUGINS_SUBMODULE_ROOT, 'AdjustMetaReferrer')
META_REFERRER_SDK_CSPROJ = os.path.join(META_REFERRER_SDK_SUBMODULE_ROOT, 'AdjustMetaReferrer.csproj')

GOOGLE_LVL_SDK_SUBMODULE_ROOT = os.path.join(PLUGINS_SUBMODULE_ROOT, 'AdjustGoogleLVL')
GOOGLE_LVL_SDK_CSPROJ = os.path.join(GOOGLE_LVL_SDK_SUBMODULE_ROOT, 'AdjustGoogleLVL.csproj')

TESTAPP_SUBMODULE_ROOT = os.path.join(ROOT, 'testApp')
TESTAPP_CSPROJ = os.path.join(TESTAPP_SUBMODULE_ROOT, 'TestApp.csproj')

EXAMPLE_APP_SUBMODULE_ROOT = os.path.join(ROOT, 'ExampleApp')
EXAMPLE_APP_CSPROJ = os.path.join(EXAMPLE_APP_SUBMODULE_ROOT, 'ExampleApp.csproj')
EXAMPLE_APP_CSPROJ_NUGET = os.path.join(EXAMPLE_APP_SUBMODULE_ROOT, 'ExampleApp-Nuget.csproj')

BINDINGS = ['test', 'core', 'oaid', 'meta_referrer', 'google_lvl']
APPS = ['test', 'example']
SDKS = ['core', 'oaid', 'meta_referrer', 'google_lvl']
PLATFORMS = ['android', 'ios']

def removing(str_list: list[str], *args):
    for arg in args:
        if arg in str_list:
            str_list.remove(arg)
            return True
    return False

def has_none(from_list: list[str], in_list: list[str]) -> bool:
    return not any(arg in in_list for arg in from_list)

def run(cmd):
    print('> ' + ' '.join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)

def build_bindings(targets, config):
    no_bindings_target = has_none(BINDINGS, targets)
    if 'core' in targets or no_bindings_target:
        print('> Build SDK Core bindings')
        build_core_bindings(targets, config)
    if 'test' in targets or no_bindings_target:
        print('> Build Test bindings')
        build_test_bindings(targets, config)
    if 'oaid' in targets or no_bindings_target:
        print('> Build OAID bindings')
        build_oaid_bindings(targets, config)
    if 'meta_referrer' in targets or no_bindings_target:
        print('> Build Meta Referrer bindings')
        build_meta_referrer_bindings(targets, config)
    if 'google_lvl' in targets or no_bindings_target:
        print('> Build Google LVL bindings')
        build_google_lvl_bindings(targets, config)
def build_core_bindings(targets, config):
    no_platform_target = has_none(PLATFORMS, targets)
    if 'android' in targets or no_platform_target:
        print('> Building Android SDK Core binding')
        run(['dotnet', 'build', ANDROID_CORE_BINDING_CSPROJ, '--configuration', config])
    if 'ios' in targets or no_platform_target:
        print('> Building iOS SDK Core binding')
        run(['dotnet', 'build', IOS_CORE_BINDING_CSPROJ, '--configuration', config])
def build_test_bindings(targets, config):
    no_platform_target = has_none(PLATFORMS, targets)
    if 'android' in targets or no_platform_target:
        print('> Building Android Test binding')
        run(['dotnet', 'build', ANDROID_TEST_BINDING_CSPROJ, '--configuration', config])
    if 'ios' in targets or no_platform_target:
        print('> Building iOS Test binding')
        run(['dotnet', 'build', IOS_TEST_BINDING_CSPROJ, '--configuration', config])
def build_oaid_bindings(targets, config):
    print('> Building Android OAID binding')
    run(['dotnet', 'build', ANDROID_OAID_BINDING_CSPROJ, '--configuration', config])
def build_meta_referrer_bindings(targets, config):
    print('> Building Android Meta Referrer binding')
    run(['dotnet', 'build', ANDROID_META_REFERRER_BINDING_CSPROJ, '--configuration', config])
def build_google_lvl_bindings(targets, config):
    print('> Building Android Google LVL binding')
    run(['dotnet', 'build', ANDROID_GOOGLE_LVL_BINDING_CSPROJ, '--configuration', config])
def build_sdk(targets, config):
    no_sdk_target = has_none(SDKS, targets)
    if 'core' in targets or no_sdk_target:
        print('> Building Core SDK')
        run(['dotnet', 'build', CORE_SDK_CSPROJ, '--configuration', config])
    if 'oaid' in targets or no_sdk_target:
        print('> Building OAID SDK plugin')
        run(['dotnet', 'build', OAID_SDK_CSPROJ, '--configuration', config])
    if 'meta_referrer' in targets or no_sdk_target:
        print('> Building Meta Referrer SDK plugin')
        run(['dotnet', 'build', META_REFERRER_SDK_CSPROJ, '--configuration', config])
    if 'google_lvl' in targets or no_sdk_target:
        print('> Building Google LVL SDK plugin')
        run(['dotnet', 'build', GOOGLE_LVL_SDK_CSPROJ, '--configuration', config])
def build_apps(targets, config):
    no_app_target = has_none(APPS, targets)
    if 'example' in targets or no_app_target:
        build_example(targets, config)
    if 'test' in targets or no_app_target:
        build_test(config)
def build_test(config):
    print('> Building Test App')
    run(['dotnet', 'build', TESTAPP_CSPROJ, '--configuration', config])
def build_example(targets, config):
    print('> Building Example')
    if 'nuget' in targets:
        run(['dotnet', 'build', EXAMPLE_APP_CSPROJ_NUGET, '--configuration', config])
    else:
        run(['dotnet', 'build', EXAMPLE_APP_CSPROJ, '--configuration', config])

def build_all(targets, config):
    build_bindings(targets, config)
    build_sdk(targets, config)
    build_apps(targets, config)


def main(argv=None):
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--release', action='store_true', help='Build in Release (default: Debug)')
    common.add_argument(
        'targets',
        nargs='*',
        choices=['bindings', 'sdk', 'apps',
         'test', 'example', 'nuget',
         'android', 'ios',
          'core', 'oaid', 'meta_referrer', 'google_lvl'],
        help='Which targets (can specify multiple)'
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
    targets = args.targets # if getattr(args, 'targets', None) else ['all']

    arg_found = False

    print('targets: %s' % targets)

    if args.command in ('clean', 'clean_all', 'clean_bindings', 'clean_sdk', 'clean_apps'):
        clean(args.command, targets[:], args.dry)
        arg_found = True
    if args.command in ('bindings', 'clean_bindings'):
        build_bindings(targets[:], config)
        arg_found = True
    if args.command in ('sdk', 'clean_sdk'):
        build_sdk(targets[:], config)
        arg_found = True
    if args.command in ('apps', 'clean_apps'):
        build_apps(targets[:], config)
        arg_found = True
    if args.command in ('all', 'clean_all'):
        build_all(targets[:], config)
        arg_found = True

    if not arg_found:
        parser.print_help()
        return 1

    return 0

ARTIFACTS_OUTPUT_DIR = os.path.join(ROOT, '.artifacts')

ARTIFACTS_CORE_BINDING_ANDROID_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, 'AdjustSdk.AndroidBinding')
ARTIFACTS_CORE_BINDING_IOS_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, 'AdjustSdk.iOSBinding')
ARTIFACTS_TEST_BINDING_ANDROID_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, 'TestLibrary.AndroidBinding')
ARTIFACTS_TEST_BINDING_IOS_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, 'TestLibrary.iOSBinding')
ARTIFACTS_OAID_BINDING_ANDROID_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, 'AdjustOaid.AndroidBinding')
ARTIFACTS_META_REFERRER_BINDING_ANDROID_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, 'AdjustMetaReferrer.AndroidBinding')
ARTIFACTS_GOOGLE_LVL_BINDING_ANDROID_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, 'AdjustGoogleLVL.AndroidBinding')

ARTIFACTS_CORE_SDK_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, 'AdjustSdk')
ARTIFACTS_OAID_SDK_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, 'AdjustOaid')
ARTIFACTS_META_REFERRER_SDK_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, 'AdjustMetaReferrer')
ARTIFACTS_GOOGLE_LVL_SDK_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, 'AdjustGoogleLVL')
ARTIFACTS_TEST_APP_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, 'TestApp')
ARTIFACTS_EXAMPLE_APP_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, 'ExampleApp')

def clean(command: str, targets: list[str], dry: bool):
    if command == 'clean_all' or (command == 'clean' and has_none(targets, ('bindings', 'sdk', 'apps'))):
        clean_target(dry, ARTIFACTS_OUTPUT_DIR)
    if command == 'clean_bindings' or removing(targets, 'bindings'):
        clean_bindings(targets, dry)
    if command == 'clean_sdk' or removing(targets, 'sdk'):
        clean_sdk(targets, dry)
    if command == 'clean_apps' or removing(targets, 'apps'):
        clean_apps(targets, dry)

def clean_bindings(targets, dry):
    no_bindings_target = has_none(BINDINGS,targets)
    if 'test' in targets or no_bindings_target:
        clean_test_bindings(targets, dry)
    if 'core' in targets or no_bindings_target:
        clean_core_bindings(targets, dry)
    if 'oaid' in targets or no_bindings_target:
        clean_oaid_bindings(targets, dry)
    if 'meta_referrer' in targets or no_bindings_target:
        clean_meta_referrer_bindings(targets, dry)
    if 'google_lvl' in targets or no_bindings_target:
        clean_google_lvl_bindings(targets, dry)

def clean_sdk(targets, dry):
    no_sdk_target = has_none(SDKS, targets)
    if 'core' in targets or no_sdk_target:
        clean_target(dry, ARTIFACTS_CORE_SDK_OUTPUT_DIR)
    if 'oaid' in targets or no_sdk_target:
        clean_target(dry, ARTIFACTS_OAID_SDK_OUTPUT_DIR)
    if 'meta_referrer' in targets or no_sdk_target:
        clean_target(dry, ARTIFACTS_META_REFERRER_SDK_OUTPUT_DIR)
    if 'google_lvl' in targets or no_sdk_target:
        clean_target(dry, ARTIFACTS_GOOGLE_LVL_SDK_OUTPUT_DIR)

def clean_apps(targets, dry):
    no_app_target = has_none(APPS, targets)
    if 'test' in targets or no_app_target:
        clean_target(dry, ARTIFACTS_TEST_APP_OUTPUT_DIR)
    if 'example' in targets or no_app_target:
        clean_target(dry, ARTIFACTS_EXAMPLE_APP_OUTPUT_DIR)

def clean_test_bindings(targets, dry):
    no_platform_target = has_none(PLATFORMS, targets)
    if 'ios' in targets or no_platform_target:
        clean_target(dry, ARTIFACTS_TEST_BINDING_IOS_OUTPUT_DIR)
    if 'android' in targets or no_platform_target:
        clean_target(dry, ARTIFACTS_TEST_BINDING_ANDROID_OUTPUT_DIR)

def clean_core_bindings(targets, dry):
    no_platform_target = has_none(PLATFORMS, targets)
    if 'ios' in targets or no_platform_target:
        clean_target(dry, ARTIFACTS_CORE_BINDING_IOS_OUTPUT_DIR)
    if 'android' in targets or no_platform_target:
        clean_target(dry, ARTIFACTS_CORE_BINDING_ANDROID_OUTPUT_DIR)

def clean_oaid_bindings(targets, dry):
    clean_target(dry, ARTIFACTS_OAID_BINDING_ANDROID_OUTPUT_DIR)

def clean_meta_referrer_bindings(targets, dry):
    clean_target(dry, ARTIFACTS_META_REFERRER_BINDING_ANDROID_OUTPUT_DIR)

def clean_google_lvl_bindings(targets, dry):
    clean_target(dry, ARTIFACTS_GOOGLE_LVL_BINDING_ANDROID_OUTPUT_DIR)

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

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
