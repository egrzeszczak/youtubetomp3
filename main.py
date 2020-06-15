import math, os
import pytube, tkinter, copy, urllib

#define
CURRENT_PATH = os.getcwd()
WINDOW = tkinter.Tk()
WINDOW.title(f"youtoo in {CURRENT_PATH}")

def convertSize(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])
def showDebug(message):
    os.system(f"echo \'\033[0;34m[DEBUG]:\033[0m {message}\'")   

class App():
    def goDownloadMP3(self, stream, footerFrame):
        filename = stream.default_filename
        stream.download()
        old = os.path.join(CURRENT_PATH, filename)
        new = os.path.join(CURRENT_PATH, os.path.splitext(filename)[0]) + ".mp3"
        os.system("""ffmpeg -i "{}" "{}" """.format(old, new))
        os.remove(old)
        os.system("printf '\7'")
        self.displayInfoFooter(footerFrame, "Sukces {}".format(new))

    def goDownload(self, stream, footerFrame):
        filename = stream.default_filename
        stream.download()
        os.system("printf '\7'")
        self.displayInfoFooter(footerFrame, "Suckes {}".format(filename))

    def goSubmit(self, urlInput, headerFrame, resultFrame, footerFrame):
        # Wyczyść wyniki
        for child in headerFrame.winfo_children():
            child.destroy()
        for child in resultFrame.winfo_children():
            child.destroy()
        
        # Pobierz adres URL
        urlGiven = urlInput.get()
        
        # kontra RegexMatchError 
        try:
            # youtubeHandler
            youtubeHandler = pytube.YouTube(urlGiven)

            # headerFrame zawierająca tytuł filmu i nazwę autora
            tkinter.Label(headerFrame, text=str(youtubeHandler.title), padx=5, pady=5).grid(row=0, column=0)
            tkinter.Label(headerFrame, text=str(youtubeHandler.author), padx=5, pady=5).grid(row=0, column=1)
            
            # Lista przycisków Video, MP3
            buttonsVideo, buttonsMP3 = list(), list()
            for index, stream in enumerate(youtubeHandler.streams.filter().order_by('resolution').desc(), start=0):
                # Rozmiar pliku
                filesize = stream.filesize
                # Kodeki video i audio
                vcodec, acodec = stream.parse_codecs()
                # Rozdzielczość
                resolution = stream.resolution
                # Wyświetl wyniki do resultFrame
                tkinter.Label(resultFrame, width=10, text=str(stream.mime_type)).grid(row=index+3, column=0)
                tkinter.Label(resultFrame, width=10, text=str(resolution)).grid(row=index+3, column=1)
                tkinter.Label(resultFrame, width=10, text=str(vcodec)).grid(row=index+3, column=2)
                tkinter.Label(resultFrame, width=10, text=str(acodec)).grid(row=index+3, column=3)
                tkinter.Label(resultFrame, width=10, text=str(convertSize(filesize))).grid(row=index+3, column=4)
                # Dodaj przyciski do list
                if(str(vcodec) == str(None)):
                    buttonsVideo.append(tkinter.Button(resultFrame, width=10, state=tkinter.DISABLED, text="No codec"))
                else:
                    buttonsVideo.append(tkinter.Button(resultFrame, width=10, text="Video", command= lambda stream=stream: self.goDownload(stream, footerFrame)))
                if(str(acodec) == str(None)):
                    buttonsMP3.append(tkinter.Button(resultFrame, width=10, state=tkinter.DISABLED, text="No codec"))
                else:
                    buttonsMP3.append(tkinter.Button(resultFrame, width=10, text="MP3", command= lambda stream=stream: self.goDownloadMP3(stream, footerFrame)))
                
                    
            # Przyciski video
            for index, button in enumerate(buttonsVideo, start=0):
                button.grid(row=index+3, column=5)
            # Przyciski mp3
            for index, button in enumerate(buttonsMP3, start=0):
                button.grid(row=index+3, column=6)
            # Wyświetl sukces na footerFrame
            self.displayInfoFooter(footerFrame, "Sukces! Wyświetlanie {} wyników".format(len(buttonsVideo)))
                
        # RegexMatchError
        except pytube.exceptions.RegexMatchError as error:
            print("Error: " + str(error))
            self.displayInfoFooter(footerFrame, "Error: " + str(error))
        except urllib.error.HTTPError as error:
            self.displayInfoFooter(footerFrame, "Error: " + str(error))

    # Clear
    def set_text(self, inputElement, newText):
        inputElement.delete(0, tkinter.END)
        inputElement.insert(0, newText)

    # Info
    def displayInfoFooter(self, footerFrame, infoText):
        for child in footerFrame.winfo_children():
            child.destroy()
        label = tkinter.Label(footerFrame, text=str(infoText))
        label.pack()

    def __init__(self):
        # Div
        mainForm = tkinter.Frame(WINDOW)
        headerFrame = tkinter.Frame(WINDOW)
        resultFrame = tkinter.Frame(WINDOW)
        footerFrame = tkinter.Frame(WINDOW)
        
        # mainForm
        urlLabel = tkinter.Label(mainForm, width=10, text="Adres URL")
        urlInput = tkinter.Entry(mainForm, width=40)
        urlSubmit = tkinter.Button(mainForm, width=10, text="Szukaj", command= lambda: self.goSubmit(urlInput, headerFrame, resultFrame, footerFrame))
        clearSubmit = tkinter.Button(mainForm, widt=10, text="Wyczyść", command= lambda: self.set_text(urlInput, ""))
        
        # Draw
        urlLabel.grid(row=0, column=0)
        urlInput.grid(row=0, column=1)
        urlSubmit.grid(row=0, column=2)
        clearSubmit.grid(row=0, column=3)

        mainForm.pack(padx=5, pady=5)
        headerFrame.pack(padx=5, pady=5)
        resultFrame.pack(padx=5, pady=5)
        footerFrame.pack(padx=5, pady=5)

        WINDOW.mainloop()


if __name__ == "__main__":
    App()

