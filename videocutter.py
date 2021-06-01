from downloader import ytdownload
import os
import webvtt
from natsort import natsorted
from pprint import pprint

def crop(start_stamp,end_stamp,inputfile,outputfile):
	os.system("ffmpeg -i " + inputfile + " -ss  " + str(start_stamp) + " -to " +  str(end_stamp) + " -c copy " + str(outputfile))

def find_subtitles_file(path):
    for filename in os.listdir(path):
        if filename.endswith('.vtt'):
            return filename

def find_video_file(path):
    for filename in os.listdir(path):
        if filename.endswith('.mp4'):
            return filename

def second_convert(timestamp):
    hours, minutes, seconds = timestamp.split(':')
    hours = int(hours)
    minutes = int(minutes)
    seconds = float(seconds) 
    return seconds + 60*minutes + 3600*hours

#ytdownload("https://www.youtube.com/watch?v=I7vuVlUOYcs")

#videoNo = len(os.listdir('downloads')) -1
videoNo = 2

pathToSubtitleFile = 'downloads/{0}/{1}'.format(natsorted(os.listdir('downloads'))[videoNo], find_subtitles_file('downloads/{0}'.format( natsorted(os.listdir('downloads'))[videoNo])))

autoGenerateMode = False

searchedWord = "genius"

with open(pathToSubtitleFile, "r", encoding='utf-8') as file:
    filestr = file.read()
if "</c>" in filestr:
            autoGenerateMode = True

if autoGenerateMode:
    prevline = "\n"
    wantedLines = []
    filestr = filestr.split('\n\n')

    for lines in filestr:
        if "</c>" in lines:
            filestr.remove(lines)
        else:
            if "-->" in lines:
                lineslist = lines.split('\n')
                for line in lineslist:
                    if "-->" in line:
                        line = ' '.join(line.split(' ')[:3])
                        if prevline != "\n":
                            print(prevline)
                    #wantedLines.append("\n")
                    print(prevline)
                    print(line)
                    print("-----------------")
                    wantedLines.append(line)
                    prevline = line

    #pprint(filestr)
    wantedLines = '\n'.join(wantedLines).split('\n \n')
    newwantedlines = ['WEBVTT\nKind: captions\nLanguage: en-GB\n']
    print(wantedLines)
    for lines in wantedLines:
        if any("-->" in line for line in lines.split('\n')):
            newwantedlines.append("\n".join(lines.split('\n')[:-2]))
        else:
            print(lines)
    
    for lines in newwantedlines:
        if any("-->" in line for line in lines.split('\n')):
            pass
        else:
            newwantedlines.remove(lines)
    newwantedlines = ['WEBVTT\nKind: captions\nLanguage: en-GB\n'] + newwantedlines
    for lines in newwantedlines:
        if any("-->" in line for line in lines.split('\n')):
            pass
        else:
            newwantedlines.remove(lines)
    newwantedlines = ['WEBVTT\nKind: captions\nLanguage: en-GB\n'] + newwantedlines
    for lines in newwantedlines:
        if any("-->" in line for line in lines.split('\n')):
            pass
        else:
            newwantedlines.remove(lines)
    newwantedlines = ['WEBVTT\nKind: captions\nLanguage: en-GB\n'] + newwantedlines


    with open("temp.vtt", "w") as file:
        file.write("\n \n".join(newwantedlines))
    pathToSubtitleFile = 'temp.vtt'
    
partfiles = []
counter = 0
for caption in webvtt.read(pathToSubtitleFile):
    if searchedWord in caption.text:
        counter += 1
        print(caption.text)
        print(second_convert(caption.start))
        video = 'downloads/{0}/{1}'.format(natsorted(os.listdir('downloads'))[videoNo], find_video_file('downloads/{0}'.format( natsorted(os.listdir('downloads'))[videoNo])))
        print(video)
        video = '"' + video + '"'
        print(video)
        print(caption.start, caption.end)
        crop(second_convert(caption.start) - 2, second_convert(caption.end), video,  '"output/Number {0}.mp4"'.format(counter))
        partfiles.append("file 'output/Number {0}.mp4'".format(counter))
        print(caption.text)



with open('list.txt', "w") as file:
    file.write("\n".join(partfiles))
    os.system('"ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4"')

#if os.path.exists("temp.vtt"):
#    os.remove("temp.vtt")