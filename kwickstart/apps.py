from .util import *


class App:

    NAME = 'AbstractApp'

    def ensure_installed(self):
        log('[+] Installing ' + self.NAME)
        if not self.installed:
            self.install()

    @property
    def installed(self):
        return True

    def install(self):
        pass


class Git(App):

    NAME = 'Git'

    @property
    def installed(self):
        err, version = run_cmd('git --version')
        return not err

    def install(self):
        assert SYS_NAME in ['windows', 'osx']
        if SYS_NAME == 'windows':
            fn = download_file('https://github.com/git-for-windows/git/releases/download/v2.24.1.windows.2/Git-2.24.1.2-64-bit.exe')
            run_cmd(fn + ' /VERYSILENT /NORESTART /SP-')
        elif SYS_NAME == 'osx':
            fn = download_file('https://astuteinternet.dl.sourceforge.net/project/git-osx-installer/git-2.23.0-intel-universal-mavericks.dmg')
            install_dmg(fn, 'Git 2.23.0 Mavericks Intel Universal', 'git-2.23.0-intel-universal-mavericks.pkg')

class NodeJS(App):

    NAME = 'NodeJS'

    @property
    def installed(self):
        err, version = run_cmd('node --version')
        return not err

    def install(self):
        assert SYS_NAME in ['windows', 'osx']
        if SYS_NAME == 'windows':
            fn = download_file('https://nodejs.org/dist/v12.14.0/node-v12.14.0-x64.msi')
            install_msi(fn)
        elif SYS_NAME == 'osx':
            fn = download_file('https://nodejs.org/dist/v12.14.0/node-v12.14.0.pkg')
            install_pkg(fn)


class Yarn(App):

    NAME = 'Yarn'

    @property
    def installed(self):
        err, version = run_cmd('yarn --version')
        return not err

    def install(self):
        assert SYS_NAME in ['windows', 'osx']
        if SYS_NAME == 'windows':
            fn = download_file('https://yarnpkg.com/latest.msi')
            install_msi(fn)
        elif SYS_NAME == 'osx':
            run_cmd('brew install yarn')


class Expo(App):

    NAME = 'Expo'

    @property
    def installed(self):
        err, version = run_cmd('expo --version')
        return not err

    def install(self):
        run_cmd('npm install -g expo-cli')


PY_VERSION = '3.7.4'
class Python(App):

    NAME = 'Python'

    @property
    def installed(self):
        err, version = run_cmd('python -c "import sys; print(sys.version)"')
        if not version.startswith('3.'):
            err, version = run_cmd('python3 -c "import sys; print(sys.version)"')
        return not err and version.startswith('3.')

    def install(self):
        assert SYS_NAME in ['windows', 'osx']
        if SYS_NAME == 'windows':
            fn = download_file('https://www.python.org/ftp/python/{0}/python-{0}.exe'.format(PY_VERSION))
            run_cmd(fn + ' /quiet Include_pip=1 PrependPath=1')
        elif SYS_NAME == 'osx':
            fn = download_file('https://www.python.org/ftp/python/{0}/python-{0}-macosx10.6.pkg'.format(PY_VERSION))
            install_pkg(fn)


APPS = {
    'Git': Git,
    'Yarn': Yarn,
    'NodeJS': NodeJS,
    'Expo': Expo,
    'Python': Python
}