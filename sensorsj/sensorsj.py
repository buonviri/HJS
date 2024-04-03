from subprocess import Popen, PIPE

process = Popen(['sensors', '-j'], stdout=PIPE, stderr=PIPE)  # sensors -j returns JSON format
stdout, stderr = process.communicate()
sensors = stdout.decode("utf-8")

print(sensors)

# notes:
#   should we include error handling?
#   is it better to remove all the unwanted entries prior to serial transmission?
#   all we really need is a few temperatures and the fans, not all the limits and other info

# -----------------------------------------------------

# eval test for use on logging computer:
import ast
sjdict = ast.literal_eval(sensors)
for k in sjdict:
    for fan in ['fan1','fan2']:
        if fan in sjdict[k]:
            print(fan + ': ' + str(sjdict[k][fan][fan + '_input']))

