import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import yt_dlp
import os
import threading


def download():
    def download_thread():
        video_url = url_entry.get().strip()
        if not video_url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return

        choice = format_var.get()
        quality = quality_var.get()
        if not choice or not quality:
            messagebox.showerror("Error", "Please select a format and quality.")
            return

        save_path = filedialog.askdirectory(title="Select Download Folder")
        if not save_path:
            messagebox.showerror("Error", "Please select a download folder.")
            return

        # Clear previous status
        status_label.config(text="Preparing to download...")
        progress_var.set(0)

        try:
            def progress_hook(d):
                if d['status'] == 'downloading':
                    # Safely extract percentage and update progress bar
                    percentage = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
                    progress_var.set(percentage)
                    video_name = d['info_dict'].get('title', 'unknown') + f".{d['info_dict'].get('ext', '')}"
                    status_label.config(
                        text=f"Downloading: {video_name}\n{percentage:.2f}% completed"
                    )
                elif d['status'] == 'finished':
                    status_label.config(text="Download completed successfully!")

            ydl_opts = {
                'format': quality,
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
            }

            if choice == "MP3":
                ydl_opts['postprocessors'] = [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }
                ]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Start the download process in a new thread
    threading.Thread(target=download_thread).start()


def update_quality_options():
    choice = format_var.get()
    quality_menu["menu"].delete(0, "end")
    if choice == "MP4":
        qualities = [("Best Quality (Recommended)", "best"), ("480p", "best[height<=480]"), ("360p", "best[height<=360]")]
    elif choice == "MP3":
        qualities = [("Best Quality (Recommended)", "bestaudio"), ("Low Quality", "worstaudio")]

    for label, value in qualities:
        quality_menu["menu"].add_command(label=label, command=lambda v=value: quality_var.set(v))
    quality_var.set(qualities[0][1])


# Tkinter GUI
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("500x400")
root.resizable(False, False)
root.configure(bg="#2C3E50")

title_label = tk.Label(root, text="YouTube Downloader", font=("Arial", 20, "bold"), fg="#ECF0F1", bg="#2C3E50")
title_label.pack(pady=10)

url_label = tk.Label(root, text="Enter YouTube URL:", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50, font=("Arial", 10))
url_entry.pack(pady=5)

format_var = tk.StringVar(value="MP4")
mp4_radio = tk.Radiobutton(root, text="Download as MP4 (Video)", variable=format_var, value="MP4", font=("Arial", 10),
                           bg="#2C3E50", fg="#ECF0F1", selectcolor="#34495E", command=update_quality_options)
mp4_radio.pack(pady=5)
mp3_radio = tk.Radiobutton(root, text="Download as MP3 (Audio)", variable=format_var, value="MP3", font=("Arial", 10),
                           bg="#2C3E50", fg="#ECF0F1", selectcolor="#34495E", command=update_quality_options)
mp3_radio.pack(pady=5)

quality_var = tk.StringVar()
quality_label = tk.Label(root, text="Select Quality:", font=("Arial", 12), fg="#ECF0F1", bg="#2C3E50")
quality_label.pack(pady=5)
quality_menu = tk.OptionMenu(root, quality_var, "")
quality_menu.config(font=("Arial", 10), bg="#34495E", fg="#ECF0F1", width=20)
quality_menu.pack(pady=5)
update_quality_options()

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=400)
progress_bar.pack(pady=10)

status_label = tk.Label(root, text="", font=("Arial", 10), fg="#ECF0F1", bg="#2C3E50")
status_label.pack()

download_button = tk.Button(root, text="Download", command=download, bg="#E74C3C", fg="#ECF0F1",
                            font=("Arial", 14, "bold"), relief="flat")
download_button.pack(pady=20)

root.mainloop()