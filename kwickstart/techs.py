from .util import *
from .apps import APPS
import os


class Tech:

    def __init__(self, path, project):
        self.dir = path
        self.project = project

    def setup(self):
        with PrintProgress('Setting up ' + self.NAME):
            self.install_dependencies()
            self.make()
            self.display()

    def install_dependencies(self):
        for app_name in self.REQUIRE:
            APPS[app_name].ensure_installed()

    def make(self):
        chdir(self.dir)

    def display(self):
        open_dir(self.dir)


class React(Tech):

    NAME = 'React'
    REQUIRE = ['NodeJS', 'Yarn']

    def make(self):
        chdir(self.dir)
        run_cmd('yarn create react-app ' + self.project)
        self.react_path = os.path.join(self.dir, self.project)

    def display(self):
        open_dir(self.react_path)
        chdir(self.react_path)
        run_cmd_external('yarn start')


TECHS = {
    'React': React,
}