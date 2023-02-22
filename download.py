import youtube_dl
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
  ssl._create_default_https_context = ssl._create_unverified_context

def run():
    video_url = input("Por favor insira a URL do vídeo desejado: ")
    video_info = youtube_dl.YoutubeDL().extract_info(
        url=video_url,
        download=False
    )
    filename = f"{video_info['title']}.mp3"
    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print("Download concluído com sucesso... {}".format(filename))

if __name__ == '__main__':
    run()
