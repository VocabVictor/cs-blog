from subprocess import Popen, PIPE

output = Popen(["git", "add","*"], stdout=PIPE, stderr=PIPE)
while True:
    line = output.stdout.readline()
    if not line:
        break
    print(line)
# Popen(["git", "commit","-m","init"], stdout=PIPE, stderr=PIPE)
# Popen(["git", "push","origin" "main"], stdout=PIPE, stderr=PIPE)

