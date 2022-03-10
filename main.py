from tkinter import *   
import pygame  # for playing music selected
from tkinter import filedialog # to search in system for song to add
import time # to get current time of the song 
from mutagen.mp3 import MP3  # to get complete length of the song
import tkinter.ttk as ttk  # for slide bar

# initialize tkinter window
root = Tk()
root.title("Music Player")
root.iconbitmap(bitmap=r'C:\Users\Sony\PycharmProjects\pythonProject\Frameworks of python\tkinter_projects\music player\icon.ico')
root.geometry("600x400")

# initialize pygame
pygame.mixer.init()


# creating function to get length of the song
def play_time():
    # sometimes slider moves faster so we terminate the funcion
    if stopped:
        return
    # getting the current time
    current_time = pygame.mixer.music.get_pos() / 1000

    # throw up temp label to get data   # to check whether the slide and son position are same 
    # slider_label.config(text=f'Slider: {int(my_slider.get())} and Song Pos: {int(current_time)}')

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
    global song_length
    # get song length with mutagen
    song_length = song_mut.info.length  # we get that in seconds
    # converting the time(in seconds) we get into time format
    converted_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))


    # increase current time by 1
    current_time+=1

    # if the song is finished we need to stop teh timer in the status bar
    if int(my_slider.get()) == int(song_length):
        # teh song timer stops 1 sec before teh song length so we replaced converted_current_time to converted_song_length to compensate for that 1 sec
        status_bar.config(text=f'Time Elapsed: {converted_song_length}  of  {converted_song_length}  ')
    
    # doing this so that teh slider get paused when the pause button is clicked
    elif Pause:
        pass
    
    # slider hasen't been moved
    elif int(my_slider.get()) == int(song_length):   
        # syncing the slider psotion and current time
        # updating slider position when song plays and also slider goes to origial position when new song is selected
        slider_position = int(song_length)	
        my_slider.config(to=slider_position, value=int(current_time))
    
    # slider has been moved
    else:       
        slider_position = int(song_length)	
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        # converting the slider position we get into time format
        converted_current_time = time.strftime('%H:%M:%S', time.gmtime(int(my_slider.get())))
        # now we have to update status bar
        # putting the current time on status bar
        status_bar.config(text=f'Time elapsed:{converted_current_time} of {converted_song_length}')

        # moving the slider along with new postion attained
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)
        

    # updating slider postion value to current song position
    # my_slider.config(value=current_time)   # commenint this out beacuse it was updting the slider to position 0 

    # calling back the function every 1 sec 
    status_bar.after(1000, play_time)

# creating slider function
def slide(x):
    # slider_label.config(text=f'{int(my_slider.get())} in {int(song_length)}')  # this was just used for testing purposes

    # loads the active song and plays it
    song = song_box.get(ACTIVE)
    # sine path and mp3 have been stripped off we have to add them back to play the song
    song = f"D:/sangeet/{song}.mp3"
    # loading and playing music
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

    # for updating slider position when song plays, we go to pla function

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
    # calling the stop function which will reset the slider and  status bar
    stop()
    # every time a song has been highlighted it's been anchored, it's an anchor song
    # deleting the currently selected song
    song_box.delete(ANCHOR)
    # stop music if it's playing the deleted Song
    pygame.mixer.music.stop()

# delete many songs from listbox
def delete_many_song():
    # calling the stop function which will reset the slider and  status bar
    stop()
    # deleting all the songs from the listbox
    song_box.delete(0, END)
    # stop music if it's playing
    pygame.mixer.music.stop()


# playing song
def play():
    # setting stopped to False so song can play and slider can move
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    # sine path and mp3 have been stripped off we have to add them back to play the song
    song = f"D:/sangeet/{song}.mp3"
    # loading and playing music
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # calling the palytime function to get song length
    play_time()

    # below is giving a problem since slider is lagging by 1 sec to teh current time of song that's why we move below statements to play_time funvtion
    # updating slider position when song plays and also slider goes to origial position when new son is selected
    # slider_position = int(song_length)	
    # my_slider.config(to=slider_position, value=0)

    # to get the current volume value
    # current_volume = pygame.mixer.music.get_volume()
    # slider_label.config(text=current_volume*100)

# stopping the music
global stopped
stopped = False
def stop():
    # updating slider and staus bar when stopped is pressed
    status_bar.config(text='')
    my_slider.config(value=0)

    # stopping the music
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    #setting a global stopped variable to True
    global stopped
    stopped = True

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
    # updating slider and staus bar when next is pressed
    status_bar.config(text='')
    my_slider.config(value=0)

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
    # updating slider and staus bar when prev is pressed
    status_bar.config(text='')
    my_slider.config(value=0)

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


# creating a volume function
def volume(x):
    pygame.mixer.music.set_volume(vol_slider.get())

    # to get the current volume value
    # current_volume = pygame.mixer.music.get_volume()
    # slider_label.config(text=current_volume*100)

# creating master frame
master_frame = Frame(root)
master_frame.pack(pady=20)

# creating playlistboc
song_box = Listbox(master_frame, bg="black", fg="green", width=60, selectbackground="gray", selectforeground="black")
song_box.grid(row=0, column=0)

# define user control buttons images
back_btn_img = PhotoImage(file=r'C:\Users\Sony\PycharmProjects\pythonProject\Frameworks of python\tkinter_projects\music player\img\back50.png')
fwrd_btn_img = PhotoImage(file=r'C:\Users\Sony\PycharmProjects\pythonProject\Frameworks of python\tkinter_projects\music player\img\forward50.png')
play_btn_img = PhotoImage(file=r'C:\Users\Sony\PycharmProjects\pythonProject\Frameworks of python\tkinter_projects\music player\img\play50.png')
pause_btn_img = PhotoImage(file=r'C:\Users\Sony\PycharmProjects\pythonProject\Frameworks of python\tkinter_projects\music player\img\pause50.png')
stop_btn_img = PhotoImage(file=r'C:\Users\Sony\PycharmProjects\pythonProject\Frameworks of python\tkinter_projects\music player\img\stop50.png')

# create user frame
control_frame =Frame(master_frame)
control_frame.grid(row=1, column=0, pady=20)  # right underneath the playlist(LISTBOX)

# Create Volume Label Frame
volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=20)

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

##### song slider below

# creating music position slider 
#                             [starting value, end value]
#                                  [     /|\      ] 
#                                  [      |       ] 
#                                  [      |       ] 
#                                  [      |       ]                [Current pos]       [increse length slider]
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=10)

# creating a volume slider
#                              [starting value, end value]
#                                  [     /|\      ] 
#                                  [      |       ] 
#                                  [      |       ] 
#                                  [      |       ]                [Current pos]       [increse length slider]
vol_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=125)
vol_slider.pack(pady=10)

# making temporary slider label
# slider_label = Label(root, text=0)
# slider_label.pack(pady=10)

root.mainloop()
