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


def run_cmd(cmdline):
    log('[?]  $ ' + cmdline)
    try:
        ret = subprocess.check_output(cmdline, shell=True)
        log_file('cmd succeeded ' + cmdline)
        return False, ret.decode("utf-8").strip()
    except subprocess.CalledProcessError:
        log_file('cmd error ' + cmdline)
        return True, ''


def run_cmd_external(cmdline):
    assert SYS_NAME == 'windows'
    run_cmd('start ' + cmdline)


def get_default_path():
    if SYS_NAME == 'windows':
        return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
    else:
        return os.path.join(os.path.expanduser('~'))


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


def log(msg):
    msg = str(msg)
    log_file(msg)
    print(msg)


def log_file(info):
    info = str(info)
    log_fn = os.path.join(get_temp_path(), 'kwickstart.log')
    with open(log_fn, 'a') as f:
        f.write('{}|{}|{}\n'.format(datetime.now().timestamp(), SYS_NAME, info))