import urllib.request
import subprocess
import tempfile
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
    print('[?]  $ ' + cmdline)
    try:
        ret = subprocess.check_output(cmdline, shell=True)
        return False, ret.decode("utf-8").strip()
    except subprocess.CalledProcessError:
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


def chdir(path):
    try:
        os.mkdir(path)
    except OSError as e:
        pass
    os.chdir(path)


def open_dir(path):
    if SYS_NAME == 'windows':
        os.startfile(path)


def download_file(url, name=None):
    print('[?]  Loading ' + url)
    if name is None:
        name = os.path.basename(url)
    fn = os.path.join(get_temp_path(), name)
    urllib.request.urlretrieve(url, fn)
    return fn


def unzip_file(zip_name, output_path):
    print('[?]  Loading ' + zip_name)
    input_path = os.path.join(os.path.dirname(__file__), 'templates', zip_name)
    with zipfile.ZipFile(input_path, 'r') as zip_ref:
        zip_ref.extractall(output_path)


def install_msi(fn):
    run_cmd('"{}" /quiet /qn /norestart'.format(fn))