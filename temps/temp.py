import os
from natsort import natsorted
liste = []
for file in os.listdir():
    liste.append("file '" +file + "'")

with open("convertion.txt", "w") as file:
    file.write("\n".join(natsorted(liste)))
