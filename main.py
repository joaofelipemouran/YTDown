import os
from tkinter import Tk, Label, Button, Entry, StringVar, filedialog, ttk
from pytube import YouTube

class YouTubeDownloader:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Downloader")

        self.url_label = Label(master, text="URL do Vídeo:")
        self.url_label.pack()

        self.url_entry = Entry(master, width=50)
        self.url_entry.pack()

        self.output_label = Label(master, text="Local de Salvamento:")
        self.output_label.pack()

        self.output_entry = Entry(master, width=50, state='disabled')
        self.output_entry.pack()

        self.browse_button = Button(master, text="Procurar", command=self.browse_output)
        self.browse_button.pack()

        self.download_button = Button(master, text="Baixar Vídeo", command=self.download_video)
        self.download_button.pack()

    def browse_output(self):
        folder_selected = filedialog.askdirectory()
        self.output_entry.config(state='normal')
        self.output_entry.delete(0, 'end')
        self.output_entry.insert(0, folder_selected)
        self.output_entry.config(state='disabled')

    def download_video(self):
        url = self.url_entry.get()
        output_path = self.output_entry.get()

        if not url or not output_path:
            print("Por favor, preencha ambos os campos.")
            return

        try:
            self.yt = YouTube(url)
            video = self.yt.streams.filter(progressive=True, file_extension='mp4').first()

            self.progress_bar['maximum'] = video.filesize
            video.download(output_path, on_progress_callback=self.update_progress)
            print("Download concluído!")
        except Exception as e:
            print("Ocorreu um erro durante o download:", str(e))

if __name__ == "__main__":
    root = Tk()
    downloader = YouTubeDownloader(root)
    root.mainloop()
