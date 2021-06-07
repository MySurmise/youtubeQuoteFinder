from captioncropper import *

with open("links.txt", "r") as file:
    for link in file:
        try:
            captioncrop(link, "technology")
        except Exception as e:
            print(e)

    
