from videosubtitler import *
#from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import *
#import Path

def crop(start_stamp,end_stamp,inputfile,outputfile):
	os.system('ffmpeg -y -i  "'  + inputfile + '" -ss  "' + str(start_stamp) + '" -to "' +  str(end_stamp) + '" -c copy "' + str(outputfile) + '"' )


def captioncrop(url = None, searchedword = "", subtitles_of_video_no = None, language = "en"):
    language = "en"
    subtitles_of_video_no = -1

        
    video_folder = video_subtitler(url, subtitles_of_video_no, language) 

    video = video_folder + find_video_file(video_folder)
    captionsfile = video_folder + "captions.txt"

    print('Extracting video "' + video + '" ...')


    captionLines = pickle.load(open(video_folder + 'captions.pkl', 'rb'))

    complete_str = ""
    counter = 0
    positions = []
    for cap in captionLines:
        complete_str += '\u0000' + cap['text']
        if cap['text'] == searchedword:
            positions.append(counter)
        counter += 1
    print(positions)
    counter = 0
    for position in positions:
        #ffmpeg_extract_subclip(video, second_convert(captionLines[position]["timestart"], -100),  second_convert(captionLines[position]["timeend"], 600), targetname="output/clip {0}.mp4".format(counter))
        # with ffmpeg: 
        # crop(captionLines[position]["timestart"], captionLines[position]["timeend"], video, "output/clip{0}.mp4".format(counter)
        print(captionLines[position])
        counter += 1

    vidfile = VideoFileClip(video)
    videos = []
    for position in positions:
        videos.append(vidfile.subclip(t_start = second_convert(captionLines[position]["timestart"], -1000), t_end = second_convert(captionLines[position]["timeend"], 1000)))


    final = concatenate_videoclips(videos)
    number = len(os.listdir("output/"))
    final.write_videofile("output/clip{0}.mp4".format(number))


    

#captioncrop(url = "https://www.youtube.com/watch?v=-W7GaehLsmY", searchedword = "technology")