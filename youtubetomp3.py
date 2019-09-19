from pytube import YouTube, Playlist
import subprocess
import ffmpeg

import os

FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
current_path = os.getcwd()

def youtubeToMp3(link):
    video = YouTube(link).streams.filter(file_extension='mp4').first()
    print('Downloading {}...'.format(video.default_filename))

    video.download()
    old = os.path.join(os.getcwd(), video.default_filename)
    new = os.path.join(os.getcwd(), os.path.splitext(video.default_filename)[0]) + ".mp3"

    print(old + "\n" + new)


    # DONT JUDGE ME
    os.system("""{} -i "{}" "{}" """.format(FFMPEG_PATH, old, new))


    

    

youtubeToMp3("https://www.youtube.com/watch?v=BettkUR8-5w")



    
