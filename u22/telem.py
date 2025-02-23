# formatted telemetry

with open('telem.info', 'rb') as f:
    telem = f.read()
print(telem.printable())

# EOF
