from pathlib import Path

from pytube import YouTube
from pytube import Playlist
import os

# yt = YouTube("https://www.youtube.com/watch?v=9tp50icGhX8&list=PLrFmilN-p5i9g-htrdk4935Pt8y1wm3vq&index=26")
# audio = yt.streams.filter(only_audio=True).first()
# audio_name = audio.title
# audio.download(output_path="c:\\Users\\najsk\\Downloads", filename=audio_name)
# YouTube('https://www.youtube.com/watch?v=t5trXhAmWWk&list=PLrFmilN-p5i_2sqqzc_1ywHA8H2x6pPHc&index=52').streams.get_highest_resolution().download()

# playlist = Playlist("https://www.youtube.com/playlist?list=PLrFmilN-p5i9g-htrdk4935Pt8y1wm3vq")
# for video in playlist:
#     yt = YouTube(video)
#     audio = yt.streams.filter(only_audio=True).first()
#     audio_name = audio.title
#     audio.download(output_path="c:\\Users\\Pocitac\\Downloads", filename=audio_name)


class YTCommander:
    def __init__(self, audio_only: bool, file_path=str(os.path.join(Path.home(), "Downloads") + "\\YoutubeDownloader\\")):
        self.audio_only = audio_only
        if self.audio_only:
            self.file_path = file_path + "\\audio\\"
        else:
            self.file_path = file_path + "\\video\\"
        if not os.path.isdir(self.file_path):
            os.mkdir(self.file_path)
        # Write here all exceptions logs and after download save it to text file in self.file_path

    def rename_file_extension(self):
        """
        Called in "Main" file when program download audio from youtube and is finished.
        Method looks into directory where downloaded files are stored and chang their extension from mp4 (default) to mp3
        Every file downloaded by pytube has mp4 extension by default even if it is only audio

        """

        arr = os.listdir(self.file_path)
        for file in arr:
            new_filename = file.title()[:-3]
            if file.title().find(".mp4"):
                try:
                    os.rename(self.file_path+ file.title(), self.file_path+ new_filename + "mp3")
                except FileExistsError:
                    print("Cannot create a file when that file already exists. " + new_filename)

    def download(self, url: str):
        """
        Use this method to download video from youbube based on its url.
        Decide if url refers to video or playlist and then download it as mp3 or mp4.
        :param url: url to video
        """
        if "playlist" in url: # youtube playlist
            self.download_playlist(url)
            return
        else:
            self.download_single_link(url)

    def download_single_link(self, url):
        """
        Method downloads video from specific youtube url from arg.
        If self.audio_only is true, it downloads just mp3 of selected URL.
        Pytube may not gets correct youtube title from the appropriate url and
        instead of youtube title returns string: "YouTube". This occur randomly.
        That is why we must use loop to check if the title is correct.

        :param url: http request of youtube video we want download, obtained from GUI text inputs
        """
        try:
            while True:
                yt = YouTube(url)
                if self.audio_only:
                    video = yt.streams.filter(only_audio=True).first()
                    video_name = yt.streams[0].title
                else:
                    video = yt.streams.filter(progressive=True).get_highest_resolution()
                    video_name = video.title
                print(video_name)
                if not video_name == "YouTube":
                    break
            video.download(output_path=self.file_path, filename=str(video_name))
        except Exception as ex:
            # Just for sure, some problems with downloading may happen during downloading private video or live-stream
            # Makes sure that downloading will continue to run
            message = "Video is unable to download  {0} \n becase of: {1}".format(url,ex)
            print(message)
            with open(self.file_path+"\\log.txt", 'a') as log_file:
                log_file.write(message)

    def download_playlist(self, url: str):
        """
        Download entire yt playlist. Split and download each video one by one.
        Warning: playlist you want to download must be public!
        And maybe (it will need more test) count of videos from one playlist is max 47
        """
        playlist = Playlist(url)
        for video_name in playlist:
            self.download_single_link(video_name)
