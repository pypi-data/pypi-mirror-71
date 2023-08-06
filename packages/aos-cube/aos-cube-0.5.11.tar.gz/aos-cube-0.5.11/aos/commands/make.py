import os
import sys
import re
import subprocess
import shutil
import traceback

import click
from aos.util import *
from aos.constant import APP_INCLUDES, APP_UPDATE_MKFILE, \
                         APP_GEN_INCLUDES, NO_SDK_HINT, \
                         NO_AOSSRC_HINT
from aos.download import install_externals
from aos.usertrace.do_report import set_op, report_op

# Make command
@click.command("make", short_help="Make aos program/component",
               help="Make aos program/component.\n"\
                    "\nPlease run 'aos make help' to explore more ...")
@click.argument("targets", required=False, nargs=-1, metavar="[TARGETS...]")
@click.option("-c", "--cmd", metavar="[CMD]", help="Sub build stage for target")
def cli(targets, cmd):
    """ Make aos program/component """
    from aos import __version__
    log('aos-cube version: %s\n' % __version__)

    ret = 0
    res = 'success'

    cmd_content = ''
    if cmd:
        cmd_content += ' -c %s' % cmd
    if targets:
        cmd_content += ' ' + ' '.join(targets)

    set_op(op='make', content=cmd_content)

    make_args = ' '.join(targets)
    for arg in targets:
        if '@' in arg:
            targets = arg.split('@')
            if len(targets) < 2:
                error('Must special app and board when build aos')

            board = targets[1]
            if cmd:
                make_args = re.sub(arg, "%s.%s" % (arg, cmd), make_args)

            if board in get_scons_enabled_boards():
                scons_build(targets)
            else:
                ret = make_build(make_args)
                if ret != 0:
                    res = 'fail: return code %d' % ret

            set_op(result=res)
            report_op()

            return

    #aos make clean go here
    ret = make_build(make_args)
    if ret != 0:
        res = 'fail: return code %d' % ret

    set_op(result=res)
    report_op()

#
# Common functions
#
def download_toolchains(downloads):
    """ Download toolchains """

    tmp_dir = 'tmp_{0:02x}'.format(ord(os.urandom(1)))
    while os.path.isdir(tmp_dir):
        tmp_dir = 'tmp_{0:02x}'.format(ord(os.urandom(1)))

    try:
        os.mkdir(tmp_dir)
    except:
        error("Download toolchains failed: can not create temp folder")

    try:
        os.chdir(tmp_dir)
        for download in downloads:
            result = 0
            name, git_url, dst_dir = download
            print('Toolchain {} missing, start download ...'.format(name))
            print(git_url + ' -> ' + dst_dir)
            result += subprocess.call(['git', 'clone', '--depth=1', git_url, name])
            if result > 0:
                print('git clone toolchain {} failed'.format(name))
                print('You can mannually try fix this problem by running:')
                print('    git clone {} {}'.format(git_url, name))
                print('    mv {0}/main {1} && rm -rf {0}'.format(name, dst_dir))

            src_dir = name + '/main'
            if os.path.exists(src_dir) == False:
                print('Toolchain folder {} is not exist'.format(src_dir))
                result += 1

            if result == 0:
                if os.path.isfile(dst_dir):
                    os.remove(dst_dir)
                if os.path.isdir(dst_dir):
                    shutil.rmtree(dst_dir)
                if not os.path.isdir(os.path.dirname(dst_dir)):
                    os.makedirs(os.path.dirname(dst_dir))

                shutil.move(src_dir, dst_dir)
                print('Download toolchain {} succeed'.format(name))
            else:
                print('Download toolchain {} failed'.format(name))
    except:
        traceback.print_exc()
    finally:
        os.chdir('../')

    try:
        shutil.rmtree(tmp_dir)
    except:
        print("Toolchain auto-install error: can not remove temp folder {}, please remove it manually".format(tmp_dir))
        pass

def is_specific_path(toolchain):
    try:
        if toolchain['path_specific']:
            return True
    except KeyError as exc:
        return False
    return False

def _install_toolchains(build_args, source_root, host_os, app_root=None):
    board = None

    #check config file to be enable this function (for backward compatability)
    autodownload_enable = False
    config_file = os.path.join(source_root, "build/toolchain_config.py")
    config_file_old = os.path.join(source_root, "build/toolchain_autodownload.config")
    board_dirs = None
    if os.path.exists(config_file):
        sys.path.append(os.path.dirname(config_file))
        try:
            from toolchain_config import auto_download
        except:
            error("Import toolchain configs failed")

        if auto_download == "yes":
            autodownload_enable = True

        try:
            from toolchain_config import board_dirs
        except:
            pass

    elif os.path.exists(config_file_old):
        try:
            with open(config_file_old) as file:
                if 'yes' in file.read():
                    autodownload_enable = True
        except:
            pass

    if not autodownload_enable:
        return

    for arg in build_args:
        if '@' not in arg:
            continue
        args = arg.split('@')
        board = args[1]
        break

    if not board:
        if app_root:
            board = get_config_value("AOS_BUILD_BOARD", "%s/.config" % app_root)
        else:
            board = get_config_value("AOS_BUILD_BOARD")

    if not board:
        return

    board_dir = get_board_dir(board, source_root, board_dirs)
    if not board_dir:
        error('Can not find board {}'.format(board))

    downloads = []
    if os.path.exists(config_file):
        from toolchain_config import boards
    else:
        from aos.constant import boards

    if board in boards:
        print('Check if required tools for {} exist'.format(board))
        for toolchain in boards[board]:
            name = toolchain['name']
            command = toolchain['command']
            version = toolchain['version']

            if is_specific_path(toolchain):
                cmd_path = '{}/bin/{}'.format(toolchain['path'], command)
            else:
                cmd_path = '{}/{}/bin/{}'.format(toolchain['path'], host_os, command)

            cmd_path = os.path.join(source_root, cmd_path)
            if cmd_version_match(cmd_path, version) == True:
                continue
            if toolchain['use_global'] and cmd_version_match(command, version) == True:
                continue

            git_url = toolchain['{}_url'.format(host_os)]
            if not git_url:
                continue

            if not is_domestic():
                git_url = git_url.replace('gitee', 'github')
                git_url = git_url.replace('alios-things', 'aliosthings')

            if is_specific_path(toolchain):
                downloads.append([name, git_url, '{}'.format(os.path.join(source_root, toolchain['path']))])
            else:
                downloads.append([name, git_url, '{}/{}'.format(os.path.join(source_root, toolchain['path']), host_os)])

    if len(downloads): 
        download_toolchains(downloads)


#
# Support for scons build
#
def scons_build(args):
    if os.path.exists('ucube.py') == True:
        make_args = ['scons -j4 -f ucube.py']
    else:
        make_args = ['scons -j4 -f build/ucube.py']

    target_find = False

    for arg in args:
        if '@' in arg and not target_find:
            targets = arg.split('@')
            if len(targets) < 2:
                error('Must special app and board when build aos')

            app = 'APPLICATION='+targets[0]
            board = 'BOARD=' + targets[1]
            make_args.append(app)
            make_args.append(board)

            if len(targets) == 3:
                build_type = 'TYPE=' + targets[2]
                make_args.append(build_type)

            target_find = True
        elif arg.startswith('JOBS=') and arg.replace('JOBS=', '').isdigit() == True:
            jnum = arg.replace('JOBS=', '-j')
            make_args[0] = make_args[0].replace('-j4', jnum)
        else:
            make_args.append(arg)

    popen(' '.join(make_args), shell=True, cwd=os.getcwd())

def get_scons_enabled_boards():
    if os.path.exists("build/scons_enabled.py"):
        module_path = os.path.abspath(os.path.join('build'))
        sys.path.append(module_path)
        from scons_enabled import scons_enabled_boards
        return scons_enabled_boards
    else:
        return []

#
# Support for make build
#
def make_build(make_args):
    # build from app project
    ret, orig_dir = cd_app_root()

    if ret == 'success':
        app_root_dir = os.getcwd()
        aos_sdk_path = os.environ.get("AOS_SDK_PATH")
        if not aos_sdk_path:
            error(NO_SDK_HINT)

        if not os.path.isdir(aos_sdk_path):
            error("Can't access AOS_SDK_PATH, no such directory: %s" % aos_sdk_path)

        source_root = "SOURCE_ROOT=%s" % aos_sdk_path

        build_dir = ""
        if "BUILD_DIR" not in make_args and "BUILD_DIR" not in os.environ:
            out = os.path.join(app_root_dir, "out").replace(os.path.sep, "/")
            build_dir = "BUILD_DIR=%s" % out

        app_makefile = "APP_MAKEFILE=%s" % os.path.join(app_root_dir, "aos.mk").replace(os.path.sep, "/")
        app_dir = "APPDIR=%s" % app_root_dir

        with cd(aos_sdk_path):
            ret = _run_make(['-e', ' '.join(['-f', os.path.sep.join([aos_sdk_path, 'build', 'Makefile'])]), source_root, make_args, app_dir, build_dir])

        if os.path.isdir(orig_dir):
            os.chdir(orig_dir)

        return ret
    else:
        # build from source code
        if os.path.isdir(orig_dir):
            os.chdir(orig_dir)
        return _run_make(['-e', ' '.join(['-f', os.path.sep.join(['build', 'Makefile'])]), make_args])

def _run_make(arg_list):
    """ Build AliOS Things from source """

    # check operating system
    host_os = get_host_os()
    if not host_os:
        error('Unsupported Operating System!')

    # check source root
    source_root = ""
    for arg in arg_list:
        if "SOURCE_ROOT" in arg:
            source_root = arg.replace("SOURCE_ROOT=", "")
            break

    original_dir = ""
    if not source_root:
        ret, original_dir = cd_aos_root()
        if ret == "success":
            source_root = os.getcwd()
            source_root = locale_to_unicode(source_root)

    if not source_root:
        error("*** Fatal error! Failed to find source!\n"
              "*** Please ensure you are running 'make' command inside "
              "your project directory or AliOS Things SDK directory.")

    app_build = False
    app_root = ""

    download_externals = True
    download_toolchain = True
    target_no_toolchain = [".config", ".menuconfig", "clean", "distclean", "help", "export-keil", "export-iar", "_defconfig"]
    for arg in arg_list:
        if arg.startswith("APPDIR="):
            app_build = True
            app_root = arg.replace("APPDIR=", "")

        for target in target_no_toolchain:
            if target in arg:
                download_toolchain = False
                download_externals = False
                break

    if download_externals:
        if app_root:
            install_externals(source_root, app_root)
        else:
            install_externals(source_root)

    if download_toolchain:
        if app_root:
            _install_toolchains(sys.argv[2:], source_root, host_os, app_root)
        else:
            _install_toolchains(sys.argv[2:], source_root, host_os)

    # Update comp dependency according to head files
    if app_build and download_toolchain:
        if os.path.isfile(APP_GEN_INCLUDES):
            cmd = ["python", APP_GEN_INCLUDES, source_root, APP_INCLUDES]
            ret, err = pqueryerr(cmd)
            if ret != 0:
                if original_dir and os.path.isdir(original_dir):
                    os.chdir(original_dir)
                simple_error("Failed to generate includes, error: %s" % err.decode(get_locale()))

        if os.path.isfile(APP_UPDATE_MKFILE):
            cmd = ["python", APP_UPDATE_MKFILE, app_root]
            ret, err = pqueryerr(cmd)
            if ret != 0:
                if original_dir and os.path.isdir(original_dir):
                    os.chdir(original_dir)
                simple_error("Failed to update makefile, error: %s" % err.decode(get_locale()))

    make_cmds = {
        'Win32': os.path.sep.join(['cmd', 'win32', 'make.exe']),
        'Linux64': os.path.sep.join(['cmd', 'linux64', 'make']),
        'Linux32': os.path.sep.join(['cmd', 'linux32', 'make']),
        'OSX': os.path.sep.join(['cmd', 'osx', 'make'])
        }
    tools_dir = os.path.join(source_root, 'build')
    make_cmd = os.path.join(tools_dir, make_cmds[host_os])

    # Run make command
    make_cmd_str = ' '.join([make_cmd, 'HOST_OS=' + host_os, 'TOOLS_ROOT=' + tools_dir] + list(arg_list))
    ret = popen(make_cmd_str, shell=True, cwd=os.getcwd(), suppress_error=True)

    if original_dir and os.path.isdir(original_dir):
        os.chdir(original_dir)

    return ret
