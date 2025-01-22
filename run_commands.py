from settings import *
from colorama import Fore, Back, Style
from commands import Commands


class RunCommands:

    def __init__(self):
        self.command_list = []
        self.commands = Commands()

        # Get all methods in class
        method_list = [func for func in dir(
            self.commands) if callable(getattr(self.commands, func))]

        # Get all the valid methods
        for method in method_list:
            # Skip python methods and special run method
            if method.startswith('__') or method == 'run':
                continue

            # Add to method list
            self.command_list.append(method)

    # Run a command in this class
    # Return success
    def run(self, command):
        if not command:
            return False

        # Parse command in separate groups
        command_groups = cmd_regex.search(command)

        # Get command name
        command_name = command_groups.group(1)

        # Verify if the command exist
        if not command_name in self.command_list:
            print(Style.RESET_ALL + Fore.RESET +
                  'System: Unable to execute command \"{}\", command is not listed as a valid command in class RunCommands.'.format(command))
            return False

        # Remove $ from the string
        command = command.replace('$', '', 1)

        # Execute the command
        try:
            eval('self.commands.' + command)
        except Exception as e:
            print(Style.RESET_ALL + Fore.RESET +
                  'System: Unable to execute method \"{}()\" because of an error:\n{}'.format(command_name, e))
            return False

        return True
