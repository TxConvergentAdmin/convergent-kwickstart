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
            'message': 'What\'s the name of the project?',
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
            'message': 'What do you want to use?',
            'choices': [dict(name=name) for name in TECHS]
        }, 
        {
            'type': 'input',
            'name': 'github',
            'default': lambda resp: 'https://github.com/TxConvergentAdmin/' + resp['name'],
            'when': lambda resp: 'Github' in resp['frameworks'],
            'message': 'What GitHub repo are you using?'
        },
        {
            'type': 'confirm',
            'name': 'begin',
            'message': 'Begin setup?',
            'default': False
        }
    ]

    resp = prompt(form)
    log_file(resp)
    if not resp.get('begin') or len(resp['frameworks']) == 0:
        log('Canceling...')
        return

    if 'github' in resp:
        resp['github'] = resp['github'].replace('.git', '')
        if os.path.basename(resp['github']) != os.path.basename(resp['path']):
            log('The project folder must match the Github repo name!')
            return

    for tech in resp['frameworks']:
        TECHS[tech](resp['path'], resp['name'], 
            techs=resp['frameworks'], github=resp.get('github')).setup()


if __name__ == '__main__':
    main()