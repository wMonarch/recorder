import speech_recognition as sr
from tkinter import *
import pyaudio
import keyboard
import numpy as np
from scipy.io import wavfile
import threading


class Recorder(): # Класс для записи аудио
    def __init__(self):
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.sample_rate = 44100
        self.chunk = int(0.03*self.sample_rate)
        self.filename = 'Space.wav'
        self.START_KEY = 'Space'
        self.STOP_KEY = 'alt'

    def Gui(self): # интерфейс
        root = Tk()
        root.title('AudioTranslator')
        root.geometry('450x300')
        root.resizable(width=False, height=False)
        canvas = Canvas(root, height=450, width=300)
        canvas.pack()
        frame = Frame(root, bg='white')
        frame.place(relheight=1, relwidth=1)
        title = Label(frame, text='AudioTranslator', bg='gray', font='40')
        title.pack()
        bt1 = Label(frame, text='Нажмите клавишу "Space" для записи аудио', bg='white', font='45')
        bt2 = Label(frame, text='Нажмите клавишу "Alt" для прекращения записи', bg='white', font='45')
        bt3 = Button(frame, text='...', width=30, height=3)
        bt4 = Button(frame, text='...', width=30, height=3)
        bt1.pack()
        bt2.pack()
        bt3.pack()
        bt4.pack()
        root.mainloop()


    def record(self): # функция
        recorded_data = []
        p = pyaudio.PyAudio()

        stream = p.open(format=self.audio_format, channels=self.channels,
                        rate=self.sample_rate, input=True,
                        frames_per_buffer=self.chunk)
        while(True):
            data = stream.read(self.chunk)
            recorded_data.append(data)
            if keyboard.is_pressed(self.STOP_KEY):
                print("Stop recording")
                # начать и закончить стрим
                stream.stop_stream()
                stream.close()
                p.terminate()
                #convert recorded data to numpy array
                recorded_data = [np.frombuffer(frame, dtype=np.int16) for frame in recorded_data]
                wav = np.concatenate(recorded_data, axis=0)
                wavfile.write(self.filename, self.sample_rate, wav)
                print("You should have a wav file in the current directory")
                break


    def listen(self): # функция записи
        print(f"Press `{self.START_KEY}` to start and `{self.STOP_KEY}` to quit!")
        while True:
            if keyboard.is_pressed(self.START_KEY):
                self.record()
                break


def translate_record(): # Функция перевода голоса в текст
    r = sr.Recognizer()
    translate = sr.AudioFile('Space.wav')
    with translate as source:
        audio = r.record(source)
    query = r.recognize_google(audio, language='ru-RU')
    file = open('translate.txt', 'w')
    file.write(query)
    file.close()


recorder = Recorder()


