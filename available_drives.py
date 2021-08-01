import string
import os

def system_drives():
    """ Find the different drives located in the system

        Args:
            Does not take any arguments

        Returns:
            available_drives: A list of all available drives in the system
    """
    # Runs a list through all uppercase alphabets and stores values which are drives
    available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
    print("The system is searching for your files...")
    return available_drives
