# formatted telemetry

with open('~/telem.info', 'r') as f:
    telem = f.read()
print(telem.printable())

# EOF
