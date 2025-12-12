# Intention here is to be a cli tool for fine grained interactive operations

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

nouns = {
    'autex',
    'cnpj',
    'dof',
    'plans',
    'transport'
}

verbs = {
    'download',
    'ingest'
}

def valid_pair(n: str, v: str):
    if not n in nouns:
        return False 
    if not v in verbs:
        return False
    return True

def prompt():
    print('Action?')
    cmd = input()
    return verify_command(cmd)
    

def verify_command(cmd: str):
    noun, verb = cmd.split()
    if not valid_pair(noun, verb):
        if not noun in nouns: 
            print(f'{noun} not a recognized command, try one of: {', '.join([n for n in nouns])}')
        elif not verb in verbs:
            print(f'{verb} not a recognized action, try one of: {', '.join([v for v in verbs])}')
        return prompt()
    else:       
        return [noun, verb]

def cli(args: list[str] | None):
    if args:
       return verify_command(' '.join(args))
    else:
        return prompt()