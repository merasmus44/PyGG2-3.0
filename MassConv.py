import os
pyfiles = []
blacklist = []

def walk(path):
    global pyfiles
    for path, subdirs, files in os.walk(path):
        if subdirs != []:
            for i in subdirs:
                walk(os.path.abspath(i))
        for name in files:
            if name.endswith(".py"):
                skip = False
                fullpath = str(os.path.join(path, name))
                for i in blacklist:
                    if i in fullpath:
                        skip = True
                        break
                if not skip:
                    pyfiles.append(str(os.path.join(path, name)))



walk(os.curdir)
print(pyfiles)
if not eval(input("Do you wish to continue? (y/n)")) == "y":
    exit()
for i in pyfiles:
    os.system(f"python 2to3.py -w {i}")

print("\n\n\n\nFinished converting files")