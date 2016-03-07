__author__ = 'AButz'

import colorama

def returnTest():
    return "This is some text, let's make it change colors"

print(colorama.Fore.RED + returnTest() + colorama.Fore.YELLOW + " And this should be yellow.")
print(colorama.Style.RESET_ALL + "Normal text.")