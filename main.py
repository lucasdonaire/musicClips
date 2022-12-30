import moviepy.video.fx.all as vfx
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips
import librosa
import numpy as np



def toVideo1s(video, tam): 
    videoclip = VideoFileClip(video)
    videoclip = videoclip.fx(vfx.speedx, videoclip.duration)
    size = videoclip.size
    arr = [size[i]/tam[i] for i in range(2)]
    idx = arr.index(max(arr))
    videoclip = videoclip.resize( tuple( np.array( size ) / ( max(arr) ) ) )
    return videoclip



def ajustaVideo(video_loc, audio_loc, out_loc, bpm='auto', reps=2):
    video = VideoFileClip(video_loc) # carrega o video
    video1s = video.fx(vfx.speedx, video.duration) # ajusta ele para 1s
    if(bpm == 'auto'):
        y, sr = librosa.load(audio_loc) # carrega o audio em uma lib
        bpm, beat_frames = librosa.beat.beat_track(y, sr) # acha o bpm
    bps = bpm / 60 # acha o bps
    print(f'bps = {bps}')
    videoajustado = video1s.fx(vfx.speedx, bps/reps) # ajusta o video para repetir 'reps' vezes em cada batida
    audioclip = AudioFileClip(audio_loc) # carrega o audio na outra lib
    final = concatenate_videoclips([videoajustado for i in range(int(audioclip.duration // videoajustado.duration + 1))]) # concatena o video para repetir
    
    # se quiser ajustar o tamanho ou o inicio do video, é aqui
    # final = final.set_start(0.17)
    # final = final.resize((600,600)) 

    final.audio = audioclip # junta video e audio
    final.write_videofile(out_loc) # salva


# more than 1 video
# tam = tamanho do video final : tuple, ex (1200,700)
def ajustaVideos(videos, audio_loc, out_loc, bpm='auto', reps=2, tam = 'first'):
    
    if tam == 'first':
        tam = VideoFileClip(videos[0]).size

    videosNew = []
    for video in videos:
        videosNew.append(toVideo1s(video, tam))
    print(videosNew)
    videosconc = concatenate_videoclips(videosNew, "compose", bg_color=None, padding=0)

    if(bpm == 'auto'):
        y, sr = librosa.load(audio_loc) # carrega o audio em uma lib
        bpm, beat_frames = librosa.beat.beat_track(y, sr) # acha o bpm
    bps = bpm / 60 # acha o bps
    print(f'bps = {bps}')

    videoajustado = videosconc.fx(vfx.speedx, bps/(reps)) # ajusta o video para repetir 'reps' vezes em cada batida
    audioclip = AudioFileClip(audio_loc) # carrega o audio na outra lib
    # audioclip = concatenate_audioclips()
    final = concatenate_videoclips([videoajustado for i in range(int(audioclip.duration // videoajustado.duration + 1))]) # concatena o video para repetir
    final.audio = audioclip # junta video e audio
    final.write_videofile(out_loc) # salva


video = 'catpunk.mp4' 
audio_loc = 'jumpOutTheHouse.wav'
out_loc = 'gatoOuvindoCarti.mp4'

ajustaVideo(video, audio_loc, out_loc, bpm=144, reps=2 )