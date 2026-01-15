#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import shutil
import subprocess
import sys
import time
import json
from typing import Optional, List


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
EXAMPLE_CSProj = os.path.join(ROOT, 'ExampleApp', 'ExampleApp.csproj')
EXAMPLE_CSProj_NET10 = os.path.join(ROOT, 'ExampleApp', 'ExampleApp-Net10.csproj')
EXAMPLE_NUGET_CSProj = os.path.join(ROOT, 'ExampleApp', 'ExampleApp-Nuget.csproj')
EXAMPLE_NUGET_CSProj_NET10 = os.path.join(ROOT, 'ExampleApp', 'ExampleApp-Nuget-Net10.csproj')
TESTAPP_CSProj = os.path.join(ROOT, 'TestApp', 'TestApp.csproj')
TESTAPP_CSProj_NET10 = os.path.join(ROOT, 'TestApp', 'TestApp-Net10.csproj')

def log(msg: str) -> None:
    print(msg)

def set_net_version(net_version: str):
    if net_version == 'net8':
        version = "8.0.402"
    else:
        version = "10.0.101"
    global_json = {"sdk": {"version": version, "rollForward": "latestFeature"}}
    with open(os.path.join(ROOT, "global.json"), "w") as f:
        json.dump(global_json, f, indent=2)


def run(cmd, cwd=None, check=True) -> int:
    log('> ' + ' '.join(cmd))
    result = subprocess.run(cmd, cwd=cwd)
    if check and result.returncode != 0:
        sys.exit(result.returncode)
    return result.returncode


def ensure_example_exists(net_version: str) -> None:
    if net_version == 'net10':
        csproj = EXAMPLE_CSProj_NET10
    else:
        csproj = EXAMPLE_CSProj
    if not os.path.isfile(csproj):
        log('ExampleApp.csproj not found at: %s' % csproj)
        sys.exit(1)

def ensure_example_nuget_exists(net_version: str) -> None:
    if net_version == 'net10':
        csproj = EXAMPLE_NUGET_CSProj_NET10
    else:
        csproj = EXAMPLE_NUGET_CSProj
    if not os.path.isfile(csproj):
        log('ExampleApp-Nuget.csproj not found at: %s' % csproj)
        sys.exit(1)

def ensure_test_exists(net_version: str) -> None:
    if net_version == 'net10':
        csproj = TESTAPP_CSProj_NET10
    else:
        csproj = TESTAPP_CSProj
    if not os.path.isfile(csproj):
        log('TestApp.csproj not found at: %s' % csproj)
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


def get_ios_sim_udid(sim_name: str) -> Optional[str]:
    """Return UDID of the requested simulator name, preferring Booted if multiple."""
    try:
        out = subprocess.check_output(['xcrun', 'simctl', 'list', 'devices', 'available', '--json'])
        data = json.loads(out)
        booted: List[str] = []
        matches: List[str] = []
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


def get_ios_device_udid(device_name: str) -> Optional[str]:
    """Return UDID of the requested physical device name."""
    try:
        out = subprocess.check_output(['xcrun', 'xctrace', 'list', 'devices'], stderr=subprocess.DEVNULL)
        lines = out.decode('utf-8').split('\n')
        in_devices_section = False
        for line in lines:
            line = line.strip()
            if line == '== Devices ==':
                in_devices_section = True
                continue
            if line.startswith('==') and line.endswith('=='):
                in_devices_section = False
                continue
            if in_devices_section and device_name in line:
                # Extract UDID from line like "uPhone (26.1) (00008120-001645063C43A01E)"
                parts = line.split('(')
                if len(parts) >= 3:
                    udid = parts[-1].rstrip(')').strip()
                    if len(udid) > 20:  # UDIDs are typically long
                        return udid
    except Exception as e:
        log(f'Error getting device UDID: {e}')
    return None


def resolve_csproj(app: str, net_version: str) -> str:
    if app == 'example':
        ensure_example_exists(net_version)
        if net_version == 'net10':
            return EXAMPLE_CSProj_NET10
        else:
            return EXAMPLE_CSProj
    if app == 'example-nuget':
        ensure_example_nuget_exists(net_version)
        if net_version == 'net10':
            return EXAMPLE_NUGET_CSProj_NET10
        else:
            return EXAMPLE_NUGET_CSProj
    if app == 'test':
        ensure_test_exists(net_version)
        if net_version == 'net10':
            return TESTAPP_CSProj_NET10
        else:
            return TESTAPP_CSProj
    log("Unknown app: %s (expected 'test', 'example' or 'example-nuget') with net-version: %s" % (app, net_version))
    sys.exit(1)


def get_android_tfm(net_version: str) -> str:
    """Get the target framework moniker for Android based on .NET version."""
    if net_version == 'net10':
        return 'net10.0-android36.0'
    else:
        return 'net8.0-android'  # .NET 8 doesn't require explicit version

def get_ios_tfm(net_version: str) -> str:
    """Get the target framework moniker for iOS based on .NET version."""
    if net_version == 'net10':
        return 'net10.0-ios26.2'
    else:
        return 'net8.0-ios'  # .NET 8 doesn't require explicit version

def run_android(config: str, avd_name: str, app: str, net_version: str) -> None:
    csproj = resolve_csproj(app, net_version)
    boot_android_avd(avd_name)
    set_net_version(net_version)
    tfm = get_android_tfm(net_version)
    run(['dotnet', 'build', csproj, '-c', config, '-f', tfm, '-t:Run'])

def run_ios(config: str, sim_name: Optional[str], app: str, net_version: str, device_name: Optional[str] = None) -> None:
    csproj = resolve_csproj(app, net_version)
    set_net_version(net_version)
    tfm = get_ios_tfm(net_version)

    if device_name:
        # Running on physical device
        log(f'Running on iOS device: {device_name}')
        udid = get_ios_device_udid(device_name)
        if not udid:
            log(f'Error: Device "{device_name}" not found. Use "list-devices" to see available devices.')
            sys.exit(1)
        log(f'Found device UDID: {udid}')
        # Clean iOS simulator build artifacts to ensure we rebuild for device
        log('Cleaning iOS simulator build artifacts to ensure device build...')
        app_name = os.path.basename(csproj).replace('.csproj', '')
        artifacts_obj_dir = os.path.join(ROOT, '.artifacts', app_name, 'obj', config, tfm)
        artifacts_bin_dir = os.path.join(ROOT, '.artifacts', app_name, 'bin', config, tfm)
        # Remove all simulator-related build artifacts
        for artifacts_dir in [artifacts_obj_dir, artifacts_bin_dir]:
            if os.path.exists(artifacts_dir):
                for item in os.listdir(artifacts_dir):
                    item_path = os.path.join(artifacts_dir, item)
                    if os.path.isdir(item_path) and 'simulator' in item.lower():
                        log(f'Removing simulator build artifacts: {item}')
                        shutil.rmtree(item_path, ignore_errors=True)
        # Build and run for device (clean build to avoid simulator artifacts)
        log('Building for iOS device (this may take a moment)...')
        cmd = ['dotnet', 'build', csproj, '-c', config, '-f', tfm, '-p:RuntimeIdentifier=ios-arm64', '-t:Run']
        # Use just the UDID for _DeviceName (mlaunch expects UDID directly)
        cmd.append(f'-p:_DeviceName={udid}')
    else:
        # Running on simulator (default behavior)
        if sim_name:
            boot_ios_sim(sim_name)
            udid = get_ios_sim_udid(sim_name)
        else:
            udid = None
        cmd = ['dotnet', 'build', csproj, '-c', config, '-f', tfm, '-p:RuntimeIdentifier=iossimulator-arm64', '-t:Run']
        if udid:
            cmd.append(f'-p:_DeviceName=:v2:udid={udid}')
    
    run(cmd)

def list_android_avds() -> None:
    emu = shutil.which('emulator') or os.path.expanduser('~/Library/Android/sdk/emulator/emulator')
    if not os.path.exists(emu):
        log('Android emulator not found.')
        return
    run([emu, '-list-avds'], check=False)


def list_ios_sims() -> None:
    run(['xcrun', 'simctl', 'list', 'devices', 'available'], check=False)


def list_ios_devices() -> None:
    """List available physical iOS devices."""
    run(['xcrun', 'xctrace', 'list', 'devices'], check=False)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description='Configure and run the MAUI Example/Test apps')
    sub = parser.add_subparsers(dest='command')

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('-c', '--config', default='Debug', choices=['Debug', 'Release'], help='Build configuration (default: Debug)')

    # Run
    p_run_android = sub.add_parser('run-android', parents=[common], help='Boot emulator and run selected app on Android')
    p_run_android.add_argument('app', choices=['test', 'example', 'example-nuget'], help='Which app to run')
    p_run_android.add_argument('--net10', action='store_true', help='Use .NET 10')
    p_run_android.add_argument('--avd', default=os.environ.get('ANDROID_AVD', 'Pixel_5_API_34'), help='Android AVD name')

    p_run_ios = sub.add_parser('run-ios', parents=[common], help='Run selected app on iOS simulator or device')
    p_run_ios.add_argument('app', choices=['test', 'example', 'example-nuget'], help='Which app to run')
    p_run_ios.add_argument('--net10', action='store_true', help='Use .NET 10')
    p_run_ios.add_argument('--ios-sim', default=os.environ.get('IOS_SIM', 'iPhone 15'), help='iOS Simulator name (used if --device not specified)')
    p_run_ios.add_argument('--device', help='Physical iOS device name (e.g., "uPhone"). Overrides --ios-sim.')

    # List devices
    sub.add_parser('list-avds', help='List Android AVDs')
    sub.add_parser('list-sims', help='List available iOS simulators')
    sub.add_parser('list-devices', help='List available physical iOS devices')

    return parser.parse_args(argv)

def main(argv=None) -> int:
    args = parse_args(argv)
    if not args.command:
        print('Usage: maui_run.py [run-android|run-ios|list-avds|list-sims|list-devices] [options]')
        return 1
    net_version = 'net8'
    if hasattr(args, 'net10') and args.net10:
        net_version = 'net10'
    if args.command == 'run-android':
        run_android(args.config, args.avd, args.app, net_version)
        return 0
    if args.command == 'run-ios':
        device_name = getattr(args, 'device', None)
        sim_name = args.ios_sim if not device_name else None
        run_ios(args.config, sim_name, args.app, net_version, device_name)
        return 0
    if args.command == 'list-avds':
        list_android_avds()
        return 0
    if args.command == 'list-sims':
        list_ios_sims()
        return 0
    if args.command == 'list-devices':
        list_ios_devices()
        return 0

    print('Unknown command')
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


