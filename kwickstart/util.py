import urllib.request
import subprocess
import tempfile
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
    except OSError:
        pass
    os.chdir(path)


def open_dir(path):
    if SYS_NAME == 'windows':
        os.startfile(path)


def download_file(url, name=None):
    if name is None:
        name = os.path.basename(url)
    fn = os.path.join(get_temp_path(), name)
    urllib.request.urlretrieve(url, fn)
    return fn


def install_msi(fn):
    run_cmd('"{}" /quiet /qn /norestart'.format(fn))


class PrintProgress:

    def __init__(self, prefix):
        self.prefix = prefix

    def __enter__(self):
        print(self.prefix + '...', end='')

    def __exit__(self, *args):
        print('done.')