import os
from tkinter import Tk, Label, Button, Entry, filedialog
from concurrent.futures import ThreadPoolExecutor
from pytube import YouTube, Playlist, Channel

class GUI:
    def __init__(self, master, controller):
        self.controller = controller
        master.title("YouTube Downloader")

        self.step_label_1 = Label(master, text="Passo 1: Insira as URLs dos Vídeos, Playlists ou Canais (separados por vírgula):")
        self.step_label_1.pack()

        self.url_entry = Entry(master, width=50)
        self.url_entry.pack()

        self.step_label_2 = Label(master, text="Passo 2: Escolha o Local de Salvamento:")
        self.step_label_2.pack()

        self.output_entry = Entry(master, width=50, state='disabled')
        self.output_entry.pack()

        self.browse_button = Button(master, text="Procurar", command=self.controller.browse_output)
        self.browse_button.pack()

        self.step_label_3 = Label(master, text="Passo 3: Insira um nome para a nova pasta (opcional):")
        self.step_label_3.pack()

        self.folder_name_entry = Entry(master, width=50)
        self.folder_name_entry.pack()

        self.step_label_4 = Label(master, text="Passo 4: Clique para Baixar:")
        self.step_label_4.pack()

        self.download_button = Button(master, text="Baixar", command=lambda: self.controller.validate_and_download())
        self.download_button.pack()

class Downloader:
    def download_video(self, video, output_path):
        stream = video.streams.filter(progressive=True, file_extension='mp4').first()
        stream.download(output_path)

    def download_playlist(self, playlist, output_path):
        for video in playlist.videos:
            self.download_video(video, output_path)

    def download_channel(self, channel, output_path):
        for video in channel.videos:
            self.download_video(video, output_path)

class Validator:
    def __init__(self, gui, downloader):
        self.gui = gui
        self.downloader = downloader

    def validate_and_download(self):
        urls = [url.strip() for url in self.gui.url_entry.get().split(',')]
        output_path = self.gui.output_entry.get()
        folder_name = self.gui.folder_name_entry.get()

        if not urls or not output_path:
            print("Por favor, preencha ambos os campos.")
            return

        self.downloader.download_content(urls, output_path, folder_name)

class FileManager:
    def __init__(self, gui):
        self.gui = gui

    def browse_output(self):
        folder_selected = filedialog.askdirectory()
        self.gui.output_entry.config(state='normal')
        self.gui.output_entry.delete(0, 'end')
        self.gui.output_entry.insert(0, folder_selected)
        self.gui.output_entry.config(state='disabled')

class YouTubeDownloader:
    def __init__(self, master):
        self.downloader = Downloader()
        self.gui = GUI(master, self)
        self.validator = Validator(self.gui, self.downloader)
        self.file_manager = FileManager(self.gui)

    def download_content(self, urls, output_path, folder_name):
        try:
            if folder_name:
                output_path = os.path.join(output_path, folder_name)
                os.makedirs(output_path, exist_ok=True)

            with ThreadPoolExecutor(max_workers=len(urls)) as executor:
                executor.map(self.download_url, urls, [output_path] * len(urls))

            print("Downloads concluídos!")
        except Exception as e:
            print("Ocorreu um erro durante o download:", str(e))

    def download_url(self, url, output_path):
        try:
            if "playlist" in url.lower():
                playlist = Playlist(url)
                self.download_playlist(playlist, output_path)
            elif "channel" in url.lower():
                channel = Channel(url)
                self.download_channel(channel, output_path)
            else:
                video = YouTube(url)
                self.download_video(video, output_path)
        except Exception as e:
            print(f"Erro no download de {url}: {str(e)}")

    def download_video(self, video, output_path):
        self.downloader.download_video(video, output_path)

    def download_playlist(self, playlist, output_path):
        self.downloader.download_playlist(playlist, output_path)

    def download_channel(self, channel, output_path):
        self.downloader.download_channel(channel, output_path)

if __name__ == "__main__":
    root = Tk()
    downloader = YouTubeDownloader(root)
    root.mainloop()

