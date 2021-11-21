from tkinter import *
import pygame  # for playing music selected
from tkinter import filedialog # to search in system for song to add
import time # to get current time of the song 
from mutagen.mp3 import MP3  # to get complete length of the song


# initialize tkinter window
root = Tk()
root.title("Music Player")
root.iconbitmap(bitmap=r'C:\Users\Sony\PycharmProjects\pythonProject\Frameworks of python\tkinter_projects\music player\icon.ico')
root.geometry("500x450")

# initialize pygame
pygame.mixer.init()


# creating function to get length of the song
def play_time():
    # getting the current time
    current_time = pygame.mixer.music.get_pos() / 1000

    # converting the time(in seconds) we get into time format
    converted_current_time = time.strftime('%H:%M:%S', time.gmtime(current_time))

    # get currrently playing song
    # current_song = song_box.curselection()  # returns a number
    # grabbing title from playlist
    song = song_box.get(ACTIVE) # grabs the active song and it's index
    # add directory and mp3 to title
    song = f"D:/sangeet/{song}.mp3"
    
    # loading the song
    song_mut = MP3(song)
    # get song length with mutagen
    song_length = song_mut.info.length  # we get that in seconds
    # converting the time(in seconds) we get into time format
    converted_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))


    # putting the current time on status bar
    status_bar.config(text=f'Time elapsed:{converted_current_time} of {converted_song_length}')

    # calling back the function every 1 sec 
    status_bar.after(1000, play_time)

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
	
# delete a song from listbox
def delete_song():
    stop()
    # every time a song has been highlighted it's been anchored, it's an anchor song
    # deleting the currently selected song
    song_box.delete(ANCHOR)
    # stop music if it's playing the deleted Song
    pygame.mixer.music.stop()

# delete many songs from listbox
def delete_many_song():
    stop()
    # deleting all the songs from the listbox
    song_box.delete(0, END)
    # stop music if it's playing
    pygame.mixer.music.stop()


# playing song
def play():
    song = song_box.get(ACTIVE)
    # sine path and mp3 have been stripped off we have to add them back to play the song
    song = f"D:/sangeet/{song}.mp3"
    # loading and playing music
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # calling the palytime function to get song length
    play_time()

# stopping the music
def stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    # clearing the status bar
    status_bar.config(text='')

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

# playing next song
def next_song():
    # getting the index of teh current song
    next_one = song_box.curselection() # this returns a tuple of indexes
    # print(next_one)
    # next_one[0] gives you the item at 0th index at tuple which is teh 0th position of the song
    # adding 1 to current song index to go fo next index
    next_one = next_one[0] + 1
    # grabbing the next song from playlist with new next_one
    song = song_box.get(next_one)  # eturns song name without directory and .mp3 extension
    # sine path and mp3 have been stripped off we have to add them back to play the song
    song = f"D:/sangeet/{song}.mp3"
    # loading and playing music
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # changing the active bar 
            # clearing the current active bar  and alson any bar fron the list box
    song_box.selection_clear(0, END)

            # activating the new active bar
    song_box.activate(next_one)

            # seting the active bar to next song
    song_box.selection_set(next_one, last=None)

# prev song || almost similar to the next_song function
def prev_song():
    prev_one = song_box.curselection()
    prev_one = prev_one[0] - 1
    song = song_box.get(prev_one)
    song = f"D:/sangeet/{song}.mp3"
    # loading and playing music
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # changing the active bar 
            # clearing the current active bar  and alson any bar fron the list box
    song_box.selection_clear(0, END)

            # activating the new active bar
    song_box.activate(prev_one)

            # seting the active bar to next song
    song_box.selection_set(prev_one, last=None)



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
fwrd_btn = Button(control_frame, image=fwrd_btn_img , borderwidth=0, command=next_song)
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
# add many songs in the listbox
add_song_menu.add_command(label="Add many song to playlist", command=add_many_song)

# delete song from listbox
delete_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove song", menu=delete_song_menu)
delete_song_menu.add_command(label="Delete one song to playlist", command=delete_song)
# delete many songs in the listbox
delete_song_menu.add_command(label="Delete many song to playlist", command=delete_many_song)

# create status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)


root.mainloop()