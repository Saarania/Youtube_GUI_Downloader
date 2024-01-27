from pathlib import Path
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
import os
import threading
from YTCommander import YTCommander


def main():

    def clear_input():
        for i in range(len(inputs_text_area)):
            inputs_text_area[i].delete(0,"end")

    def get_video_count():
        """
        Returns number of yt links from input lines.
        :return: video links count
        """
        count = 0
        for i in range(len(inputs_text_area)):
            url_text = inputs_text_area[i].get()
            # text field with url is not empty and starts with http
            if url_text != "" and str(url_text).startswith("https", 0, 5):
                count = count + 1
        return count

    def download_media():
        """
        Start downloading audio from youtube using links.
        Method called after pressing 'Download!' button.
        """
        # Create progress bar
        progress_bar_value = 0
        pg_bar = Progressbar(master=root, orient=HORIZONTAL, mode="determinate", maximum=get_video_count(), length=400)
        pg_bar.place(x=50, y=725)

        audio_only = chk_var.get()
        downloader = YTCommander(audio_only= audio_only, file_path=file_path_input.get())

        for i in range(len(inputs_text_area)):
            video_url = inputs_text_area[i].get()
            if video_url == "":  # line is empty, without url
                continue
            downloader.download(video_url)
            progress_bar_value = progress_bar_value + 1
            pg_bar['value'] = progress_bar_value

        if chk_var.get():  # audio download selected
            downloader.rename_file_extension()  # rename extension for audio file (default is mp4 for some reason)
        # object imported from tkinter
        messagebox.showinfo("Downloader", "Downloading complete")
        pg_bar['value'] = 0

    def start_download():
        """
        Ensure downloading runs in a different thread.
        """
        # Daemon is set to False to ensure safe downloading even when the app is closed
        # print(threading.currentThread().getName())
        x = threading.Thread(target=download_media, daemon=False)
        x.start()

    # INITIALIZE
    root = Tk()
    root.title("Best youtube downloader")
    root.geometry("500x770")
    root.call('wm', 'attributes', '.', '-topmost', '1')
    # root.configure(background='white')
    root.resizable(0, 0)

    Label(root, text="Youtube Video Downloader", font=("Comic Sans MS", 30)).pack()

    Label(root, text="Insert our links here:", font=("Comic Sans MS", 10)).place(x=20, y=100)
    chk_var = BooleanVar()
    chk_var.set(True)
    chk = Checkbutton(root, text='Audio only', var=chk_var)
    chk.place(x=20, y=200)
    Label(root, text="Made by Sara Praks", font=("Comic Sans MS", 8)).place(x=20, y=660)
    btn = Button(root, text="Download!", bg="black", fg="white", command=start_download)
    btn.place(x=20, y=240)
    btn = Button(root, text="Clear lines", bg="black", fg="white", command=clear_input)
    btn.place(x=20, y=300)
    Label(root, text="Download dir:", font=("Comic Sans MS", 9)).place(x=20, y=365)
    string_var = StringVar(root, value=str(os.path.join(Path.home(), "Downloads")))
    file_path_input = Entry(root, width=20, textvariable=string_var)
    file_path_input.place(x=20, y=390)
    # Input
    inputs_text_area = []
    for i in range(20):
        links_input = Entry(root, width=100)
        links_input.place(x=170, y=95 + 30 * i)
        inputs_text_area.append(links_input)

    root.mainloop()


if __name__ == '__main__':
    main()
