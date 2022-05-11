import time
from tkinter import *
import pyaudio
from array import array
import threading
from tkinter.filedialog import asksaveasfilename, askopenfile
from tkinter import filedialog
import wave
import speech_recognition as sr


font = "courier"
fontsize = 15

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
record_on = False
frames = []

p = pyaudio.PyAudio()
stream = None

counter = 0


def start_counter(label):
    counter = 0

    def count():
        global counter
        if not record_on:
            return
        counter += 1
        label.config(text="Recording: " + str(counter) + " sec")
        label.after(1000, count)

    count()


def start_rec():
    global record_on, frames, counter_label, counter
    counter = 0
    start_counter(counter_label)

    while record_on:
        data = stream.read(CHUNK)
        data_chunk = array('h', data)
        vol = max(data_chunk)
        if (vol >= 500):
            print("something said")
            frames.append(data)
        else:
            print("nothing")
        print("\n")


def record():
    # WAVE_OUTPUT_FILENAME = "output.wav"
    global record_on, p, stream, counter_label
    if record_on:
        return

    frames.clear()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    frames_per_buffer=CHUNK,
                    input=True
                    )

    print("* recording.........")

    record_on = True
    if len(frames) > 0:
        frames.clear()

    t = threading.Thread(target=start_rec)
    t.start()

    print("* done recording")


def save_audio():
    global p, CHANNELS, FORMAT, RATE, frames, record_on, counter_label, record_type
    if len(frames) < 1:
        return
    global filename
    filename = asksaveasfilename(title="Save as",
                                 filetypes=(("audio file", "*.wav"), ("all files", "*.*")),
                                 defaultextension=".wav")

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    frames.clear()
    counter_label.config(text="Recording: 0 sec")
    record_on = False


def stop_record():
    global record_on, counter, stream, counter_label, p
    if not record_on:
        print("Recording has not initiated...")
        return
    record_on = False
    # counter_label.destroy()
    stream.stop_stream()
    stream.close()
    # p.terminate()
    stream = None
    print("Recording stopped.....")

def translate_record(): # Функция перевода голоса в текст
    r = sr.Recognizer()
    translate = sr.AudioFile(filename)
    with translate as source:
        audio = r.record(source)
    query = r.recognize_google(audio, language='ru-RU')
    flname = asksaveasfilename(title="Save as",
                                 filetypes=(("Text files", "*.txt"), ("all files", "*.*")),
                                 defaultextension=".txt")
    file = open(flname, 'w')
    file.write(query)
    file.close()


def empty_entry(text):
    text.delete(0, END)


root = Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry(f'{width}x{height}')
root.minsize(int(width / 2), int(height / 2))
root.title("Data Translator")

frame1 = Frame(root, bg='green')
frame1.place(relx=0.25, rely=(0.25,), relwidth=0.50, relheight=0.50)

start = Button(frame1, text="Record", relief=FLAT, command=record, padx=10, pady=5, fg="white", bg="blue",
               font=(font, fontsize, 'bold'))
start.place(relx=0, rely=0.3, relwidth=0.48, relheight=0.2)

stop = Button(frame1, text="Stop", relief=FLAT, command=stop_record, padx=10, pady=5, fg="white", bg="blue",
              font=(font, fontsize, 'bold'))
stop.place(relx=0.52, rely=0.3, relwidth=0.48, relheight=0.2)

saveBtn = Button(frame1, text="Save", relief=FLAT, command=save_audio, padx=10, pady=5, fg="white", bg="blue",
                 font=(font, fontsize, 'bold'))
saveBtn.place(relx=0, rely=0.6, relwidth=0.48, relheight=0.2)

translateaud = Button(frame1, text="Translate", relief=FLAT, command=translate_record ,padx=10, pady=5, fg="white", bg="blue",
              font=(font, fontsize, 'bold'))
translateaud.place(relx=0.52, rely=0.6, relwidth=0.48, relheight=0.2)



counter_label = Label(frame1, font=(font, fontsize, 'bold'))
counter_label.place(relx=0.3, rely=0.1)



root.mainloop()
