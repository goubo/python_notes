import os

print(os.path.split(os.path.realpath(__file__))[0])

if True:
    l = 3
else:
    l = 4
print(l)

s = ''
if s:
    print(True)
else:
    print(False)
