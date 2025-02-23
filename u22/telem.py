# formatted telemetry

with open('telem.info', 'r', encoding='utf-8') as f:  # utf-8 allows non-ascii chars
    telem = f.read()
print(telem.printable())

# EOF
