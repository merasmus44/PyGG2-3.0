import os
print(os.curdir)
exit()
pyfiles = []
for path, subdirs, files in os.walk("./"):
    for name in files:
        if name.endswith(".py"):
            pyfiles.append(str(os.path.join(path, name)))