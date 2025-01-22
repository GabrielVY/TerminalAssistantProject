import re

# REGEX ATTEMPTS
# \$(?![1-9])[a-zA-z1-9]*\((.*?)\)$
# \$((?![1-9])[a-zA-z1-9]*)\((.*?)\)$
# (?:^|\s)\$((?![1-9])[a-zA-z1-9]*)\((.*?)\)$
# (?:^|\s)\$((?![1-9])[a-zA-z1-9]*)\((.*?)\)(?=\s|$)
# (?:(?<=^)|(?<=\s))\$((?![1-9])[a-zA-z1-9]*)\((.*?)\)(?=\s|$)

# This website helped me a lot to debug https://regex101.com
# Regex to get the command in the message
# get commands in this format
# $command(parameters)
# Can get anywhere on the text
_regex = r'(?:(?<=^)|(?<=\s))\$((?![1-9])[a-zA-z1-9]*)\((.*?)\)(?=\s|$)'
cmd_regex = re.compile(_regex)

# Used to remove commands from the message, gets the regex + 1 blankspace character
_regex = r'(?:(?<=^)|(?:\s))\$((?![1-9])[a-zA-z1-9]*)\((.*?)\)(?=\s|$)'
cmd_cleaner = re.compile(_regex)
