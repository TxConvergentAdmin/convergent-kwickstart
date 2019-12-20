from .util import *
from .apps import APPS
import os


class Tech:

    NAME = 'AbstractTech'
    REQUIRE = []

    def __init__(self, path, project, techs=[], github=None):
        self.dir = path
        self.project = project
        self.techs = techs
        self.github = github

    def setup(self):
        self.install_dependencies()
        log('[+] Setting up ' + self.NAME)
        if self.make():
            self.display()

    def install_dependencies(self):
        for app_name in self.REQUIRE:
            APPS[app_name]().ensure_installed()

    def make(self):
        chdir(self.dir)
        return True

    def display(self):
        open_dir(self.dir)


GIT_IGNORE = """
node_modules/
__pycache__/
*.pyc
*.zip
"""
class Github(Tech):

    NAME = 'Github'
    REQUIRE = ['Git']

    def make(self):
        chdir(os.path.join(self.dir, '..'))
        run_cmd('git clone {}'.format(self.github))
        chdir(self.dir)
        run_cmd('git checkout -b {}-edits'.format(get_username()))

        ignore_fn = os.path.join(self.dir, '.gitignore')
        if not os.path.exists(ignore_fn):
            with open(ignore_fn, 'w') as f:
                f.write(GIT_IGNORE)

        return True

    def display(self):
        pass


class React(Tech):

    NAME = 'React'
    REQUIRE = ['NodeJS', 'Yarn']

    def make(self):
        chdir(self.dir)
        self.react_path = os.path.join(self.dir, self.project)
        install_cmd = 'yarn create react-app {}-react'.format(self.project)
        if os.path.exists(self.react_path):
            chdir(self.react_path)
            install_cmd = 'yarn install'
        err, res = run_cmd(install_cmd)
        return not err

    def display(self):
        open_dir(self.react_path)
        chdir(self.react_path)
        run_cmd('yarn start', external=True)


class ReactNative(Tech):

    NAME = 'React Native'
    REQUIRE = ['NodeJS', 'Expo']

    def make(self):
        chdir(self.dir)
        install_cmd = 'expo init -t tabs --npm --non-interactive --name {0} {0}-rn'.format(self.project)
        self.expo_path = os.path.join(self.dir, self.project)
        if os.path.exists(self.react_path):
            chdir(self.expo_path)
            install_cmd = 'npm install'
        err, res = run_cmd(install_cmd)
        return not err

    def display(self):
        open_dir(self.expo_path)
        chdir(self.expo_path)
        run_cmd('expo start', external=True)


class Flask(Tech):

    NAME = 'Flask'
    REQUIRE = ['Python']

    def make(self):
        chdir(self.dir)
        self.flask_path = os.path.join(self.dir, '{}-flask'.format(self.project))
        exists = os.path.exists(self.flask_path)
        chdir(self.flask_path)
        if not exists:
            unzip_file('flask.zip', self.flask_path)
        run_cmd('pip install -r requirements.txt', correct_python=True)
        return True

    def display(self):
        chdir(self.flask_path)
        open_dir(self.flask_path)
        run_cmd('python app.py', correct_python=True, external=True)


class NLPTools(Tech):

    NAME = 'NLP Tools'
    REQUIRE = ['Python']

    def make(self):
        assert SYS_NAME in ['windows', 'osx']
        chdir(self.dir)
        self.nlp_path = os.path.join(self.dir, '{}-nlp'.format(self.project))
        chdir(self.nlp_path)
        unzip_file('nlptools.zip', self.nlp_path)
        run_cmd('pip install virtualenv', correct_python=True)
        run_cmd('python -m virtualenv nlpenv')
        if SYS_NAME == 'windows':
            pyext = '.exe'
        else:
            pyext = ''
        run_cmd('.\\nlpenv\\Scripts\\pip{} install numpy gensim nltk textblob spacy'.format(pyext))
        run_cmd('.\\nlpenv\\Scripts\\python{} -m textblob.download_corpora'.format(pyext))
        download_file('http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip', extract_path=self.nlp_path)
        return True

    def display(self):
        chdir(self.nlp_path)
        open_dir(self.nlp_path)
        run_cmd('.\\nlpenv\\Scripts\\activate', external=True)


# The order here matters (Github should be first)
TECHS = {
    'Github': Github,
    'NLP Tools': NLPTools,
    'React': React,
    'React Native': ReactNative,
    'Flask': Flask
}