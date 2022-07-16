from tkinter import *
from gtts import gTTS
import os
from playsound import playsound

root = Tk()
root.geometry("400x400")
root.configure(bg='LIGHT GREEN')
root.title("TEXT TO SPEECH python UI")


Label(root, text="TEXT TO VOICE", font="arial 35 bold", bg='white smoke').pack()
Msg = StringVar()
entry_field = Entry(root, textvariable=Msg, width='50',)
entry_field.place(x=30, y=100)


def Text_to_speech():
    Message = entry_field.get()
    speech = gTTS(text=Message)
    speech.save('Data.mp3')
    playsound('Data.mp3')


def Exit():
    root.destroy()
    os.remove('Data.mp3')



Button(root, text="PLAY", font='arial 15 bold', command=Text_to_speech, width='4').place(x=25, y=140)
Button(root, font='arial 15 bold', text='EXIT', width='4', command=Exit, bg='Red').place(x=100, y=140)

root.mainloop()