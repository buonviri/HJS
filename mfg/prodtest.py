from subprocess import Popen, PIPE
import ast

process = Popen(['bmc'], stdout=PIPE, stderr=PIPE)  # sensors -j returns JSON format
stdout, stderr = process.communicate()
sensors = stdout.decode("utf-8")

print('SENSORS')
print(sensors)

# notes:
#   should we include error handling?
#   is it better to remove all the unwanted entries prior to serial transmission?
#   all we really need is a few temperatures and the fans, not all the limits and other info

# -----------------------------------------------------

# eval test for use on logging computer:
prodtest = sensors
print('PRODTEST')
print(prodtest)

# EOF
