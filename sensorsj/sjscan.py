import pprint
import yaml
import os
from subprocess import Popen, PIPE
from ast import literal_eval

# pseudo #defines
WINDOWS = os.name == 'nt'
LINUX = os.name == 'posix'


def get_sensors():
    # sensors -j returns multi-line formatted JSON
    if LINUX:
        process = Popen(["sensors", "-j"], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        sensors = stdout.decode("utf-8")
        sjdict = literal_eval(sensors)
    else:  # simulate result on Windows
        sjdict = {"FakeDevice":{"Adapter":"FakeAdapter","fan1":{"fan1_input":1234.500,"fan1_pulses":2},"SYSTIN":{"temp1_input": 12.345},"NC":{"temp2_input": 123.45}}}
    # pprint.pprint(sjdict)
    yaml = {  # blank dict for results
        'A) Fan Speed': [],
        'B) Temperature': [],
        'C) Invalid': [],
        'D) Other': [],
        }
    for i in sjdict:
        for j in sjdict[i]:
            if j in ['Adapter',]:  # list of non-sensors
                yaml['D) Other'].append([i,j,sjdict[i][j]])  # does not include value
            else:
                for k in sjdict[i][j]:
                    if k.startswith('fan') and k.endswith('input'):
                        v = sjdict[i][j][k]
                        if v > 0:  # only keep fans that are spinning
                            yaml['A) Fan Speed'].append([i,j,k,v])
                        else:  # invalid fan speed
                            yaml['C) Invalid'].append([i,j,k,v])
                    elif k.startswith('temp') and k.endswith('input'):
                        v = sjdict[i][j][k]
                        if v > 0 and v < 100:  # only temps in range
                            yaml['B) Temperature'].append([i,j,k,v])
                        else:  # invalid temperature
                            yaml['C) Invalid'].append([i,j,k,v])
                    else:  # sensor isn't fan or temp input
                        v = sjdict[i][j][k]
                        yaml['D) Other'].append([i,j,k,v])
    return yaml


if __name__ == "__main__":
    """
    csvline = get_sensors()
    print('\n'.join(csvline))
    print('Log: ' + ','.join(csvline))
    print('End of hard coded info')
    print()
    """
    sensors = get_sensors()
    pprint.pprint(sensors['A) Fan Speed'])
    pprint.pprint(sensors['B) Temperature'])
    print('Invalid Entries: ' + str(len(sensors['C) Invalid'])))
    print('Other Entries: ' + str(len(sensors['D) Other'])))
    print('See YAML for more details.')
    with open('sjscan.yaml', 'w') as f:
        yaml.dump(sensors, f)
