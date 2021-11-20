from tkinter import *
import pygame  # for playing music selected
from tkinter import filedialog # to search in system for song to add



# initialize tkinter window
root = Tk()
root.title("Music Player")
root.iconbitmap(bitmap=r'C:\Users\Sony\PycharmProjects\pythonProject\Frameworks of python\tkinter_projects\music player\icon.ico')
root.geometry("500x400")

# initialize pygame
pygame.mixer.init()

#add single song function
def add_song():
    song = filedialog.askopenfilename(initialdir='D:\sangeet', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
	
    #strip out directory info and .mp3 extension
    song = song.replace("D:/sangeet/", "")
    song = song.replace(".mp3", "")

    # adding song to listbox
    song_box.insert(END, song)

# adding many songs
def add_many_song():
    songs = filedialog.askopenfilenames(initialdir='D:\sangeet', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))

    # looping through directory and removing the direcoty an d .mp3 section from name
    for song in songs:
         #strip out directory info and .mp3 extension
        song = song.replace("D:/sangeet/", "")
        song = song.replace(".mp3", "")

        # adding song to listbox
        song_box.insert(END, song)
	
# playing song
def play():
    song = song_box.get(ACTIVE)
    # sine path and mp3 have been stripped off we have to add them back to play the song
    song = f"D:/sangeet/{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

# stopping the music
def stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

# creating global pause
global Pause
Pause = False

# pausing the current music
def pause(is_paused):
    global Pause
    Pause = is_paused

    if Pause: # here the value of Pause is True which is passed
        # unpausing
        pygame.mixer.music.unpause()
        Pause = False
    else:  # here the value of Pause if false which is passed
        # pausing
        pygame.mixer.music.pause()
        Pause = True    

# next song
def newxt_song():
    pass

# prev song
def prev_song():
    pass

# creating playlistboc
song_box = Listbox(root, bg="black", fg="green", width=60, selectbackground="gray", selectforeground="black")
song_box.pack(pady=20)

# define user control buttons images
back_btn_img = PhotoImage(file=r'C:\Users\Sony\PycharmProjects\pythonProject\Frameworks of python\tkinter_projects\music player\img\back50.png')
fwrd_btn_img = PhotoImage(file=r'C:\Users\Sony\PycharmProjects\pythonProject\Frameworks of python\tkinter_projects\music player\img\forward50.png')
play_btn_img = PhotoImage(file=r'C:\Users\Sony\PycharmProjects\pythonProject\Frameworks of python\tkinter_projects\music player\img\play50.png')
pause_btn_img = PhotoImage(file=r'C:\Users\Sony\PycharmProjects\pythonProject\Frameworks of python\tkinter_projects\music player\img\pause50.png')
stop_btn_img = PhotoImage(file=r'C:\Users\Sony\PycharmProjects\pythonProject\Frameworks of python\tkinter_projects\music player\img\stop50.png')

# create user frame
control_frame =Frame(root)
control_frame.pack()

# creating player control buttons
back_btn = Button(control_frame, image=back_btn_img , borderwidth=0, command=prev_song)
fwrd_btn = Button(control_frame, image=fwrd_btn_img , borderwidth=0, command=newxt_song)
play_btn = Button(control_frame, image=play_btn_img , borderwidth=0, command=play)
# passing the global Pause in pause function to check if current song in paused or not 
pause_btn = Button(control_frame, image=pause_btn_img , borderwidth=0, command=lambda: pause(Pause))
stop_btn = Button(control_frame, image=stop_btn_img , borderwidth=0, command=stop)

back_btn.grid(row=0, column=0, padx=10)
fwrd_btn.grid(row=0, column=1, padx=10)
play_btn.grid(row=0, column=2, padx=10)
pause_btn.grid(row=0, column=3, padx=10)
stop_btn.grid(row=0, column=4, padx=10)


# creaating menu
my_menu = Menu(root)
root.config(menu=my_menu)
# add song part in menu
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add song", menu=add_song_menu)
add_song_menu.add_command(label="Add one song to playlist", command=add_song)
#add many songs in the listbox
add_song_menu.add_command(label="Add many song to playlist", command=add_many_song)

root.mainloop()