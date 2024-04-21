import os
import yaml  # pip install pyyaml

with open("test.yaml") as f:
    try:
        print(yaml.safe_load(f))
    except:
        print('YAML Error')

os.system('PAUSE')

# EOF
