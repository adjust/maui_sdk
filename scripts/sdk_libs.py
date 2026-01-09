#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import shutil
import subprocess
import sys
import time
import signal

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ANDROID_SUBMODULE_ROOT = os.path.join(ROOT, 'android_sdk', 'Adjust')
#ANDROID_SUBMODULE_ROOT = os.path.join(ROOT, 'android_sdk_dev', 'Adjust')
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

ANDROID_PLUGINS_ROOT = os.path.join(ANDROID_SUBMODULE_ROOT, 'plugins')
ANDROID_OAID_DIR = os.path.join(ANDROID_PLUGINS_ROOT, 'sdk-plugin-oaid')
ANDROID_OAID_BINDING_LIBS_DIR = os.path.join(
    ROOT, 'android', 'AdjustOaid.AndroidBinding', 'libs'
)
ANDROID_META_REFERRER_DIR = os.path.join(ANDROID_PLUGINS_ROOT, 'sdk-plugin-meta-referrer')
ANDROID_META_REFERRER_BINDING_LIBS_DIR = os.path.join(
    ROOT, 'android', 'AdjustMetaReferrer.AndroidBinding', 'libs'
)
ANDROID_GOOGLE_LVL_DIR = os.path.join(ANDROID_PLUGINS_ROOT, 'sdk-plugin-google-lvl')
ANDROID_GOOGLE_LVL_BINDING_LIBS_DIR = os.path.join(
    ROOT, 'android', 'AdjustGoogleLVL.AndroidBinding', 'libs'
)

IOS_SDK_ROOT = os.path.join(ROOT, 'ios_sdk')
#IOS_SDK_ROOT = os.path.join(ROOT, 'ios_sdk_dev')
IOS_BINDING_DIR = os.path.join(ROOT, 'iOs', 'AdjustSdk.iOSBinding')
IOS_TEST_BINDING_DIR = os.path.join(ROOT, 'iOs', 'TestLibrary.iOSBinding')

PLATFORMS = ['android', 'ios']
SDKS = ['core', 'oaid', 'meta_referrer', 'google_lvl', 'test', 'plugins']

def run(cmd, cwd=None, env=None, check=True):
    print('> ' + ' '.join(cmd))
    result = subprocess.run(cmd, cwd=cwd, env=env)
    if check and result.returncode != 0:
        sys.exit(result.returncode)
    return result.returncode


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
    if not os.path.isdir(IOS_SDK_ROOT):
        print('iOS SDK directory not found: %s' % IOS_SDK_ROOT)
        # iOS build is optional; don't exit here.
    if not os.path.isdir(IOS_BINDING_DIR):
        # Create if missing so copy succeeds when building iOS
        os.makedirs(IOS_BINDING_DIR, exist_ok=True)
    if not os.path.isdir(IOS_TEST_BINDING_DIR):
        # Create if missing so copy succeeds when copying test framework
        os.makedirs(IOS_TEST_BINDING_DIR, exist_ok=True)

def _build_and_copy_aar_common(
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

    variant_cap = 'Release'
    variant_lower = 'release'

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

    print('Produced AAR: %s' % produced_path)

    final_dest = dest_path.format(variant=variant_lower)
    os.makedirs(os.path.dirname(final_dest), exist_ok=True)
    shutil.copyfile(produced_path, final_dest)
    print('Copied AAR to %s' % final_dest)
    return final_dest


def build_android_core():
    return _build_and_copy_aar_common(
        gradle_task_template=':sdk-core:adjustCoreAar{Variant}',
        candidate_path_templates=[
            os.path.join(ANDROID_SDK_CORE_DIR, 'build', 'libs', 'adjust-sdk-{variant}.aar'),
            os.path.join(ANDROID_SDK_CORE_DIR, 'build', 'outputs', 'aar', 'sdk-core-{variant}.aar'),
        ],
        dest_path=os.path.join(ANDROID_BINDING_LIBS_DIR, 'adjust-android.aar'),
        search_dir=None,
        search_prefix=None,
    )


def build_android_test_library():
    return _build_and_copy_aar_common(
        gradle_task_template=':tests:test-library:adjustTestLibraryAar{Variant}',
        candidate_path_templates=[
            os.path.join(ANDROID_TEST_LIBRARY_DIR, 'build', 'libs', 'test-library-{variant}.aar'),
            os.path.join(ANDROID_TEST_LIBRARY_DIR, 'build', 'outputs', 'aar', 'test-library-{variant}.aar'),
        ],
        dest_path=os.path.join(ANDROID_TEST_BINDING_LIBS_DIR, 'test-library.aar'),
        search_dir=None,
        search_prefix=None,
    )


def build_android_test_options():
    return _build_and_copy_aar_common(
        gradle_task_template=':tests:test-options:assemble{Variant}',
        candidate_path_templates=[
            os.path.join(ANDROID_TEST_OPTIONS_DIR, 'build', 'outputs', 'aar', 'test-options-{variant}.aar'),
        ],
        dest_path=os.path.join(ANDROID_TEST_BINDING_LIBS_DIR, 'test-options.aar'),
        search_dir=os.path.join(ANDROID_TEST_OPTIONS_DIR, 'build', 'outputs', 'aar'),
        search_prefix='test-options-'
    )

def build_android_oaid():
    return _build_and_copy_aar_common(
        # OAID module defines a single copy task that always depends on assembleRelease.
        # There is no variant-suffixed task (e.g., ...AarDebug), so call the fixed task.
        gradle_task_template=':plugins:sdk-plugin-oaid:adjustOaidAndroidAar',
        candidate_path_templates=[
            # Direct output from assembleRelease
            os.path.join(ANDROID_OAID_DIR, 'build', 'outputs', 'aar', 'sdk-plugin-oaid-release.aar'),
            # Or the copied/renamed artifact produced by adjustOaidAndroidAar
            os.path.join(ANDROID_OAID_DIR, 'build', 'libs', 'sdk-plugin-oaid.aar'),
        ],
        dest_path=os.path.join(ANDROID_OAID_BINDING_LIBS_DIR, 'adjust-android-oaid.aar'),
        search_dir=None,
        search_prefix=None,
    )

def build_android_meta_referrer():
    return _build_and_copy_aar_common(
        # Meta Referrer module defines a single copy task that always depends on assembleRelease.
        # There is no variant-suffixed task (e.g., ...AarDebug), so call the fixed task.
        gradle_task_template=':plugins:sdk-plugin-meta-referrer:adjustMetaReferrerPluginAar',
        candidate_path_templates=[
            # Direct output from assembleRelease
            os.path.join(ANDROID_META_REFERRER_DIR, 'build', 'outputs', 'aar', 'sdk-plugin-meta-referrer-release.aar'),
            # Or the copied/renamed artifact produced by adjustMetaReferrerPluginAar
            os.path.join(ANDROID_META_REFERRER_DIR, 'build', 'libs', 'sdk-plugin-meta-referrer.aar'),
        ],
        dest_path=os.path.join(ANDROID_META_REFERRER_BINDING_LIBS_DIR, 'adjust-android-meta-referrer.aar'),
        search_dir=None,
        search_prefix=None,
    )

def build_android_google_lvl():
    return _build_and_copy_aar_common(
        gradle_task_template=':plugins:sdk-plugin-google-lvl:adjustLvlPluginAar',
        candidate_path_templates=[
            os.path.join(ANDROID_GOOGLE_LVL_DIR, 'build', 'outputs', 'aar', 'sdk-plugin-google-lvl-release.aar'),
            os.path.join(ANDROID_GOOGLE_LVL_DIR, 'build', 'libs', 'sdk-plugin-google-lvl.aar'),
        ],
        dest_path=os.path.join(ANDROID_GOOGLE_LVL_BINDING_LIBS_DIR, 'adjust-android-google-lvl.aar'),
        search_dir=None,
        search_prefix=None,
    )

def has_none(from_list: list[str], in_list: list[str]) -> bool:
    return not any(arg in in_list for arg in from_list)

def build_libs(targets):
    no_sdk_target = has_none(SDKS, targets)
    if 'core' in targets or no_sdk_target:
        print('> Building Core SDK')
        build_core(targets)
    if 'oaid' in targets or 'plugins' in targets or no_sdk_target:
        print('> Building OAID SDK plugin')
        build_android_oaid()
    if 'meta_referrer' in targets or 'plugins' in targets or no_sdk_target:
        print('> Building Meta Referrer SDK plugin')
        build_android_meta_referrer()
    if 'google_lvl' in targets or 'plugins' in targets or no_sdk_target:
        print('> Building Google LVL SDK plugin')
        build_android_google_lvl()
    if 'test' in targets or no_sdk_target:
        print('> Building Test Library')
        build_test(targets)

def build_core(targets):
    no_platform_target = has_none(PLATFORMS, targets)
    if 'android' in targets or no_platform_target:
        print('> Building Android Core SDK')
        build_android_core()
    if 'ios' in targets or no_platform_target:
        print('> Building iOS Core SDK')
        build_ios_core_scripts()

def build_test(targets):
    no_platform_target = has_none(PLATFORMS, targets)
    if 'android' in targets or no_platform_target:
        print('> Building Android Test Library')
        build_android_test_library()
        print('> Building Android Test Options')
        build_android_test_options()
    if 'ios' in targets or no_platform_target:
        print('> Building iOS Test Library')
        build_ios_test_library_scripts()

def build_ios_test_library_scripts():
    """Build AdjustTestLibrary.framework using repo-provided bash scripts.

    Uses ios_sdk/scripts/build_frameworks.sh with static test library framework.
    Copies resulting AdjustTestLibrary.framework into iOS test binding folder.
    """
    ensure_paths()
    if not os.path.isdir(IOS_SDK_ROOT):
        print('Skipping iOS build (scripts): iOS SDK not found at %s' % IOS_SDK_ROOT)
        return

    # Execute the framework build script for static test library framework
    # Script expects to be run from ios_sdk root directory
    print('Before build_frameworks.sh')
    env = os.environ.copy()
    env['SDK_CODE_SIGN_IDENTITY'] = '-'
    code = run(['bash', './scripts/build_frameworks.sh', '-test'], cwd=IOS_SDK_ROOT, env=env, check=False)
    #code = run(['bash', './scripts/build_frameworks.sh', '-test-sim'], cwd=IOS_SDK_ROOT, env=env, check=False)
    print('After build_frameworks.sh (exit code: %s)' % code)

    # Preferred static test library framework output path
    static_test_library_framework = os.path.join(
        IOS_SDK_ROOT,
        'sdk_distribution',
        #'test-static-framework-simulator',
        'test-static-framework-device',
        'AdjustTestLibrary.framework'
    )

    if not os.path.isdir(static_test_library_framework):
        print('Failed to locate produced AdjustTestLibrary.framework under sdk_distribution')
        sys.exit(1)

    dest_test_library_framework = os.path.join(IOS_TEST_BINDING_DIR, 'AdjustTestLibrary.framework')
    print('Copying Test Library Framework to %s' % dest_test_library_framework)
    if os.path.isdir(dest_test_library_framework):
        shutil.rmtree(dest_test_library_framework)
    shutil.copytree(static_test_library_framework, dest_test_library_framework)
    print('Copied Test Library Framework to %s' % dest_test_library_framework)

def build_ios_core_scripts():
    """Build AdjustSdk.xcframework using repo-provided bash scripts.

    Uses ios_sdk/scripts/build_frameworks.sh with dynamic xcframeworks for iOS + tvOS.
    Copies resulting AdjustSdk.xcframework into iOS sdk binding folder.
    """
    ensure_paths()
    if not os.path.isdir(IOS_SDK_ROOT):
        print('Skipping iOS build (scripts): iOS SDK not found at %s' % IOS_SDK_ROOT)
        return

    # Execute the framework build script for dynamic xcframework (iOS + tvOS)
    # Script expects to be run from ios_sdk root directory
    print('Before build_frameworks.sh')
    env = os.environ.copy()
    env['SDK_CODE_SIGN_IDENTITY'] = '-'
    code = run(['bash', './scripts/build_frameworks.sh', '-xd', '-ios'], cwd=IOS_SDK_ROOT, env=env, check=False)
    print('After build_frameworks.sh (exit code: %s)' % code)

    dynamic_out = os.path.join(
        IOS_SDK_ROOT,
        'sdk_distribution',
        'xcframeworks-dynamic',
        'AdjustSdk-iOS-tvOS-xcframework',
        'AdjustSdk.xcframework'
    )
    produced_xcframework = None
    if os.path.isdir(dynamic_out):
        produced_xcframework = dynamic_out

    if not produced_xcframework:
        print('Failed to locate produced AdjustSdk.xcframework under sdk_distribution')
        sys.exit(1)

    dest_xcframework = os.path.join(IOS_BINDING_DIR, 'AdjustSdk.xcframework')
    if os.path.isdir(dest_xcframework):
        shutil.rmtree(dest_xcframework)
    shutil.copytree(produced_xcframework, dest_xcframework)
    print('Copied XCFramework to %s' % dest_xcframework)

def main(argv=None):
    common = argparse.ArgumentParser(add_help=False)

    common.add_argument(
        'targets',
        nargs='*',
        choices= SDKS + PLATFORMS ,
        help='Which targets (can specify multiple)'
    )

    parser = argparse.ArgumentParser(description='Build SDK libraries for MAUI bindings')
    sub = parser.add_subparsers(dest='command')
    sub.add_parser('build', help='Build specified targets', parents=[common])

    args = parser.parse_args(argv)

    # Check if a valid command was provided
    if args.command is None or args.command not in ('build',):
        parser.print_help()
        return 1

    # Now safe to access targets since command exists
    targets = args.targets

    if args.command == 'build':
        build_libs(targets)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


