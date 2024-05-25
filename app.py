from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    link = request.form['youtube_link']
    yt = YouTube(link)
    
    audio_stream = yt.streams.filter(only_audio=True).first()
    video_stream = yt.streams.get_highest_resolution()


    choice = request.form['download_choice']
    if choice == "mp4":
        try:
            filename = f"{yt.title}.mp4"
            video_stream.download(filename=filename)
            return send_file(filename, as_attachment=True)
        except Exception as e:
            return f"An error occurred while downloading the video: {e}"
    elif choice == "mp3":
        try:
            filename = f"{yt.title}.mp3"
            audio_stream.download(filename=filename)
            return send_file(filename, as_attachment=True)
        except Exception as e:
            return f"An error occurred while downloading the audio: {e}"
    else:
        return "Invalid choice. Please enter 'mp4' or 'mp3'."

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
