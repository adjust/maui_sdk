#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import shutil
import subprocess
import sys
import time
import json


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
EXAMPLE_CSProj = os.path.join(ROOT, 'ExampleApp', 'ExampleApp.csproj')

TESTAPP_CSProj = os.path.join(ROOT, 'testApp', 'TestApp.csproj')

def log(msg: str) -> None:
    print(msg)


def run(cmd, cwd=None, check=True) -> int:
    log('> ' + ' '.join(cmd))
    result = subprocess.run(cmd, cwd=cwd)
    if check and result.returncode != 0:
        sys.exit(result.returncode)
    return result.returncode


def ensure_example_exists() -> None:
    if not os.path.isfile(EXAMPLE_CSProj):
        log('ExampleApp.csproj not found at: %s' % EXAMPLE_CSProj)
        sys.exit(1)

def ensure_test_exists() -> None:
    if not os.path.isfile(TESTAPP_CSProj):
        log('TestApp.csproj not found at: %s' % TESTAPP_CSProj)
        sys.exit(1)

def boot_android_avd(avd_name: str) -> None:
    # Try system emulator first, fallback to default SDK location
    emu_bin = shutil.which('emulator')
    if not emu_bin:
        emu_bin = os.path.expanduser('~/Library/Android/sdk/emulator/emulator')
    if not os.path.exists(emu_bin):
        log('Android emulator not found. Ensure Android SDK is installed and emulator is on PATH.')
        sys.exit(1)

    # Check if AVD is running; if not, start
    # There's no simple cross-platform check; attempt to start headless
    log('Booting Android AVD: %s' % avd_name)
    subprocess.Popen([emu_bin, '-avd', avd_name, '-netdelay', 'none', '-netspeed', 'full', '-no-snapshot-load'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Give emulator time to boot
    time.sleep(5)


def boot_ios_sim(sim_name: str) -> None:
    if run(['xcrun', '--version'], check=False) != 0:
        log('xcrun not found. Install Xcode command line tools.')
        sys.exit(1)
    log('Booting iOS Simulator: %s' % sim_name)
    # Newer Xcode supports bootstatus; fallback to boot only
    code = run(['xcrun', 'simctl', 'bootstatus', sim_name, '-b'], check=False)
    if code != 0:
        run(['xcrun', 'simctl', 'boot', sim_name], check=False)
    run(['open', '-a', 'Simulator'], check=False)


def get_ios_sim_udid(sim_name: str) -> str | None:
    """Return UDID of the requested simulator name, preferring Booted if multiple."""
    try:
        out = subprocess.check_output(['xcrun', 'simctl', 'list', 'devices', 'available', '--json'])
        data = json.loads(out)
        booted: list[str] = []
        matches: list[str] = []
        for runtime_devices in data.get('devices', {}).values():
            for dev in runtime_devices:
                if dev.get('name') == sim_name:
                    udid = dev.get('udid')
                    if not udid:
                        continue
                    if dev.get('state') == 'Booted':
                        booted.append(udid)
                    else:
                        matches.append(udid)
        if booted:
            return booted[0]
        if matches:
            return matches[0]
    except Exception:
        pass
    return None


def resolve_csproj(app: str) -> str:
    if app == 'example':
        ensure_example_exists()
        return EXAMPLE_CSProj
    if app == 'test':
        ensure_test_exists()
        return TESTAPP_CSProj
    log("Unknown app: %s (expected 'test' or 'example')" % app)
    sys.exit(1)


def run_android(config: str, avd_name: str, app: str) -> None:
    csproj = resolve_csproj(app)
    boot_android_avd(avd_name)
    run(['dotnet', 'build', csproj, '-c', config, '-f', 'net8.0-android', '-t:Run'])


def run_ios(config: str, sim_name: str, app: str) -> None:
    csproj = resolve_csproj(app)
    boot_ios_sim(sim_name)
    udid = get_ios_sim_udid(sim_name)
    cmd = ['dotnet', 'build', csproj, '-c', config, '-f', 'net8.0-ios', '-p:RuntimeIdentifier=iossimulator-arm64']
    if udid:
        cmd.append(f'-p:_DeviceName=:v2:udid={udid}')
    cmd.append('-t:Run')
    run(cmd)

def list_android_avds() -> None:
    emu = shutil.which('emulator') or os.path.expanduser('~/Library/Android/sdk/emulator/emulator')
    if not os.path.exists(emu):
        log('Android emulator not found.')
        return
    run([emu, '-list-avds'], check=False)


def list_ios_sims() -> None:
    run(['xcrun', 'simctl', 'list', 'devices', 'available'], check=False)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description='Configure and run the MAUI Example/Test apps')
    sub = parser.add_subparsers(dest='command')

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('-c', '--config', default='Debug', choices=['Debug', 'Release'], help='Build configuration (default: Debug)')

    # Run
    p_run_android = sub.add_parser('run-android', parents=[common], help='Boot emulator and run selected app on Android')
    p_run_android.add_argument('app', choices=['test', 'example'], help='Which app to run')
    p_run_android.add_argument('--avd', default=os.environ.get('ANDROID_AVD', 'Pixel_5_API_34'), help='Android AVD name')

    p_run_ios = sub.add_parser('run-ios', parents=[common], help='Boot simulator and run selected app on iOS simulator')
    p_run_ios.add_argument('app', choices=['test', 'example'], help='Which app to run')
    p_run_ios.add_argument('--ios-sim', default=os.environ.get('IOS_SIM', 'iPhone 15'), help='iOS Simulator name')

    # List devices
    sub.add_parser('list-avds', help='List Android AVDs')
    sub.add_parser('list-sims', help='List available iOS simulators')

    return parser.parse_args(argv)

def main(argv=None) -> int:
    args = parse_args(argv)
    if not args.command:
        print('Usage: maui_run.py [run-android|run-ios|list-avds|list-sims] [options]')
        return 1

    if args.command == 'run-android':
        run_android(args.config, args.avd, args.app)
        return 0
    if args.command == 'run-ios':
        run_ios(args.config, args.ios_sim, args.app)
        return 0
    if args.command == 'list-avds':
        list_android_avds()
        return 0
    if args.command == 'list-sims':
        list_ios_sims()
        return 0

    print('Unknown command')
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


