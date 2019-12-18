from kwickstart.techs import TECHS
from kwickstart.util import *
from PyInquirer import prompt
import os


def main():

    form = [
        {
            'type': 'input',
            'name': 'name',
            'default': 'cvgt-project',
            'message': 'What the name of the project?',
        },
        {
            'type': 'input',
            'name': 'path',
            'default': lambda resp: os.path.join(get_default_path(), resp['name']),
            'message': 'Where should it be?',
        },
        {
            'type': 'checkbox',
            'name': 'frameworks',
            'message': 'What are you using?',
            'choices': [dict(name=name) for name in TECHS]
        }, 
        {
            'type': 'confirm',
            'name': 'begin',
            'message': 'Begin setup?',
            'default': False
        }
    ]

    resp = prompt(form)
    if not resp['begin'] or len(resp['frameworks']) == 0:
        print('Canceling...')
        return

    for tech in resp['frameworks']:
        TECHS[tech](resp['path'], resp['name']).setup()


if __name__ == '__main__':
    main()