from videosubtitler import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def crop(start_stamp,end_stamp,inputfile,outputfile):
	os.system('ffmpeg -y -i  "'  + inputfile + '" -ss  "' + str(start_stamp) + '" -to "' +  str(end_stamp) + '" -c copy "' + str(outputfile) + '"' )

video_folder = video_subtitler(url = "https://www.youtube.com/watch?v=XJ9BPE8pF-g", language = "de")



video = video_folder + find_video_file(video_folder)
captionsfile = video_folder + "captions.txt"

print('Extracting video "' + video + '" ...')

searchedword = "hund"

captionLines = pickle.load(open(video_folder + 'captions.pkl', 'rb'))
#pprint(captionLines)

complete_str = ""
counter = 0
positions = []
for cap in captionLines:
    complete_str += '\u0000' + cap['text']
    #print('\u0001')
    if cap['text'] == searchedword:
        positions.append(counter)
    counter += 1
#print(complete_str)
#print(complete_str.split("\u0000")[1:][100])
#print(captionLines[100])
print(positions)
counter = 0
for position in positions:
    ffmpeg_extract_subclip(video, second_convert(captionLines[position]["timestart"], -2500),  second_convert(captionLines[position]["timeend"], 2500), targetname="output/clip {0}.mp4".format(counter))
    # with ffmpeg: 
    # crop(captionLines[position]["timestart"], captionLines[position]["timeend"], video, "output/clip{0}.mp4".format(counter))
    print(captionLines[position])
    counter += 1

from moviepy import editor
import os
from natsort import natsorted

L =[]

for root, dirs, files in os.walk("/output"):

    #files.sort()
    files = natsorted(files)
    for file in files:
        if os.path.splitext(file)[1] == '.mp4':
            filePath = os.path.join(root, file)
            video = editor.VideoFileClip(filePath)
            L.append(video)

final_clip = editor.concatenate_videoclips(L)
final_clip.to_videofile("output.mp4", fps=24, remove_temp=False)
