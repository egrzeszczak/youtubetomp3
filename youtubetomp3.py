from pytube import YouTube, Playlist
import os

ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"
current_path = os.getcwd()
console_header = "_"*60 + " [ YT to MP3 Converter ]\n"
current_collection = list(os.path.splitext(x)[0] for x in os.listdir(current_path) if x.endswith('.mp3'))
logo =  r"""
                      __        __            __                          _____
   __  ______  __  __/ /___  __/ /_  ___     / /_____     ____ ___  ____ |__  /
  / / / / __ \/ / / / __/ / / / __ \/ _ \   / __/ __ \   / __ `__ \/ __ \ /_ < 
 / /_/ / /_/ / /_/ / /_/ /_/ / /_/ /  __/  / /_/ /_/ /  / / / / / / /_/ /__/ / 
 \__, /\____/\__,_/\__/\__,_/_.___/\___/   \__/\____/  /_/ /_/ /_/ .___/____/  
/____/                                                          /_/            
"""
def youtubeToMp3(link):
    # Getting video
    video = YouTube(link).streams.filter(file_extension='mp4').first()

    if not os.path.splitext(video.default_filename)[0] in current_collection:
        print('GETTING FILE: {}'.format(video.default_filename))
        video.download()
        # <path>.mp4
        old = os.path.join(os.getcwd(), video.default_filename)
        # <path>.mp3
        new = os.path.join(os.getcwd(), os.path.splitext(video.default_filename)[0]) + ".mp3"

        # Using FFMPEG to convert
        os.system("""{} -loglevel panic -i "{}" "{}" """.format(ffmpeg_path, old, new))
        # Erase mp4 file
        os.remove(old)

        print("Done")
    else:
        print('FILE {} already in current directory'.format(os.path.splitext(video.default_filename)[0]))


def playlistToMp3(link):
    showCurrentCollection()
    # Getting playlist
    playlist = Playlist(link, suppress_exception=True)
    # Generate video urls    
    playlist.populate_video_urls()

    if len(playlist.video_urls) > 0:
        # Working
        print(console_header + "PLAYLIST: {} with {} videos".format(playlist.playlist_url, len(playlist.video_urls)))
        for link in playlist.video_urls:
            youtubeToMp3(link)
    else:
        # Doesn't have videos or playlist private
        print(console_header + "PLAYLIST: {} doesn't have videos / is private / doesn't exist".format(playlist.playlist_url))

    print()
def showCurrentCollection():
    print(console_header + 'CURRENT COLLECTION in {}: '.format(current_path))
    for item in current_collection:
       print(item)

if __name__ == "__main__":
    print(logo)
    
    while True:
        option = input(console_header + "Do you want download video or playlist? (video/playlist/exit): ")
        if option.upper().startswith("V"):
            youtubeToMp3(str(input("VIDEO > ENTER LINK: ")))
        elif option.upper().startswith("P"):
            playlistToMp3(str(input("PLAYLIST > ENTER LINK: ")))
        elif option.upper().startswith("SH"):
            showCurrentCollection()
        else:
            exit()
        

    

