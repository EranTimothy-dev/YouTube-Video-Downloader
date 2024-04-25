from tkinter import * 
from tkinter import ttk
from tkinter import messagebox
from pytube import *
from PIL import ImageTk, Image
import urllib.request
import io
import os
from pathlib import Path



root = Tk()
root.title("YouTube Downloader")
root.iconbitmap("images/icon.ico")
root.geometry("690x200")
root.resizable(0,0)

# Set style for the label widget
s = ttk.Style()
s.configure("Label.TLabel", 
            background = "#FAF9F6", 
            font = ('Helvetica', '12', 'bold'), 
            padding = (15, 6, 15, 6)
            )

# Get the resolution available to download in the videp
def get_resolutions(Stream):
    args = str(Stream)
    start_index = args.find("=",41) + 2
    end_index = args.find('p',41) + 1
    resolution = args[start_index:end_index]
    return resolution

# get the size and download bytes of the video
def on_progress(stream, chunk, bytes_remaining):
    """Callback function"""
    global percentage
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    percentage = round(pct_completed, 2)
    print(f"Status: {round(pct_completed, 2)} %")
    
    # Update the progress bar as the video downloads
    download_progress['value'] = int(percentage)
    root.update_idletasks()
    

 

def search(url):
    '''Wrap whole segment inside try except block to catch connection error and display a messagebox'''
    global photo
    global percentage
    global download_progress
    global download_section
    # global image
    url = str(url)
    # Search for the youtube video and get required details
    yt = YouTube(url, on_progress_callback=on_progress)
    Title = yt.title
    Thumbnail = yt.thumbnail_url
    quality = yt.streams.filter(progressive=True)
    Thumbnail = str(Thumbnail)
    
    # Display details in a toplevel window
    download_section = Toplevel()
    download_section.title("Download Video")
    download_section.iconbitmap("images/icon.ico")
    download_section.geometry("690x500")
    download_section.resizable(0,0)
    
    frame1 = Label(download_section)
    frame1.pack(side=TOP)
    
    # Open thumbnail url and load image
    try:
      with urllib.request.urlopen(Thumbnail) as u:
         raw_data = u.read()
    except Exception as e:
        response = messagebox.showerror("Issue loading image", "Thumbnail could not be loaded")
        print(f"Error fetching image: {e}")
        return

    try:
        image = Image.open(io.BytesIO(raw_data))
        resized_image= image.resize((300,205))
        photo = ImageTk.PhotoImage(resized_image)
    except Exception as e:
        print(f"Error opening image: {e}")
        return
    
    video_thumbnail = ttk.Label(frame1, image=photo)
    video_thumbnail.pack(padx=5, pady=5)
    
    video_title = ttk.Label(frame1, text=Title, style='Label.TLabel')
    video_title.pack(padx=10, pady=10)
    
    # Get the resolution quality available to download
    video_quality = ["   "]
    for i in quality:
        Resolution = get_resolutions(i)
        video_quality.append(Resolution)
    
    
    
    frame2 = Frame(download_section)
    frame2.pack(fill='both',expand=1,side=BOTTOM)
    
    clicked = StringVar()
    
    frame2.rowconfigure(0, weight=1)
    frame2.rowconfigure(1, weight=1)
    
    resolution_label = ttk.Label(frame2, text="Please select resolution quality:")
    resolution_label.place(x=25, y=20)
    
    # Drop down menu to select resolution
    dropdown = ttk.OptionMenu(frame2, clicked, *video_quality)
    dropdown.place(x= 70, y=50)
    
    # Get path to the downloads folder
    path_to_download = str(os.path.join(Path.home(), 'Downloads'))
    
    # Create download button
    download_button = ttk.Button(frame2, text="Download", command=lambda: download_video(clicked,quality, path_to_download))
    download_button.place(x=60, y=100)

    # Progress bar to see the download
    download_progress = ttk.Progressbar(frame2, orient=HORIZONTAL, length=350, mode="determinate")
    download_progress.place(x=300, y=90)


# Function to download the vide 
def download_video(resolution,stream, path):
    # Option to allow users to select download quality from a selected resolution
    downloading = stream.get_by_resolution(resolution)
    if downloading == None:
        # Display an error message if something unusual happens and destroy top level window
        response = messagebox.showerror("Resolution Unavailable","Something went wrong please try again!")
        print("resolution unavailable")
        download_section.destroy()
    else:
        downloading.download(path) 
  


 
note = '''NOTE: If the download doesn't start please check if it already is downloaded in the Downloads folder'''

# Create frame for url search
url_frame = ttk.Frame(root, width=500, height=500)
url_frame.pack(fill="both", expand=1)

# Frame to place entry box and search button
entry_frame = ttk.Labelframe(url_frame, text="Enter url", padding=5)
entry_frame.grid(row=1, column=1, columnspan=2, padx=20, pady=20)

# Provide not for user to to understand an issue with the download feature
note_label = ttk.Label(url_frame, text=note)
note_label.grid(row=2, column=1)


# Entry box to enter youtube url
take_URL = ttk.Entry(entry_frame, width=100)
take_URL.pack()

# Search for the video url that is given
search_button = ttk.Button(entry_frame, text="Search", command=lambda: search(take_URL.get()))
search_button.pack(pady=10, padx=10) #grid(row=2, column=1)

root.mainloop()