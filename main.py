import os
import threading
import tkinter as tk
from tkinter import ttk
import pyaudio
import wave
import time
from transcriber import transcribe_audio, summarize_text
from tkinter import messagebox


class GPAssistantApp:

    def __init__(self, root):
        self.root = root
        self.root.title("GP AI Assistant")
        self.recording = False

        self.main_frame = ttk.Frame(self.root, padding=(20, 20, 20, 20))
        self.main_frame.pack(fill='both', expand=True)

        self.voice_recorder_button = tk.Button(self.main_frame, text="🎤", font=("Arial", 60, "bold"),
                                               command=self.click_recorder)
        self.voice_recorder_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.recording_time_label = ttk.Label(self.main_frame, text="00:00:00")
        self.recording_time_label.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.audio_files_label = ttk.Label(self.main_frame, text="Audio Files:")
        self.audio_files_label.grid(row=2, column=0, sticky="w", pady=5)

        self.audio_files_listbox = tk.Listbox(self.main_frame, width=50)
        self.audio_files_listbox.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        self.refresh_button = ttk.Button(self.main_frame, text="Refresh", command=self.refresh_files)
        self.refresh_button.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        self.transcribe_button = ttk.Button(self.main_frame, text="Transcribe", command=self.transcribe)
        self.transcribe_button.grid(row=3, column=2, pady=5, padx=5, sticky="nsew")

        self.summary_button = ttk.Button(self.main_frame, text="Summarize", command=self.summarize)
        self.summary_button.grid(row=3, column=3, pady=5, padx=5, sticky="nsew")

        self.refresh_files()

    def click_recorder(self):
        if self.recording:
            self.recording = False
            self.voice_recorder_button.config(fg="black")
        else:
            self.recording = True
            self.voice_recorder_button.config(fg="red")
            threading.Thread(target=self.record).start()

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        frames = []
        start = time.time()
        while self.recording:
            data = stream.read(1024)
            frames.append(data)
            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60
            self.recording_time_label.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Create or ensure the folder "GP Client Audio" exists on the desktop
        folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "GP Client Audio")
        os.makedirs(folder_path, exist_ok=True)

        # Find an available file name
        i = 1
        while True:
            file_path = os.path.join(folder_path, f"recording{i}.wav")
            if not os.path.exists(file_path):
                break
            i += 1

        # Save the audio file
        with wave.open(file_path, "wb") as sound_file:
            sound_file.setnchannels(1)
            sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            sound_file.setframerate(44100)
            sound_file.writeframes(b"".join(frames))

    def refresh_files(self):
        folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "GP Client Audio")
        if os.path.isdir(folder_path):
            audio_files = [file for file in os.listdir(folder_path) if (file.endswith(".wav") or file.endswith(".mp4") or file.endswith(".txt"))]
            self.audio_files_listbox.delete(0, tk.END)
            for audio_file in audio_files:
                self.audio_files_listbox.insert(tk.END, audio_file)
        else:
            self.audio_files_listbox.delete(0, tk.END)
            self.audio_files_listbox.insert(tk.END, "Folder not found!")

    def transcribe(self):
        selected_item = self.audio_files_listbox.curselection()
        if selected_item:
            file_name = self.audio_files_listbox.get(selected_item[0])
            if file_name.lower().endswith((".mp3", ".mp4", ".wav")):
                transcribe_audio(file_name)
            else:
                messagebox.showerror('Incorrect File', 'Error: You have selected a file that cannot be '
                                                                'transcribed. Please make sure selected the file is an '
                                                                'audio file.')

    def summarize(self):
        selected_item = self.audio_files_listbox.curselection()
        if selected_item:
            file_name = self.audio_files_listbox.get(selected_item[0])
            if file_name.lower().endswith(".txt"):
                summarize_text(file_name)
            else:
                messagebox.showerror('Incorrect File', 'Error: You have selected a file that cannot be '
                                                       'transcribed. Please make sure selected the file is an '
                                                       'text file.')

def main():
    root = tk.Tk()
    app = GPAssistantApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
