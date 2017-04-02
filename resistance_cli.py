#!/usr/bin/env python

import signal
import os
import sys
from pathlib import Path
from json import loads

# Secret code for exiting at a prompt
with open('secret_exit.txt', 'r') as f:
    secret_exit_code = f.read().strip()

# Hang onto a buffer to populate the screen or go back.
buffered_lines = []
buffered_inputs = []

# Hang on to whether we've printed the thing.
we_printed_it = False

# Since this is supposed to be a VI responding to input, some of the responses
# for general cases should be customizable so-as to fit Amelia's character.
with open('general_responses.json', 'r') as f:
    general_responses = loads(f.read())

'''
Commands for The Resistance's CLI.
'''
class resistance_commands:

    '''
    Makes a query to the database (i.e., looks in the query_responses folder
    for a similarly-named file).
    '''
    def query(query_string):
        # Check if such a thing exists in our 'database'.
        query_response = Path("query_responses/%s.txt" % (query_string.lower()))
        if not query_response.is_file():
            buffered_lines.append(general_responses['invalid_query'])
            print(general_responses['invalid_query'])
            return

        # Get the appropriate response.
        with open("query_responses/%s.txt" % (query_string.lower()), 'r') as f:
            response = f.read()

        # Dump it out.
        buffered_lines.append(response)
        print(response)

    '''
    Prints out help for a thing (i.e., looks in the help_messages folder for
    a similarly-named file).
    '''
    def help(command=None):
        # An empty command means we want the general help.
        if not command:
            command = 'general'

        # Check if help exists.
        help_text = Path("help_messages/%s.txt" % (command.lower()))
        if not help_text.is_file():
            buffered_lines.append(general_responses['help_not_found'] % (command))
            print(general_responses['help_not_found'] % (command))
            return

        # Get the appropriate help message.
        with open("help_messages/%s.txt" % (command.lower()), 'r') as f:
            help_message = f.read()

        # Dump it out.
        buffered_lines.append(help_message)
        print(help_message)

    '''
    Reads a 'file' that we have access to.
    '''
    def read(file_string):
        # Let's check if our 'file' exists.
        file_thing = Path("read_files/%s" % (file_string))
        if not file_thing.is_file():
            buffered_lines.append(general_responses['file_not_found'] % (file_string))
            print(general_responses['file_not_found'] % (file_string))
            return

        # Now, clear the screen. We're going to re-populate the buffer once
        # we're done here.
        os.system('clear')
        # If this is a PDF, print it to the screen.
        if file_thing.suffix == '.pdf':
            with open("read_files/%s" % (file_string), 'r') as f:
                pdf = f.read()

            print(pdf)
            print("Press Enter to continue ...")
            try:
                sys.stdin.read(1)
                os.system('clear')
            except KeyboardInterrupt:
                os.system('clear')

            # Replace our lines.
            for line in buffered_lines:
                print(line)
            return
        # Otherwise, this is a jpg.
        else:
            buffered_lines.append(general_responses['tried_to_read_png'])
            print(general_responses['tried_to_read_png'])


    '''
    Lists the 'files' available to us.
    '''
    def list():
        file_paths = [
                {
                    'path': 'read_files',
                    'message': general_responses['system_description'],
                },
                {
                    'path': '/media/usb0',
                    'message': general_responses['usb_description'],
                }
            ]
        for file_path in file_paths:
            directory = Path(file_path['path'])
            if directory.is_dir():
                buffered_lines.append(file_path['message'])
                print(file_path['message'])
                files = os.listdir(file_path['path'])
                for filename in files:
                    buffered_lines.append(filename)
                    print(filename)

            buffered_lines.append("")
            print("")
        return

    '''
    Prints out something. There's one thing, really.
    '''
    def print(file_string):
        # Kind of cheating the tiniest bit here.
        if file_string == 'Transparency Sheet.png':
            if we_printed_it:
                buffered_lines.append(general_responses['already_printed'])
                print(general_responses['already_printed'])
                return

            buffered_lines.append("Printing %s ..." % (file_string))
            print("Printing %s ..." % (file_string))
            os.system('lpr read_files/Transparency\ Sheet.png')
            we_printed_it = True
            return

        buffered_lines.append(general_responses['cannot_print'])


'''
Asks for a password, and checks it against the configured password.
'''
def attempt_authentication():
    with open('password.txt', 'r') as f:
        correct_password = f.read().strip()

    user_text = input('Password: ')
    if user_text == secret_exit_code:
        print('Exiting ...')
        exit()
    if user_text == correct_password:
        return True
    print("Incorrect password.")
    return False

'''
Asks for input and does something as a result.
'''
def accept_input():
    while True:
        # Ask for input.
        user_text = input('> ')
        # If it's the exit code, then exit.
        if user_text == secret_exit_code:
            print('Exiting ...')
            exit()
        # If it's an empty string, who cares.
        if user_text == '':
            return

        # Append the lines and input to the buffer.
        buffered_lines.append('> ' + user_text)
        buffered_inputs.append(user_text)
        # Split the input into the command and its parameters.
        split_text = user_text.split(' ', 1)
        # Take the appropriate action, potentially.
        if not hasattr(resistance_commands, split_text[0]):
            print(general_responses['command_not_found'] % (split_text[0]))
            return

        to_call = getattr(resistance_commands, split_text[0])
        try:
            if len(split_text) == 1:
                to_call()
            else:
                to_call(split_text[1].strip())
        except TypeError as e:
            print(general_responses['command_called_incorrectly'] % (split_text[0]))

'''
Hyper-hacky. We don't want users to eject on sigint/sigterm, so we're
aggressively revoking their ability to do so.
'''
def handle_sigint_or_sigterm(signum, frame):
    return

'''
Aaaaaand here we go
'''
if __name__ == '__main__':
    # Clean dat screen.
    os.system('clear')
    # Handle ejection attempts.
    signal.signal(signal.SIGINT, handle_sigint_or_sigterm)
    signal.signal(signal.SIGTERM, handle_sigint_or_sigterm)
    # Authenticate.
    authenticated = False
    while not authenticated:
        authenticated = attempt_authentication()

    # Give us a login message.
    with open('welcome_message.txt', 'r') as f:
        welcome = f.read()
        buffered_lines.append(welcome)
        print(welcome)

    # Start accepting input.
    while True:
        accept_input()
