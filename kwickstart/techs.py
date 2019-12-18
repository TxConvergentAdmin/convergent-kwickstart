from .util import *
from .apps import APPS
import os


class Tech:

    def __init__(self, path, project):
        self.dir = path
        self.project = project

    def setup(self):
        self.install_dependencies()
        success = False
        with PrintProgress('Setting up ' + self.NAME):
            success = self.make()
        if success:
            self.display()

    def install_dependencies(self):
        for app_name in self.REQUIRE:
            APPS[app_name]().ensure_installed()

    def make(self):
        chdir(self.dir)
        return True

    def display(self):
        open_dir(self.dir)


class React(Tech):

    NAME = 'React'
    REQUIRE = ['NodeJS', 'Yarn']

    def make(self):
        chdir(self.dir)
        err, res = run_cmd('yarn create react-app ' + self.project)
        self.react_path = os.path.join(self.dir, self.project)
        return not err

    def display(self):
        open_dir(self.react_path)
        chdir(self.react_path)
        run_cmd_external('yarn start')


class ReactNative(Tech):

    NAME = 'ReactNative'
    REQUIRE = ['NodeJS', 'Expo']

    def make(self):
        chdir(self.dir)
        err, res = run_cmd('expo init -t tabs --npm --non-interactive --name {0} {0}'.format(self.project))
        self.expo_path = os.path.join(self.dir, self.project)
        return not err

    def display(self):
        open_dir(self.expo_path)
        chdir(self.expo_path)
        run_cmd_external('expo start')


class Flask(Tech):

    NAME = 'Flask'
    REQUIRE = ['Python']

    def make(self):
        chdir(self.dir)
        self.flask_path = os.path.join(self.dir, 'flask')
        chdir(self.flask_path)
        unzip_file('flask.zip', self.flask_path)
        run_cmd('pip install -r requirements.txt')
        return True

    def display(self):
        chdir(self.flask_path)
        open_dir(self.flask_path)
        run_cmd_external('python app.py')


TECHS = {
    'React': React,
    'ReactNative': ReactNative,
    'Flask': Flask
}