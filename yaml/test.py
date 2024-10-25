import os
import yaml  # pip install pyyaml
import pprint

filename = 'test.yaml'
# filename = 'S2LP.txt'

with open(filename) as f:
    try:
        pprint.pprint(yaml.safe_load(f))
    except:
        print('YAML Error')

os.system('PAUSE')

# EOF
