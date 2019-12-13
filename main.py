import subprocess
# returns output as byte string
#returned_output = subprocess.check_output('yarn --version', shell=True)
#print('v:', returned_output.decode("utf-8"))

import regex
from pprint import pprint

from PyInquirer import style_from_dict, Token, prompt


questions = [
    {
        'type': 'input',
        'name': 'name',
        'message': 'What the name of the project?',
    },
    {
        'type': 'checkbox',
        'name': 'Frameworks',
        'message': 'What are you using?',
        'choices': [
            {'name': 'React'},
            {'name': 'ReactNative'},
            {'name': 'Firebase'},
        ]
    }, 
    {
        'type': 'confirm',
        'name': 'begin',
        'message': 'Begin install?',
        'default': False
    }
]

answers = prompt(questions)
print('Order receipt:')
pprint(answers)