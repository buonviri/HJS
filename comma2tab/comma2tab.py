import pyperclip

cells = pyperclip.paste()  # get tab data from clipboard
pyperclip.copy(cells.replace(',', '\t'))  # replace comma with tab and place back on clipboard

# EOF
