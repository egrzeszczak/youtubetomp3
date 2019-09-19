from pytube import YouTube, Playlist
from subprocess import call

import os

current_path = os.getcwd()

def youtubeToMp3(link):
    video = YouTube(link).streams.filter(file_extension='mp4').first()
    print('Downloading {}...'.format(video.default_filename))

    old = os.path.join(os.getcwd(), video.default_filename)
    new = os.path.join(os.getcwd(), os.path.splitext(video.default_filename)[0]) + ".mp3"

    print(old + "\n" + new)

    call(["mplayer", "-novideo", "-nocorrect-pts", "-ao", "pcm:waveheader", old])
    call(["lame", "-v", "audiodump.wav", new])

    # converter = VideoFileClip('test.mp4')
    # converter.audio.write_audiofile(new)
    
    # FFMPEG_VideoReader(old, print_infos=True)
    # subprocess.Popen(['ffmpeg', '-i', old, new])
    # converter = ffmpeg.input(old)
    # converter = ffmpeg.output(converter, new)
    # ffmpeg.run(converter)

    

youtubeToMp3("https://www.youtube.com/watch?v=x2tUXts-1wM")



    
