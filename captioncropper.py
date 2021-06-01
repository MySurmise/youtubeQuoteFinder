from videosubtitler import *

def crop(start_stamp,end_stamp,inputfile,outputfile):
	os.system("ffmpeg -i " + inputfile + " -ss  " + str(start_stamp) + " -to " +  str(end_stamp) + " -c copy " + str(outputfile))

print(video_subtitler())
