#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import shutil
import subprocess
import sys


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ANDROID_SUBMODULE_ROOT = os.path.join(ROOT, 'android_sdk', 'Adjust')
ANDROID_GRADLEW = os.path.join(ANDROID_SUBMODULE_ROOT, 'gradlew')
ANDROID_SDK_CORE_DIR = os.path.join(ANDROID_SUBMODULE_ROOT, 'sdk-core')
ANDROID_BINDING_LIBS_DIR = os.path.join(
    ROOT, 'android', 'AdjustSdk.AndroidBinding', 'libs'
)
ANDROID_TESTS_ROOT = os.path.join(ANDROID_SUBMODULE_ROOT, 'tests')
ANDROID_TEST_LIBRARY_DIR = os.path.join(ANDROID_TESTS_ROOT, 'test-library')
ANDROID_TEST_OPTIONS_DIR = os.path.join(ANDROID_TESTS_ROOT, 'test-options')
ANDROID_TEST_BINDING_LIBS_DIR = os.path.join(
    ROOT, 'android', 'TestLibrary.AndroidBinding', 'libs'
)


def run(cmd, cwd=None):
    print('> ' + ' '.join(cmd))
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        sys.exit(result.returncode)


def ensure_paths():
    if not os.path.isdir(ANDROID_SUBMODULE_ROOT):
        print('Android submodule directory not found: %s' % ANDROID_SUBMODULE_ROOT)
        sys.exit(1)
    if not os.path.isfile(ANDROID_GRADLEW):
        print('Gradle wrapper not found: %s' % ANDROID_GRADLEW)
        sys.exit(1)
    if not os.path.isdir(ANDROID_BINDING_LIBS_DIR):
        os.makedirs(ANDROID_BINDING_LIBS_DIR, exist_ok=True)
    if not os.path.isdir(ANDROID_TEST_BINDING_LIBS_DIR):
        os.makedirs(ANDROID_TEST_BINDING_LIBS_DIR, exist_ok=True)


def build_android_aar(is_release):
    ensure_paths()

    # Choose Gradle tasks and expected output file name from sdk-core module
    variant = 'Release' if is_release else 'Debug'
    gradle_task = f":sdk-core:adjustCoreAar{variant}"

    # Build the AAR using submodule's gradle wrapper
    # Use ./gradlew to avoid requiring a system gradle install
    gradlew_cmd = [
        ANDROID_GRADLEW,
        gradle_task,
        '--no-daemon',
    ]
    # On macOS/Linux ensure executable bit; if not, try to add it
    try:
        st = os.stat(ANDROID_GRADLEW)
        if not (st.st_mode & 0o111):
            os.chmod(ANDROID_GRADLEW, st.st_mode | 0o111)
    except Exception:
        pass

    run(gradlew_cmd, cwd=ANDROID_SUBMODULE_ROOT)

    # Where Gradle task copies/renames the aar to
    produced_name = 'adjust-sdk-release.aar' if is_release else 'adjust-sdk-debug.aar'
    produced_path = os.path.join(ANDROID_SDK_CORE_DIR, 'build', 'libs', produced_name)

    # Fallback to the default outputs location if custom task didn't copy
    if not os.path.isfile(produced_path):
        fallback_name = 'sdk-core-release.aar' if is_release else 'sdk-core-debug.aar'
        fallback_path = os.path.join(
            ANDROID_SDK_CORE_DIR, 'build', 'outputs', 'aar', fallback_name
        )
        if os.path.isfile(fallback_path):
            produced_path = fallback_path

    if not os.path.isfile(produced_path):
        print('Failed to locate built AAR. Looked for:')
        print('  ' + os.path.join(ANDROID_SDK_CORE_DIR, 'build', 'libs', produced_name))
        print('  ' + os.path.join(
            ANDROID_SDK_CORE_DIR, 'build', 'outputs', 'aar',
            'sdk-core-release.aar' if is_release else 'sdk-core-debug.aar'))
        sys.exit(1)

    # Copy into MAUI Android binding libs directory under expected name
    dest_path = os.path.join(ANDROID_BINDING_LIBS_DIR, 'adjust-android.aar')
    shutil.copyfile(produced_path, dest_path)
    print('Copied AAR to %s' % dest_path)


def build_android_test_library_aar(is_release):
    ensure_paths()

    variant = 'Release' if is_release else 'Debug'
    gradle_task = f":tests:test-library:adjustTestLibraryAar{variant}"

    # Ensure gradlew is executable
    try:
        st = os.stat(ANDROID_GRADLEW)
        if not (st.st_mode & 0o111):
            os.chmod(ANDROID_GRADLEW, st.st_mode | 0o111)
    except Exception:
        pass

    run([ANDROID_GRADLEW, gradle_task, '--no-daemon'], cwd=ANDROID_SUBMODULE_ROOT)

    produced_name = 'test-library-release.aar' if is_release else 'test-library-debug.aar'
    produced_path = os.path.join(ANDROID_TEST_LIBRARY_DIR, 'build', 'libs', produced_name)

    if not os.path.isfile(produced_path):
        fallback_path = os.path.join(
            ANDROID_TEST_LIBRARY_DIR, 'build', 'outputs', 'aar', produced_name
        )
        if os.path.isfile(fallback_path):
            produced_path = fallback_path

    if not os.path.isfile(produced_path):
        print('Failed to locate built Test Library AAR. Looked for:')
        print('  ' + os.path.join(ANDROID_TEST_LIBRARY_DIR, 'build', 'libs', produced_name))
        print('  ' + os.path.join(ANDROID_TEST_LIBRARY_DIR, 'build', 'outputs', 'aar', produced_name))
        sys.exit(1)

    dest_name = produced_name
    dest_path = os.path.join(ANDROID_TEST_BINDING_LIBS_DIR, dest_name)
    shutil.copyfile(produced_path, dest_path)
    print('Copied Test Library AAR to %s' % dest_path)


def build_android_test_options_aar(is_release):
    ensure_paths()

    variant = 'Release' if is_release else 'Debug'
    gradle_task = f":tests:test-options:assemble{variant}"

    # Ensure gradlew is executable
    try:
        st = os.stat(ANDROID_GRADLEW)
        if not (st.st_mode & 0o111):
            os.chmod(ANDROID_GRADLEW, st.st_mode | 0o111)
    except Exception:
        pass

    run([ANDROID_GRADLEW, gradle_task, '--no-daemon'], cwd=ANDROID_SUBMODULE_ROOT)

    produced_name = 'test-options-release.aar' if is_release else 'test-options-debug.aar'
    produced_path = os.path.join(
        ANDROID_TEST_OPTIONS_DIR, 'build', 'outputs', 'aar', produced_name
    )

    if not os.path.isfile(produced_path):
        # Some AGP variants may name it differently; try scanning outputs dir
        outputs_dir = os.path.join(ANDROID_TEST_OPTIONS_DIR, 'build', 'outputs', 'aar')
        alt = None
        if os.path.isdir(outputs_dir):
            for fn in os.listdir(outputs_dir):
                if fn.startswith('test-options-') and fn.endswith('.aar'):
                    if (is_release and 'release' in fn) or ((not is_release) and 'debug' in fn):
                        alt = os.path.join(outputs_dir, fn)
                        break
        if alt and os.path.isfile(alt):
            produced_path = alt

    if not os.path.isfile(produced_path):
        print('Failed to locate built Test Options AAR. Looked for:')
        print('  ' + produced_path)
        sys.exit(1)

    dest_name = 'test-options-release.aar' if is_release else 'test-options-debug.aar'
    dest_path = os.path.join(ANDROID_TEST_BINDING_LIBS_DIR, dest_name)
    shutil.copyfile(produced_path, dest_path)
    print('Copied Test Options AAR to %s' % dest_path)


def build_android_tests(is_release):
    build_android_test_library_aar(is_release)
    build_android_test_options_aar(is_release)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Build SDK libraries for MAUI bindings')
    sub = parser.add_subparsers(dest='command')

    p_android = sub.add_parser('android', help='Build Android AAR and copy to binding libs')
    p_android.add_argument('--release', action='store_true', help='Build Release (default: Debug)')

    p_android_tests = sub.add_parser('android-tests', help='Build Android Test AARs and copy to test binding libs')
    p_android_tests.add_argument('--release', action='store_true', help='Build Release (default: Debug)')

    args = parser.parse_args(argv)

    if args.command == 'android':
        build_android_aar(is_release=args.release)
        return 0
    if args.command == 'android-tests':
        build_android_tests(is_release=args.release)
        return 0

    parser.print_help()
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


