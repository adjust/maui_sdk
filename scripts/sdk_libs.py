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


def _build_and_copy_aar_common(
    is_release,
    gradle_task_template,
    candidate_path_templates,
    dest_path,
    search_dir=None,
    search_prefix=None,
):
    """Build an AAR with gradle and copy it to destination.

    - gradle_task_template: e.g. ':sdk-core:adjustCoreAar{Variant}' (Variant = Release/Debug)
    - candidate_path_templates: list of path templates where the produced file could exist,
      using {variant} placeholder as 'release'/'debug'
    - dest_path: destination file path; may include {variant} placeholder
    - search_dir/search_prefix: optional fallback directory and filename prefix to scan
    """
    ensure_paths()

    variant_cap = 'Release' if is_release else 'Debug'
    variant_lower = 'release' if is_release else 'debug'

    # Ensure gradlew is executable
    try:
        st = os.stat(ANDROID_GRADLEW)
        if not (st.st_mode & 0o111):
            os.chmod(ANDROID_GRADLEW, st.st_mode | 0o111)
    except Exception:
        pass

    gradle_task = gradle_task_template.format(Variant=variant_cap)
    run([ANDROID_GRADLEW, gradle_task, '--no-daemon'], cwd=ANDROID_SUBMODULE_ROOT)

    produced_path = None
    tried_paths = []
    for tpl in candidate_path_templates:
        candidate = tpl.format(variant=variant_lower)
        tried_paths.append(candidate)
        if os.path.isfile(candidate):
            produced_path = candidate
            break

    # Fallback: scan search_dir for a matching name
    if produced_path is None and search_dir and os.path.isdir(search_dir):
        for fn in os.listdir(search_dir):
            if not fn.endswith('.aar'):
                continue
            if search_prefix and not fn.startswith(search_prefix):
                continue
            if variant_lower in fn:
                produced_path = os.path.join(search_dir, fn)
                break

    if produced_path is None:
        print('Failed to locate built AAR. Looked for:')
        for p in tried_paths:
            print('  ' + p)
        if search_dir:
            print('Also searched dir: ' + search_dir)
        sys.exit(1)

    final_dest = dest_path.format(variant=variant_lower)
    os.makedirs(os.path.dirname(final_dest), exist_ok=True)
    shutil.copyfile(produced_path, final_dest)
    print('Copied AAR to %s' % final_dest)
    return final_dest


def build_android_sdk(is_release):
    return _build_and_copy_aar_common(
        is_release=is_release,
        gradle_task_template=':sdk-core:adjustCoreAar{Variant}',
        candidate_path_templates=[
            os.path.join(ANDROID_SDK_CORE_DIR, 'build', 'libs', 'adjust-sdk-{variant}.aar'),
            os.path.join(ANDROID_SDK_CORE_DIR, 'build', 'outputs', 'aar', 'sdk-core-{variant}.aar'),
        ],
        dest_path=os.path.join(ANDROID_BINDING_LIBS_DIR, 'adjust-android.aar'),
        search_dir=None,
        search_prefix=None,
    )


def build_android_test_library_aar(is_release):
    return _build_and_copy_aar_common(
        is_release=is_release,
        gradle_task_template=':tests:test-library:adjustTestLibraryAar{Variant}',
        candidate_path_templates=[
            os.path.join(ANDROID_TEST_LIBRARY_DIR, 'build', 'libs', 'test-library-{variant}.aar'),
            os.path.join(ANDROID_TEST_LIBRARY_DIR, 'build', 'outputs', 'aar', 'test-library-{variant}.aar'),
        ],
        dest_path=os.path.join(ANDROID_TEST_BINDING_LIBS_DIR, 'test-library-{variant}.aar'),
        search_dir=None,
        search_prefix=None,
    )


def build_android_test_options_aar(is_release):
    return _build_and_copy_aar_common(
        is_release=is_release,
        gradle_task_template=':tests:test-options:assemble{Variant}',
        candidate_path_templates=[
            os.path.join(ANDROID_TEST_OPTIONS_DIR, 'build', 'outputs', 'aar', 'test-options-{variant}.aar'),
        ],
        dest_path=os.path.join(ANDROID_TEST_BINDING_LIBS_DIR, 'test-options-{variant}.aar'),
        search_dir=os.path.join(ANDROID_TEST_OPTIONS_DIR, 'build', 'outputs', 'aar'),
        search_prefix='test-options-'
    )

def build_android_tests(is_release):
    build_android_test_library_aar(is_release)
    build_android_test_options_aar(is_release)

def build_all(targets, is_release):
    if 'sdk' in targets or 'all' in targets:
        build_sdk(targets, is_release)
    if 'test' in targets or 'all' in targets:
        build_test(targets, is_release)

def build_sdk(targets, is_release):
    if 'android' in targets or 'all' in targets:
        build_android_sdk(is_release)

def build_test(targets, is_release):
    if 'android' in targets or 'all' in targets:
        build_android_tests(is_release)

def main(argv=None):
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--release', action='store_true', help='Build in Release (default: Debug)')
    common.add_argument(
        'targets',
        nargs='*',
        choices=['sdk', 'test', 'android', 'ios', 'all'],
        help='Which targets (can specify multiple, default: all)'
    )

    parser = argparse.ArgumentParser(description='Build SDK libraries for MAUI bindings')
    sub = parser.add_subparsers(dest='command')
    sub.add_parser('build', help='Build specified targets', parents=[common])
    #sub.add_parser('clean', help='Clean build artifacts (bin/obj dirs)', parents=[common])
    #sub.add_parser('clean_build', help='Clean and build targets', parents=[common])

    args = parser.parse_args(argv)

    targets = args.targets if getattr(args, 'targets', None) else ['all']

    arg_found = False

#    if args.command in ('clean', 'clean_bindings', 'clean_build'):
#        clean(args.dry)
#        arg_found = True
#    if args.command in ('bindings', 'clean_bindings'):
#        build_bindings(targets, config)
#        arg_found = True
    if args.command in ('build', 'clean_build'):
        build_all(targets, args.release)
        arg_found = True

    if not arg_found:
        parser.print_help()
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


