from downloader import ytdownload
import os
import webvtt
from natsort import natsorted
from pprint import pprint
import json
try: 
    import cPickle as pickle
except ImportError:
    import pickle


def find_subtitles_file(path):
    for filename in os.listdir(path):
        if filename.endswith('.vtt'):
            return filename

def find_video_file(path):
    for filename in os.listdir(path):
        if filename.endswith('.mp4'):
            return filename

def second_convert(timestamp, delay_in_ms = 0):
    hours, minutes, seconds = timestamp.split(':')
    hours = int(hours)
    minutes = int(minutes)
    seconds = float(seconds) 
    return seconds + 60*minutes + 3600*hours + (float(delay_in_ms)/1000)

def video_subtitler(url = None, subtitles_of_video_no = None, language = "en")-> "folder":
    print(url) #WHHHHHHYY DOES THIS PRINT NONE WHEN I GIVE A URL???

    if url:
        ytdownload(url, language)
    if subtitles_of_video_no:
        videoNo = subtitles_of_video_no
    else:
        videoNo = len(os.listdir('downloads')) -1
    
    folder = 'downloads/{0}/'.format(natsorted(os.listdir('downloads'))[videoNo])
    pathToSubtitleFile = folder + find_subtitles_file(folder) 

    autoGenerateMode = False

    with open(pathToSubtitleFile, "r", encoding='utf-8') as file:
        filestr = file.read()
    if "</c>" in filestr:
        autoGenerateMode = True

    captionLines = []
    first_stamp_found = False
    linecounter = 0 # Linecounter starting from 1

    if autoGenerateMode:
        for line in filestr.split("\n"):
            linecounter += 1
            if linecounter <= 4:
                continue

            if not first_stamp_found:
                if "-->" in line:
                    first_stamp = line.split("-->")[0].strip()
                    first_stamp_end = line.split("-->")[1].strip().split(" ")[0].strip()
                    first_stamp_found = True
            else:
                if "-->" in line:
                        last_stamp = line.split("-->")[0].strip()
                        last_stamp_end = line.split("-->")[1].strip().split(" ")[0].strip()

            if "</c>" in line:
                line = line.replace("</c>", " ")
                line = line.replace(" ", "")
                for caption in line.split("<c>"):
                    try:
                        caption = caption.split("<")
                        captiontext = caption[0]
                    except:
                        #print("Didn't split", caption, "in", line)
                        captiontext = caption
                    try:
                        timeend = caption[1].replace(">", "")
                    except:
                        #print("Didn't find timestamp in caption", caption, "in", line)
                        timeend = last_stamp_end
                    if captionLines:
                        captionLines.append({'timestart': captionLines[-1]['timeend'], 'timeend': timeend, 'text': captiontext})
                    else:
                        captionLines.append({'timestart': first_stamp, 'timeend': first_stamp_end, 'text': captiontext})

            elif len(line.split(" ")) == 1 and line != "":
                #print("Line: ", [line])
                if not captionLines:
                    captionLines.append({'timestart': first_stamp, 'timeend': first_stamp_end, 'text': line})
                else:
                    if captionLines[-1]['text'].split(" ")[-1] != line:
                        captionLines.append({'timestart': captionLines[-1]['timeend'], 'timeend': last_stamp_end, 'text': line})
    else:
        for caption in webvtt.read(pathToSubtitleFile):
            captionLines.append({'timestart': caption.start, 'timeend': caption.end, 'text': caption.text})
    
    #pkl file
    pickle.dump(captionLines, open(folder + 'captions.pkl', 'wb'))
    
    # human readable file
    with open(folder + 'captions.txt', 'w', encoding = 'utf-8') as filehandle:
        for caption in captionLines:
            filehandle.write('%s\n' % caption)
    
    return folder
video_subtitler()