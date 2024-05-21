from subprocess import Popen, PIPE

os_command = ['cat', '/sys/devices/virtual/dmi/id/board_vendor']
process = Popen(os_command, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
info = stdout.decode("utf-8")
print(info)

# EOF
