from .util import *
from .apps import APPS
import os


class Tech:

    NAME = 'AbstractTech'
    REQUIRE = []

    def __init__(self, path, project, techs=[]):
        self.dir = path
        self.project = project
        self.techs = techs

    def setup(self):
        self.install_dependencies()
        print('[+] Setting up ' + self.NAME)
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


# class Github(Tech):

#     NAME = 'Github'
#     REQUIRE = ['Git']

#     def make(self):
#         chdir(self.dir)
#         self.nlp_path = os.path.join(self.dir, '{}-nlp'.format(self.project))
#         chdir(self.nlp_path)
#         unzip_file('nlptools.zip', self.nlp_path)
#         run_cmd('pip install virtualenv')
#         run_cmd('virtualenv nlpenv')
#         assert SYS_NAME in ['windows']
#         # run_cmd('.\\nlpenv\\Scripts\\pip.exe install numpy gensim nltk textblob spacy')
#         # run_cmd('.\\nlpenv\\Scripts\\python.exe -m textblob.download_corpora')
#         download_file('https://github.com/TxConvergentAdmin/convergent/archive/test.zip', extract_path=self.nlp_path)
#         # download_file('http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip', extract_path=self.nlp_path)
#         return True

#     def display(self):
#         chdir(self.nlp_path)
#         open_dir(self.nlp_path)
#         run_cmd_external('.\\nlpenv\\Scripts\\activate')


class React(Tech):

    NAME = 'React'
    REQUIRE = ['NodeJS', 'Yarn']

    def make(self):
        chdir(self.dir)
        err, res = run_cmd('yarn create react-app {}-react'.format(self.project))
        self.react_path = os.path.join(self.dir, self.project)
        return not err

    def display(self):
        open_dir(self.react_path)
        chdir(self.react_path)
        run_cmd_external('yarn start')


class ReactNative(Tech):

    NAME = 'React Native'
    REQUIRE = ['NodeJS', 'Expo']

    def make(self):
        chdir(self.dir)
        err, res = run_cmd('expo init -t tabs --npm --non-interactive --name {0} {0}-rn'.format(self.project))
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
        self.flask_path = os.path.join(self.dir, '{}-flask'.format(self.project))
        chdir(self.flask_path)
        unzip_file('flask.zip', self.flask_path)
        run_cmd('pip install -r requirements.txt')
        return True

    def display(self):
        chdir(self.flask_path)
        open_dir(self.flask_path)
        run_cmd_external('python app.py')


class NLPTools(Tech):

    NAME = 'NLP Tools'
    REQUIRE = ['Python']

    def make(self):
        chdir(self.dir)
        self.nlp_path = os.path.join(self.dir, '{}-nlp'.format(self.project))
        chdir(self.nlp_path)
        unzip_file('nlptools.zip', self.nlp_path)
        run_cmd('pip install virtualenv')
        run_cmd('virtualenv nlpenv')
        assert SYS_NAME in ['windows']
        run_cmd('.\\nlpenv\\Scripts\\pip.exe install numpy gensim nltk textblob spacy')
        run_cmd('.\\nlpenv\\Scripts\\python.exe -m textblob.download_corpora')
        download_file('http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip', extract_path=self.nlp_path)
        return True

    def display(self):
        chdir(self.nlp_path)
        open_dir(self.nlp_path)
        run_cmd_external('.\\nlpenv\\Scripts\\activate')


TECHS = {
    'Github': Github,
    'NLP Tools': NLPTools,
    'React': React,
    'React Native': ReactNative,
    'Flask': Flask
}