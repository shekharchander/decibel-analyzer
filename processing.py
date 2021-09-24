import numpy as np
import math
from requests import get
class Audio:
    def __init__(self,f):
        #self.f=f.split('/')[-1]
        self.f='am_voice.mp3'
        open(self.f,'wb').write(get(f).content)
        fname = self.convert_to_wav(self.f.split('.',-1)[0])
        data = self.extract_from_wav(fname)
        frequencies = self.get_frequencies(data)
        decibels=self.get_decibel_values(frequencies)
        percentile=np.percentile(decibels,[25,75])
        self.Q1,self.Q3=percentile
        self.mean=np.mean(decibels)
        self.median=np.median(decibels)
        self.standvn=np.std(decibels)
        self.variance=np.var(decibels)

    def get_slient_parts(self):
        from audio_profile import AudioSegment,silence
        fname=self.f
        audio=AudioSegment.from_mp3(fname)
        silent_parts=silence.detect_silence(audio,min_silence_len=1000,silence_thresh=-54)
        sec1,sec2,sec3,sec4,sec5,sec6,sec10=[0 for _ in range(7)]
        for i in silent_parts:
            if i[-1]-i[0]>=1000:
                sec1+=1
            if i[-1]-i[0]>=2000:
                sec2+=1
            if i[-1]-i[0]>=3000:
                sec3+=1
            if i[-1]-i[0]>=4000:
                sec4+=1
            if i[-1]-i[0]>=5000:
                sec5+=1
            if i[-1]-i[0]>=6000:
                sec6+=1
            if i[-1]-i[0]>=10000:
                sec10+=1
        return (sec1, sec2, sec3, sec4, sec5, sec6, sec10)

    def convert_to_wav(self,fname):
        import subprocess 
        subprocess.call(
            ['ffmpeg',
             '-i',
             fname+'.mp3',
             fname+'.wav',
             '-loglevel',
             'panic',
             '-y'
            ])
        del subprocess
        wav_name=fname+'.wav'
        return wav_name

    def extract_from_wav(self,fs):
        import wave
        wav = wave.open(fs)
        framerate = wav.getframerate()
        frames = wav.readframes(-1)
        self.width = wav.getsampwidth()
        wav.close()
        del wave
        return_data = (framerate,frames)
        return return_data

    def get_frequencies(self,data):
        fr,frms = data
        frequencies = np.frombuffer(frms, 'int16')
        frequencies=frequencies/fr
        return frequencies

    def get_decibel_values(self,freq):
        def to_decibel(arr):
            if arr!=0:
                return 20 * math.log10(abs(arr))    
            else:
                return -60
        return [to_decibel(i) for i in freq]

