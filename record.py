import pyaudio
import keyboard
import numpy as np
from scipy.io import wavfile
import speech_recognition as sr


class Recorder():
    def __init__(self):
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.sample_rate = 44100
        self.chunk = int(0.03*self.sample_rate)
        self.filename = 'Space.wav'
        self.START_KEY = 's'
        self.STOP_KEY = 'q'


    def record(self):
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
                # stop and close the stream
                stream.stop_stream()
                stream.close()
                p.terminate()
                #convert recorded data to numpy array
                recorded_data = [np.frombuffer(frame, dtype=np.int16) for frame in recorded_data]
                wav = np.concatenate(recorded_data, axis=0)
                wavfile.write(self.filename, self.sample_rate, wav)
                print("You should have a wav file in the current directory")
                break


    def listen(self):
        print(f"Press `{self.START_KEY}` to start and `{self.STOP_KEY}` to quit!")
        while True:
            if keyboard.is_pressed(self.START_KEY):
                self.record()
                break

    def translate_record(self): # Функция перевода голоса в текст
        r = sr.Recognizer()
        translate = sr.AudioFile('Space.wav')
        with translate as source:
            audio = r.record(source)
        query = r.recognize_google(audio, language='ru-RU')
        file = open('translate.txt', 'w')
        file.write(query)
        file.close()

recorder = Recorder()
recorder.listen()
recorder.translate_record()
