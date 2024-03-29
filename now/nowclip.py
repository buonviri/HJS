import os
import pyperclip

project = 'S2LP_'
extension = '.xlsx'

# import time  # hex version
from datetime import datetime  # standard format

# formatted = hex(int(time.time()))[2:].upper()  # hex version
formatted = datetime.now().strftime("%Y-%m-%d-%H%M%p")  # standard format

pyperclip.copy(project + formatted + extension)
