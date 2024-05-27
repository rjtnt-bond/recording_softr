
import os
import wave
import time
import threading
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
import pyaudio

# Global variables
recording = False
folder = None
# student_name = None
def get_student_name_and_select_folder():
    global student_name
    student_name = simpledialog.askstring("Input", "Please enter the student's name:")
    if not student_name:
        messagebox.showwarning("Input Error", "Student name is required.")
        return
    str(student_name)
    select_folder(student_name)

        
        
def select_folder(name):
    global folder
    directory="audio"
    student_name=str(name)
    folder = os.path.join(directory,student_name)
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    if folder:
        print(f"Folder selected: {folder}")
    else:
        print("No folder selected")

def click_handler():
    global recording

    if not folder:
        messagebox.showwarning("Input Error", "Please select a folder to save recordings.")
        return
    
    if recording:
        recording = False
        button.config(fg="black")
    else:
        recording = True
        button.config(fg="red")
        threading.Thread(target=record, args=(student_name,)).start()

def record(student_name):
    global recording
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    
    frames = []
    start = time.time()
    
    while recording:
        data = stream.read(1024)
        frames.append(data)
        
        passed = time.time() - start
        secs = int(passed % 60)
        mins = int((passed // 60) % 60)
        hours = int((passed // 3600) % 24)
        label.config(text=f"{hours:02d}:{mins:02d}:{secs:02d}")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    exists = True
    i = 1
    while exists:
        if os.path.exists(f"{folder}/{student_name}{i}.wav"):
            i += 1
        else:
            exists = False
            
    file_path = f"{folder}/{student_name}{i}.wav"
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"File saved at: {file_path}")

# Initialize Tkinter
root = tk.Tk()
root.resizable(False, False)

root.title("Voice Recorder")

# # Button to select folder
folder_button = tk.Button(root, text="Create Folder", command=get_student_name_and_select_folder)
folder_button.pack()

# # Button to start/stop recording
button = tk.Button(root, text="Start Recording", font=("Arial", 20, "bold"), command=click_handler)
button.pack(pady=20)

# Label to show the recording duration
label = tk.Label(root, text="00:00:00")
label.pack()

# Start the Tkinter event loop
root.mainloop()








