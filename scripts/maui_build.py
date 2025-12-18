#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import sys
import time
import pty
import select
from shutil import which
import json

CORE_BINDING_ANDROID_NAME = 'AdjustSdk.AndroidBinding'
CORE_BINDING_IOS_NAME = 'AdjustSdk.iOSBinding'
TEST_BINDING_ANDROID_NAME = 'TestLibrary.AndroidBinding'
TEST_BINDING_IOS_NAME = 'TestLibrary.iOSBinding'
OAID_BINDING_ANDROID_NAME = 'AdjustOaid.AndroidBinding'
META_REFERRER_BINDING_ANDROID_NAME = 'AdjustMetaReferrer.AndroidBinding'
GOOGLE_LVL_BINDING_ANDROID_NAME = 'AdjustGoogleLVL.AndroidBinding'

CORE_SDK_NAME = 'AdjustSdk'
OAID_SDK_NAME = 'AdjustOaid'
META_REFERRER_SDK_NAME = 'AdjustMetaReferrer'
GOOGLE_LVL_SDK_NAME = 'AdjustGoogleLVL'
TEST_APP_NAME = 'TestApp'
EXAMPLE_APP_NAME = 'ExampleApp'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ANDROID_BINDING_SUBMODULE_ROOT = os.path.join(ROOT, 'android')
IOS_BINDING_SUBMODULE_ROOT = os.path.join(ROOT, 'iOs')

ANDROID_CORE_BINDING_SUBMODULE_ROOT = os.path.join(ANDROID_BINDING_SUBMODULE_ROOT, CORE_BINDING_ANDROID_NAME)
ANDROID_CORE_BINDING_CSPROJ = os.path.join(ANDROID_CORE_BINDING_SUBMODULE_ROOT, f'{CORE_BINDING_ANDROID_NAME}.csproj')
IOS_CORE_BINDING_SUBMODULE_ROOT = os.path.join(IOS_BINDING_SUBMODULE_ROOT, CORE_BINDING_IOS_NAME)
IOS_CORE_BINDING_CSPROJ = os.path.join(IOS_CORE_BINDING_SUBMODULE_ROOT, f'{CORE_BINDING_IOS_NAME}.csproj')

ANDROID_TEST_BINDING_SUBMODULE_ROOT = os.path.join(ANDROID_BINDING_SUBMODULE_ROOT, TEST_BINDING_ANDROID_NAME)
ANDROID_TEST_BINDING_CSPROJ = os.path.join(ANDROID_TEST_BINDING_SUBMODULE_ROOT, f'{TEST_BINDING_ANDROID_NAME}.csproj')
IOS_TEST_BINDING_SUBMODULE_ROOT = os.path.join(IOS_BINDING_SUBMODULE_ROOT, TEST_BINDING_IOS_NAME)
IOS_TEST_BINDING_CSPROJ = os.path.join(IOS_TEST_BINDING_SUBMODULE_ROOT, f'{TEST_BINDING_IOS_NAME}.csproj')

ANDROID_OAID_BINDING_SUBMODULE_ROOT = os.path.join(ANDROID_BINDING_SUBMODULE_ROOT, OAID_BINDING_ANDROID_NAME)
ANDROID_OAID_BINDING_CSPROJ = os.path.join(ANDROID_OAID_BINDING_SUBMODULE_ROOT, f'{OAID_BINDING_ANDROID_NAME}.csproj')

ANDROID_META_REFERRER_BINDING_SUBMODULE_ROOT = os.path.join(ANDROID_BINDING_SUBMODULE_ROOT, META_REFERRER_BINDING_ANDROID_NAME)
ANDROID_META_REFERRER_BINDING_CSPROJ = os.path.join(ANDROID_META_REFERRER_BINDING_SUBMODULE_ROOT, f'{META_REFERRER_BINDING_ANDROID_NAME}.csproj')

ANDROID_GOOGLE_LVL_BINDING_SUBMODULE_ROOT = os.path.join(ANDROID_BINDING_SUBMODULE_ROOT, GOOGLE_LVL_BINDING_ANDROID_NAME)
ANDROID_GOOGLE_LVL_BINDING_CSPROJ = os.path.join(ANDROID_GOOGLE_LVL_BINDING_SUBMODULE_ROOT, f'{GOOGLE_LVL_BINDING_ANDROID_NAME}.csproj')

CORE_SDK_SUBMODULE_ROOT = os.path.join(ROOT, CORE_SDK_NAME)
CORE_SDK_CSPROJ = os.path.join(CORE_SDK_SUBMODULE_ROOT, f'{CORE_SDK_NAME}.csproj')

PLUGINS_SUBMODULE_ROOT = os.path.join(ROOT, 'plugins')

OAID_SDK_SUBMODULE_ROOT = os.path.join(PLUGINS_SUBMODULE_ROOT, OAID_SDK_NAME)
OAID_SDK_CSPROJ = os.path.join(OAID_SDK_SUBMODULE_ROOT, f'{OAID_SDK_NAME}.csproj')

META_REFERRER_SDK_SUBMODULE_ROOT = os.path.join(PLUGINS_SUBMODULE_ROOT, META_REFERRER_SDK_NAME)
META_REFERRER_SDK_CSPROJ = os.path.join(META_REFERRER_SDK_SUBMODULE_ROOT, f'{META_REFERRER_SDK_NAME}.csproj')

GOOGLE_LVL_SDK_SUBMODULE_ROOT = os.path.join(PLUGINS_SUBMODULE_ROOT, GOOGLE_LVL_SDK_NAME)
GOOGLE_LVL_SDK_CSPROJ = os.path.join(GOOGLE_LVL_SDK_SUBMODULE_ROOT, f'{GOOGLE_LVL_SDK_NAME}.csproj')

TESTAPP_SUBMODULE_ROOT = os.path.join(ROOT, 'testApp')
TESTAPP_CSPROJ = os.path.join(TESTAPP_SUBMODULE_ROOT, f'{TEST_APP_NAME}.csproj')
TESTAPP_CSPROJ_NET10 = os.path.join(TESTAPP_SUBMODULE_ROOT, f'{TEST_APP_NAME}-Net10.csproj')

EXAMPLE_APP_SUBMODULE_ROOT = os.path.join(ROOT, 'ExampleApp')
EXAMPLE_APP_CSPROJ = os.path.join(EXAMPLE_APP_SUBMODULE_ROOT, f'{EXAMPLE_APP_NAME}.csproj')
EXAMPLE_APP_CSPROJ_NET10 = os.path.join(EXAMPLE_APP_SUBMODULE_ROOT, f'{EXAMPLE_APP_NAME}-Net10.csproj')
EXAMPLE_APP_CSPROJ_NUGET = os.path.join(EXAMPLE_APP_SUBMODULE_ROOT, f'{EXAMPLE_APP_NAME}-Nuget.csproj')
EXAMPLE_APP_CSPROJ_NUGET_NET10 = os.path.join(EXAMPLE_APP_SUBMODULE_ROOT, f'{EXAMPLE_APP_NAME}-Nuget-Net10.csproj')

BINDINGS = ['test', 'core', 'oaid', 'meta_referrer', 'google_lvl', 'plugins']
APPS = ['test', 'example', 'example-nuget']
SDKS = ['core', 'oaid', 'meta_referrer', 'google_lvl', 'plugins']
PLATFORMS = ['android', 'ios']
NET_VERSIONS = ['net8', 'net10']

def set_net_version(net_version: bool):
    if net_version == 'net8':
        version = "8.0.402"
    else:
        version = "10.0.101"
    global_json = {"sdk": {"version": version, "rollForward": "latestFeature"}}
    with open(os.path.join(ROOT, "global.json"), "w") as f:
        json.dump(global_json, f, indent=2)

def removing(str_list: list[str], *args):
    for arg in args:
        if arg in str_list:
            str_list.remove(arg)
            return True
    return False

def has_none(from_list: list[str], in_list: list[str]) -> bool:
    return not any(arg in in_list for arg in from_list)

def shutdown_build_server():
    """Shutdown dotnet build server to release file locks"""
    print('> Shutting down dotnet build server...')
    subprocess.run(['dotnet', 'build-server', 'shutdown'],
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    time.sleep(0.5)  # Give it a moment to fully shutdown

def run(cmd, retry_on_file_lock=True, max_retries=3):
    """Run a command with optional retry logic for file locking errors"""
    print('> ' + ' '.join(cmd))

    for attempt in range(max_retries):
        # Use a pseudo-terminal to preserve colors
        master_fd, slave_fd = pty.openpty()

        try:
            process = subprocess.Popen(
                cmd,
                stdout=slave_fd,
                stderr=slave_fd,
                close_fds=True
            )

            os.close(slave_fd)  # Close slave in parent process

            # Capture output while displaying it in real-time
            output_lines = []
            while True:
                try:
                    # Check if there's data to read
                    readable, _, _ = select.select([master_fd], [], [], 0.1)
                    if readable:
                        try:
                            data = os.read(master_fd, 1024)
                            if not data:
                                break
                            text = data.decode('utf-8', errors='replace')
                            sys.stdout.write(text)
                            sys.stdout.flush()
                            output_lines.append(text)
                        except OSError:
                            break

                    # Check if process has finished
                    if process.poll() is not None:
                        # Read any remaining data
                        try:
                            while True:
                                data = os.read(master_fd, 1024)
                                if not data:
                                    break
                                text = data.decode('utf-8', errors='replace')
                                sys.stdout.write(text)
                                sys.stdout.flush()
                                output_lines.append(text)
                        except OSError:
                            pass
                        break
                except KeyboardInterrupt:
                    process.terminate()
                    raise

            return_code = process.wait()
        finally:
            os.close(master_fd)

        if return_code == 0:
            # Success
            return

        # On failure, check if it's a file locking error
        output = ''.join(output_lines)
        is_file_lock_error = any(err in output for err in [
            'is being used by another process',
            'Renaming temporary file failed',
            'No such file or directory',
            'XARLP7024',
            'XARLP7000'
        ])

        if retry_on_file_lock and is_file_lock_error and attempt < max_retries - 1:
            print(f'\n > File locking error detected (attempt {attempt + 1}/{max_retries}). Retrying...\n')
            shutdown_build_server()
            time.sleep(2)  # Wait for file handles to be released
            continue

        # Either not a file lock error, or we've exhausted retries
        sys.exit(return_code)

def build_with_delay(csproj, config, delay=1.0):
    """Run a command and add a delay afterwards to prevent race conditions"""
    if config == 'DebugAndRelease':
        run_with_delay(['dotnet', 'build', csproj, '--configuration', 'Debug'], delay)
        run_with_delay(['dotnet', 'build', csproj, '--configuration', 'Release'], delay)
    else:
        run_with_delay(['dotnet', 'build', csproj, '--configuration', config], delay)
def run_with_delay(cmd, delay):
    run(cmd)
    time.sleep(delay)


def build_bindings(targets):
    if 'debug' in targets:
        config = 'Debug'
    elif 'release' in targets:
        config = 'Release'
    else:
        config = 'DebugAndRelease'

    if 'net10' in targets:
        build_bindings_specific(targets, config, 'net10')
    elif 'net8' in targets:
        build_bindings_specific(targets, config, 'net8')
    else:
        build_bindings_specific(targets, config, 'net8')
        build_bindings_specific(targets, config, 'net10')
def build_bindings_specific(targets, config, net_version):
    set_net_version(net_version)
    shutdown_build_server()  # Start with clean state
    no_bindings_target = has_none(BINDINGS, targets)
    if 'core' in targets or no_bindings_target:
        print('> Build SDK Core bindings')
        build_core_bindings(targets, config)
    if 'test' in targets or no_bindings_target:
        print('> Build Test bindings')
        build_test_bindings(targets, config)
    if 'oaid' in targets or 'plugins' in targets or no_bindings_target:
        print('> Build OAID bindings')
        build_oaid_bindings(targets, config)
    if 'meta_referrer' in targets or 'plugins' in targets or no_bindings_target:
        print('> Build Meta Referrer bindings')
        build_meta_referrer_bindings(targets, config)
    if 'google_lvl' in targets or 'plugins' in targets or no_bindings_target:
        print('> Build Google LVL bindings')
        build_google_lvl_bindings(targets, config)
def build_core_bindings(targets, config):
    no_platform_target = has_none(PLATFORMS, targets)
    if 'android' in targets or no_platform_target:
        print('> Building Android SDK Core binding')
        build_with_delay(ANDROID_CORE_BINDING_CSPROJ, config)
    if 'ios' in targets or no_platform_target:
        print('> Building iOS SDK Core binding')
        build_with_delay(IOS_CORE_BINDING_CSPROJ, config)
def build_test_bindings(targets, config):
    no_platform_target = has_none(PLATFORMS, targets)
    if 'android' in targets or no_platform_target:
        print('> Building Android Test binding')
        build_with_delay(ANDROID_TEST_BINDING_CSPROJ, config)
    if 'ios' in targets or no_platform_target:
        print('> Building iOS Test binding')
        build_with_delay(IOS_TEST_BINDING_CSPROJ, config)
def build_oaid_bindings(targets, config):
    print('> Building Android OAID binding')
    build_with_delay(ANDROID_OAID_BINDING_CSPROJ, config)
def build_meta_referrer_bindings(targets, config):
    print('> Building Android Meta Referrer binding')
    build_with_delay(ANDROID_META_REFERRER_BINDING_CSPROJ, config)
def build_google_lvl_bindings(targets, config):
    print('> Building Android Google LVL binding')
    build_with_delay(ANDROID_GOOGLE_LVL_BINDING_CSPROJ, config)

def build_sdk(targets):
    if 'debug' in targets:
        config = 'Debug'
    elif 'release' in targets:
        config = 'Release'
    else:
        config = 'DebugAndRelease'

    if 'net10' in targets:
        build_sdk_specific(targets, config, 'net10')
    elif 'net8' in targets:
        build_sdk_specific(targets, config, 'net8')
    else:
        build_sdk_specific(targets, config, 'net8')
        build_sdk_specific(targets, config, 'net10')
def build_sdk_specific(targets, config, net_version):
    set_net_version(net_version)
    shutdown_build_server()  # Start with clean state
    no_sdk_target = has_none(SDKS, targets)
    if 'core' in targets or no_sdk_target:
        print('> Building Core SDK')
        build_with_delay(CORE_SDK_CSPROJ, config)
    if 'oaid' in targets or 'plugins' in targets or no_sdk_target:
        print('> Building OAID SDK plugin')
        build_with_delay(OAID_SDK_CSPROJ, config)
    if 'meta_referrer' in targets or 'plugins' in targets or no_sdk_target:
        print('> Building Meta Referrer SDK plugin')
        build_with_delay(META_REFERRER_SDK_CSPROJ, config)
    if 'google_lvl' in targets or 'plugins' in targets or no_sdk_target:
        print('> Building Google LVL SDK plugin')
        build_with_delay(GOOGLE_LVL_SDK_CSPROJ, config)

def build_apps(targets):
    config = 'Debug'

    if 'net10' in targets:
        build_apps_specific(targets, config, 'net10')
    elif 'net8' in targets:
        build_apps_specific(targets, config, 'net8')
    else:
        build_apps_specific(targets, config, 'net8')
        build_apps_specific(targets, config, 'net10')
def build_apps_specific(targets, config, net_version):
    set_net_version(net_version)
    shutdown_build_server()  # Start with clean state
    no_app_target = has_none(APPS, targets)
    if 'example' in targets or no_app_target:
        build_example(targets, config, net_version)
    if 'example-nuget' in targets or no_app_target:
        build_example_nuget(targets, config, net_version)
    if 'test' in targets or no_app_target:
        build_test(targets, config, net_version)
def build_test(targets, config, net_version):
    if 'net10' in net_version:
        print('> Building Test App Net10')
        build_with_delay(TESTAPP_CSPROJ_NET10, config)
    else:
        print('> Building Test App Net8')
        build_with_delay(TESTAPP_CSPROJ, config)
def build_example(targets, config, net_version):
    if 'net10' in net_version:
        print('> Building Example App Net10')
        build_with_delay(EXAMPLE_APP_CSPROJ_NET10, config)
    else:
        print('> Building Example App Net8')
        build_with_delay(EXAMPLE_APP_CSPROJ, config)
def build_example_nuget(targets, config, net_version):
    if 'net10' in net_version:
        print('> Building Example Nuget Net10')
        build_with_delay(EXAMPLE_APP_CSPROJ_NUGET_NET10, config)
    else:
        print('> Building Example Nuget Net8')
        build_with_delay(EXAMPLE_APP_CSPROJ_NUGET, config)

target_help = '''Which targets to build or clean (can specify multiple):

  Clean targets:
    bindings        - Native binding projects only
    sdk             - SDK wrapper projects only
    apps            - App projects only

  Platforms:
    android         - Android targets only
    ios             - iOS targets only

  SDKs:
    core            - Core SDK binding/wrapper
    oaid            - OAID plugin
    meta_referrer   - Meta Referrer plugin
    google_lvl      - Google LVL plugin
    plugins         - All plugins (oaid, meta_referrer, google_lvl)

  Apps:
    test            - Test app
    example         - Example app (project references)
    example-nuget   - Example app (NuGet references)

  .NET version:
    net8            - .NET 8 targets only
    net10           - .NET 10 targets only

  Configuration:
    debug           - Debug configuration
    release         - Release configuration
'''

def main(argv=None):
    common = argparse.ArgumentParser(add_help=False)

    common.add_argument(
        'targets',
        nargs='*',
        choices=['bindings', 'sdk', 'apps',
            'test', 'example', 'example-nuget',
            'android', 'ios',
            'core', 'oaid', 'meta_referrer', 'google_lvl', 'plugins',
            'net8', 'net10',
            'debug', 'release'
        ],
        metavar='TARGET',
        help=target_help
    )
    common.add_argument('--dry', action='store_true', default=False, help='Perform a dry run (list bin/obj dirs only)')

    parser = argparse.ArgumentParser(
        description='Python3 build tool for Adjust Maui repo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=target_help
    )
    sub = parser.add_subparsers(dest='command')
    sub.add_parser('clean', help='Clean build artifacts (bin/obj dirs)', parents=[common])
    sub.add_parser('clean_bindings', help='Clean and build bindings', parents=[common])
    sub.add_parser('clean_sdk', help='Clean and build SDK', parents=[common])
    sub.add_parser('clean_apps', help='Clean and build apps', parents=[common])

    sub.add_parser('bindings', help='Build specified bindings', parents=[common])
    sub.add_parser('sdk', help='Build maui sdk', parents=[common])
    sub.add_parser('apps', help='Build maui apps', parents=[common])

    sub.add_parser('all', help='Clean and build all targets', parents=[common])


    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 1

    arg_found = False

    print('targets: %s' % args.targets)

    if args.command == 'all' or args.command.startswith('clean'):
        clean(args.command, args.targets, args.dry)
        arg_found = True
    if args.command == 'all' or args.command.endswith('bindings'):
        build_bindings(args.targets)
        arg_found = True
    if args.command == 'all' or args.command.endswith('sdk'):
        build_sdk(args.targets)
        arg_found = True
    if args.command == 'all' or args.command.endswith('apps'):
        build_apps(args.targets)
        arg_found = True

    if not arg_found:
        parser.print_help()
        return 1

    return 0

ARTIFACTS_OUTPUT_DIR = os.path.join(ROOT, '.artifacts')

ARTIFACTS_CORE_BINDING_ANDROID_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, CORE_BINDING_ANDROID_NAME)
ARTIFACTS_CORE_BINDING_IOS_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, CORE_BINDING_IOS_NAME)
ARTIFACTS_TEST_BINDING_ANDROID_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, TEST_BINDING_ANDROID_NAME)
ARTIFACTS_TEST_BINDING_IOS_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, TEST_BINDING_IOS_NAME)
ARTIFACTS_OAID_BINDING_ANDROID_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, OAID_BINDING_ANDROID_NAME)
ARTIFACTS_META_REFERRER_BINDING_ANDROID_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, META_REFERRER_BINDING_ANDROID_NAME)
ARTIFACTS_GOOGLE_LVL_BINDING_ANDROID_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, GOOGLE_LVL_BINDING_ANDROID_NAME)

ARTIFACTS_CORE_SDK_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, CORE_SDK_NAME)
ARTIFACTS_OAID_SDK_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, OAID_SDK_NAME)
ARTIFACTS_META_REFERRER_SDK_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, META_REFERRER_SDK_NAME)
ARTIFACTS_GOOGLE_LVL_SDK_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, GOOGLE_LVL_SDK_NAME)
ARTIFACTS_TEST_APP_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, TEST_APP_NAME)
ARTIFACTS_EXAMPLE_APP_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, EXAMPLE_APP_NAME)
ARTIFACTS_EXAMPLE_APP_NUGET_OUTPUT_DIR = os.path.join(ARTIFACTS_OUTPUT_DIR, EXAMPLE_APP_NAME + '-Nuget')

ARTIFACTS_COPY_BIN_DIR = os.path.join(ROOT, 'artifacts_copy', 'build_bin')
ARTIFACTS_COPY_OBJ_DIR = os.path.join(ROOT, 'artifacts_copy', 'build_obj')

ARTIFACTS_COPY_OUTPUT_DIRS = [ARTIFACTS_COPY_BIN_DIR, ARTIFACTS_COPY_OBJ_DIR]
ARTIFACTS_COPY_CORE_BINDING_ANDROID_OUTPUT_DIRS = [os.path.join(ARTIFACTS_COPY_BIN_DIR, CORE_BINDING_ANDROID_NAME), os.path.join(ARTIFACTS_COPY_OBJ_DIR, CORE_BINDING_ANDROID_NAME)]
ARTIFACTS_COPY_CORE_BINDING_IOS_OUTPUT_DIRS = [os.path.join(ARTIFACTS_COPY_BIN_DIR, CORE_BINDING_IOS_NAME), os.path.join(ARTIFACTS_COPY_OBJ_DIR, CORE_BINDING_IOS_NAME)]
ARTIFACTS_COPY_TEST_BINDING_ANDROID_OUTPUT_DIRS = [os.path.join(ARTIFACTS_COPY_BIN_DIR, TEST_BINDING_ANDROID_NAME), os.path.join(ARTIFACTS_COPY_OBJ_DIR, TEST_BINDING_ANDROID_NAME)]
ARTIFACTS_COPY_TEST_BINDING_IOS_OUTPUT_DIRS = [os.path.join(ARTIFACTS_COPY_BIN_DIR, TEST_BINDING_IOS_NAME), os.path.join(ARTIFACTS_COPY_OBJ_DIR, TEST_BINDING_IOS_NAME)]
ARTIFACTS_COPY_OAID_BINDING_ANDROID_OUTPUT_DIRS = [os.path.join(ARTIFACTS_COPY_BIN_DIR, OAID_BINDING_ANDROID_NAME), os.path.join(ARTIFACTS_COPY_OBJ_DIR, OAID_BINDING_ANDROID_NAME)]
ARTIFACTS_COPY_META_REFERRER_BINDING_ANDROID_OUTPUT_DIRS = [os.path.join(ARTIFACTS_COPY_BIN_DIR, META_REFERRER_BINDING_ANDROID_NAME), os.path.join(ARTIFACTS_COPY_OBJ_DIR, META_REFERRER_BINDING_ANDROID_NAME)]
ARTIFACTS_COPY_GOOGLE_LVL_BINDING_ANDROID_OUTPUT_DIRS = [os.path.join(ARTIFACTS_COPY_BIN_DIR, GOOGLE_LVL_BINDING_ANDROID_NAME), os.path.join(ARTIFACTS_COPY_OBJ_DIR, GOOGLE_LVL_BINDING_ANDROID_NAME)]

ARTIFACTS_COPY_CORE_SDK_OUTPUT_DIRS = [os.path.join(ARTIFACTS_COPY_BIN_DIR, CORE_SDK_NAME), os.path.join(ARTIFACTS_COPY_OBJ_DIR, CORE_SDK_NAME)]
ARTIFACTS_COPY_OAID_SDK_OUTPUT_DIRS = [os.path.join(ARTIFACTS_COPY_BIN_DIR, OAID_SDK_NAME), os.path.join(ARTIFACTS_COPY_OBJ_DIR, OAID_SDK_NAME)]
ARTIFACTS_COPY_META_REFERRER_SDK_OUTPUT_DIRS = [os.path.join(ARTIFACTS_COPY_BIN_DIR, META_REFERRER_SDK_NAME), os.path.join(ARTIFACTS_COPY_OBJ_DIR, META_REFERRER_SDK_NAME)]
ARTIFACTS_COPY_GOOGLE_LVL_SDK_OUTPUT_DIRS = [os.path.join(ARTIFACTS_COPY_BIN_DIR, GOOGLE_LVL_SDK_NAME), os.path.join(ARTIFACTS_COPY_OBJ_DIR, GOOGLE_LVL_SDK_NAME)]
ARTIFACTS_COPY_TEST_APP_OUTPUT_DIRS = [os.path.join(ARTIFACTS_COPY_BIN_DIR, TEST_APP_NAME), os.path.join(ARTIFACTS_COPY_OBJ_DIR, TEST_APP_NAME)]
ARTIFACTS_COPY_EXAMPLE_APP_OUTPUT_DIRS = [os.path.join(ARTIFACTS_COPY_BIN_DIR, EXAMPLE_APP_NAME), os.path.join(ARTIFACTS_COPY_OBJ_DIR, EXAMPLE_APP_NAME)]
ARTIFACTS_COPY_EXAMPLE_APP_NUGET_OUTPUT_DIRS = [os.path.join(ARTIFACTS_COPY_BIN_DIR, EXAMPLE_APP_NAME + '-Nuget'), os.path.join(ARTIFACTS_COPY_OBJ_DIR, EXAMPLE_APP_NAME + '-Nuget')]

def clean(command: str, targets: list[str], dry: bool):
    targets = targets[:] # copy the list to avoid modifying the original list
    if (command == 'clean' or command == 'all') and has_none(targets, ('bindings', 'sdk', 'apps')):
        clean_target(dry, ARTIFACTS_OUTPUT_DIR)
        clean_artifacts_copy(dry, ARTIFACTS_COPY_OUTPUT_DIRS)
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
        clean_artifacts_copy(dry, ARTIFACTS_COPY_CORE_SDK_OUTPUT_DIRS)
    if 'oaid' in targets or no_sdk_target:
        clean_target(dry, ARTIFACTS_OAID_SDK_OUTPUT_DIR)
        clean_artifacts_copy(dry, ARTIFACTS_COPY_OAID_SDK_OUTPUT_DIRS)
    if 'meta_referrer' in targets or no_sdk_target:
        clean_target(dry, ARTIFACTS_META_REFERRER_SDK_OUTPUT_DIR)
        clean_artifacts_copy(dry, ARTIFACTS_COPY_META_REFERRER_SDK_OUTPUT_DIRS)
    if 'google_lvl' in targets or no_sdk_target:
        clean_target(dry, ARTIFACTS_GOOGLE_LVL_SDK_OUTPUT_DIR)
        clean_artifacts_copy(dry, ARTIFACTS_COPY_GOOGLE_LVL_SDK_OUTPUT_DIRS)

def clean_apps(targets, dry):
    no_app_target = has_none(APPS, targets)
    if 'test' in targets or no_app_target:
        clean_target(dry, ARTIFACTS_TEST_APP_OUTPUT_DIR)
        clean_artifacts_copy(dry, ARTIFACTS_COPY_TEST_APP_OUTPUT_DIRS)
    if 'example' in targets or no_app_target:
        clean_target(dry, ARTIFACTS_EXAMPLE_APP_OUTPUT_DIR)
        clean_artifacts_copy(dry, ARTIFACTS_COPY_EXAMPLE_APP_OUTPUT_DIRS)
    if 'example-nuget' in targets or no_app_target:
        clean_target(dry, ARTIFACTS_EXAMPLE_APP_NUGET_OUTPUT_DIR)
        clean_artifacts_copy(dry, ARTIFACTS_COPY_EXAMPLE_APP_NUGET_OUTPUT_DIRS)

def clean_test_bindings(targets, dry):
    no_platform_target = has_none(PLATFORMS, targets)
    if 'ios' in targets or no_platform_target:
        clean_target(dry, ARTIFACTS_TEST_BINDING_IOS_OUTPUT_DIR)
        clean_artifacts_copy(dry, ARTIFACTS_COPY_TEST_BINDING_IOS_OUTPUT_DIRS)
    if 'android' in targets or no_platform_target:
        clean_target(dry, ARTIFACTS_TEST_BINDING_ANDROID_OUTPUT_DIR)
        clean_artifacts_copy(dry, ARTIFACTS_COPY_TEST_BINDING_ANDROID_OUTPUT_DIRS)

def clean_core_bindings(targets, dry):
    no_platform_target = has_none(PLATFORMS, targets)
    if 'ios' in targets or no_platform_target:
        clean_target(dry, ARTIFACTS_CORE_BINDING_IOS_OUTPUT_DIR)
        clean_artifacts_copy(dry, ARTIFACTS_COPY_CORE_BINDING_IOS_OUTPUT_DIRS)
    if 'android' in targets or no_platform_target:
        clean_target(dry, ARTIFACTS_CORE_BINDING_ANDROID_OUTPUT_DIR)
        clean_artifacts_copy(dry, ARTIFACTS_COPY_CORE_BINDING_ANDROID_OUTPUT_DIRS)

def clean_oaid_bindings(targets, dry):
    clean_target(dry, ARTIFACTS_OAID_BINDING_ANDROID_OUTPUT_DIR)
    clean_artifacts_copy(dry, ARTIFACTS_COPY_OAID_BINDING_ANDROID_OUTPUT_DIRS)

def clean_meta_referrer_bindings(targets, dry):
    clean_target(dry, ARTIFACTS_META_REFERRER_BINDING_ANDROID_OUTPUT_DIR)
    clean_artifacts_copy(dry, ARTIFACTS_COPY_META_REFERRER_BINDING_ANDROID_OUTPUT_DIRS)

def clean_google_lvl_bindings(targets, dry):
    clean_target(dry, ARTIFACTS_GOOGLE_LVL_BINDING_ANDROID_OUTPUT_DIR)
    clean_artifacts_copy(dry, ARTIFACTS_COPY_GOOGLE_LVL_BINDING_ANDROID_OUTPUT_DIRS)

def find_bin_obj_dirs_cmd(subdir=None):
    search_root = os.path.join(ROOT, subdir) if subdir else ROOT
    return ['find', search_root, '-type', 'd', '(', '-name', 'bin', '-o', '-name', 'obj', ')', '-prune']

def find_files_cmd(subdir_list: list[str]):
    search_roots = [os.path.join(ROOT, subdir) for subdir in subdir_list]
    return ['find'] + search_roots + ['-type', 'f']

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
def clean_artifacts_copy(dry, subdir_list: list[str]):
    if dry:
        print('> dry-run: listing files under %s' % subdir_list)
        subprocess.run(find_files_cmd(subdir_list) + ['-print'])
        return
    if which('trash'):
        print('> trash directories: %s' % subdir_list)
        for subdir in subdir_list:
            subprocess.run(['trash', subdir])
    else:
        print('> rm -rf directories: %s' % subdir_list)
        for subdir in subdir_list:
            subprocess.run(['rm', '-rf', subdir])

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
