import logging
import os
import subprocess
import sys

from code_manager.utils.logger import RED
from code_manager.utils.logger import RESET


class FindCommand():

    name = 'find'

    def __init__(self):
        self.color = False if self.opt.get('Commands', 'sed-colors', fallback=True) == 'false' else True

    def execute(self, args, path):

        if self.color and not args.no_color:
            color = True
        elif args.no_color:
            color = False

        if not os.path.exists(os.path.join(path, '.git')):
            find_command = ['find', '-name', args.files]
            logging.debug('Running command: [%s] in %s', ' '.join(find_command), path)
            ret = subprocess.run(find_command, stdout=subprocess.PIPE, cwd=path, check=False)
        else:
            git_command = ['git', 'ls-files', args.files]
            logging.debug('Running command: [%s] in %s', ' '.join(git_command), path)
            ret = subprocess.run(git_command, stdout=subprocess.PIPE, cwd=path, check=False)

        files = ret.stdout.splitlines()

        for file_name in files:
            if color:
                sys.stdout.buffer.write(bytes(RED + self.pack + RESET + ':', 'utf-8') + file_name + b'\n')
            else:
                sys.stdout.buffer.write(bytes(self.pack + ':', 'utf-8') + file_name + b'\n')

        sys.stdout.buffer.flush()

        return 0


ExportedClass = FindCommand
