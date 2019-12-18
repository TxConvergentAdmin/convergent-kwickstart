from .util import *


class App:

    def ensure_installed(self):
        with PrintProgress('Installing ' + self.NAME):
            if not self.installed:
                self.install()

    @property
    def installed(self):
        return True

    def install(self):
        pass


class NodeJS(App):

    NAME = 'NodeJS'

    @property
    def installed(self):
        err, version = run_cmd('node --version')
        return not err

    def install(self):
        assert SYS_NAME in ['windows']
        fn = download_file('https://nodejs.org/dist/v12.14.0/node-v12.14.0-x64.msi')
        install_msi(fn)


class Yarn(App):

    NAME = 'Yarn'

    @property
    def installed(self):
        err, version = run_cmd('yarn --version')
        return not err

    def install(self):
        assert SYS_NAME in ['windows']
        fn = download_file('https://yarnpkg.com/latest.msi')
        install_msi(fn)


class Expo(App):

    NAME = 'Expo'

    @property
    def installed(self):
        err, version = run_cmd('expo --version')
        return not err

    def install(self):
        run_cmd('npm install -g expo-cli')


APPS = {
    'Yarn': Yarn,
    'NodeJS': NodeJS,
    'Expo': Expo
}