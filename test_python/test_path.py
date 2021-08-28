import os

print(os.path.split(os.path.realpath(__file__))[0])

test = False
print(test)


def testB(B):
    B = not B


testB()

print(test)
