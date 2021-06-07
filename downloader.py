def ytdownload(url, language = "en"):
    from pprint import pprint
    import requests
    import youtube_dl
    import os
    import json


    extension = "mp4"

    os.system('pip install -U youtube-dl --user')
    
    if language == "en":
        ydl = youtube_dl.YoutubeDL({'outtmpl': 'downloads/{0} - %(uploader)s/%(title)s.%(ext)s'.format(len(os.listdir('downloads'))), 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4', 'writeautomaticsub': True, 'writesubtitles': True}) # , 'http_chunk_size':'15M'
    else:
        ydl = youtube_dl.YoutubeDL({'outtmpl': 'downloads/{0} - %(uploader)s/%(title)s.%(ext)s'.format(len(os.listdir('downloads'))), 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4', 'writeautomaticsub': True, 'writesubtitles': True, 'subtitleslangs': language})
        
    with ydl:
        result = ydl.download([url])




'''
For custom download with extract info 

#print(video)
#print(json.dumps(video, indent=4))
#print(json.dumps(video["formats"], indent=4))
resolutions = {}
resolutionslist = []

#format ids: 

for format in video["formats"]:
    if format["ext"] == extension:
        try:
            resolutions[format['quality']][format['format_id']] = {'vcodec': format['vcodec'], 'url': format['url']} #if yes, append the format id, format name and url in a dict to it.
        except:
            resolutions[format['quality']] = {}
            resolutions[format['quality']][format['format_id']] = {
                                                    "vcodec": format['vcodec'], 
                                                    "url": format['url']
                } 
#if yes, append the format id, format name and url in a dict to it.

        resolutionslist.append(str(format['quality']) + ' = ' + format['url'])


#print(json.dumps(resolutions, indent=4))
highest_quality = resolutions[max(resolutions.keys())]
highest_formatid = highest_quality[max(highest_quality)]
print(highest_formatid['url'])

#pprint(resolutionslist)

'''