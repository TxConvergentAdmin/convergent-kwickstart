from datetime import datetime
import urllib.request
import subprocess
import tempfile
import getpass
import zipfile
import sys
import os


SYS_NAME = {
    'linux': 'linux',
    'linux2': 'linux',
    'darwin': 'osx',
    'win32': 'windows',
    'win64': 'windows'
}[sys.platform]


def run_cmd(cmdline, external=False, correct_python=False):
    if correct_python:
        suffix = get_python_suffix()
        cmdline = cmdline.replace('pip ', 'pip' + suffix + ' ')
        cmdline = cmdline.replace('python ', 'python' + suffix + ' ')
    log('[?]  $ ' + cmdline)
    if not external:
        try:
            ret = subprocess.check_output(cmdline, shell=True)
            output = ret.decode("utf-8").strip()
            log_file('cmd succeeded ' + cmdline + '\n' + output)
            return False, ret.decode("utf-8").strip()
        except subprocess.CalledProcessError:
            log_file('cmd error ' + cmdline)
            return True, ''
    else:
        _run_cmd_external(cmdline)
        return False, ''


def _run_cmd_external(cmdline, _save={'cnt': 0}):
    assert SYS_NAME in ['windows', 'osx']
    _save['cnt'] += 1
    if SYS_NAME == 'windows':
        run_cmd('start ' + cmdline)
    elif SYS_NAME == 'osx':
        temp_script_fn = os.path.join(os.getcwd(), 'kwickstart-script-{}.sh'.format(_save['cnt']))
        with open(temp_script_fn, 'w') as f:
            f.write('#!/bin/bash\ncd {}\n{}\n'.format(os.getcwd(), cmdline))
        run_cmd('chmod +x ' + temp_script_fn)
        run_cmd('open -a Terminal.app "{}"'.format(temp_script_fn))


def get_python_suffix(_save={}):
    if 'return' in _save:
        return _save['return']
    for suffix in ['', '3', '3.8']:
        err, version = run_cmd('python{} -c "import sys; print(sys.version)"'.format(suffix))
        if version.startswith('3.'):
            _save['return'] = suffix
            return suffix
    return ''


def get_default_path():
    if SYS_NAME == 'windows':
        return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
    else:
        return os.path.join(os.path.expanduser('~'), 'Desktop')


def get_temp_path():
    return tempfile.gettempdir()


def get_username():
    return getpass.getuser().lower()


def chdir(path):
    try:
        os.mkdir(path)
    except OSError as e:
        pass
    os.chdir(path)


def open_dir(path):
    if SYS_NAME == 'windows':
        os.startfile(path)


def download_file(url, name=None, extract_path=None):
    log('[?]  Loading ' + url)
    if name is None:
        name = os.path.basename(url)
    fn = os.path.join(get_temp_path(), name)
    urllib.request.urlretrieve(url, fn)
    if fn.endswith('.zip') and extract_path is not None:
        with zipfile.ZipFile(fn, 'r') as zip_ref:
            zip_ref.extractall(os.path.join(extract_path, name.replace('.zip', '')))
    return fn


def unzip_file(zip_name, output_path):
    log('[?]  Loading ' + zip_name)
    input_path = os.path.join(os.path.dirname(__file__), 'templates', zip_name)
    with zipfile.ZipFile(input_path, 'r') as zip_ref:
        zip_ref.extractall(output_path)


def install_msi(fn):
    run_cmd('"{}" /quiet /qn /norestart'.format(fn))


def install_pkg(fn):
    run_cmd('sudo -S installer -allowUntrusted -verboseR -pkg "{}" -target /'.format(fn))


def install_dmg(fn, volume_name, pkg_name):
    run_cmd('hdiutil attach {}'.format(fn))
    volume_path = os.path.join('/Volumes', volume_name)
    install_pkg(os.path.join(volume_path, pkg_name))
    run_cmd('hdiutil detach {}'.format(volume_path))


def log(msg):
    msg = str(msg)
    log_file(msg)
    print(msg)


def log_file(info):
    info = str(info)
    log_fn = os.path.join(get_temp_path(), 'kwickstart.log')
    with open(log_fn, 'a') as f:
        f.write('{}|{}|{}\n'.format(datetime.now().timestamp(), SYS_NAME, info))