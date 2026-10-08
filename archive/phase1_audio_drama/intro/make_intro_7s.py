#!/usr/bin/env python3
"""7-second version of the 'Naan Durai' intro."""
import numpy as np, wave, subprocess, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SR = 44100

def save(name, x, gain=1.0):
    x = x * gain
    m = np.max(np.abs(x))
    if m > 0.98: x = x / m * 0.98
    with wave.open(name, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x*32767).astype(np.int16).tobytes())

def lowpass(x, alpha):
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc += alpha * (x[i] - acc); y[i] = acc
    return y

def fade(x, fin, fout):
    n = len(x); fi = int(fin*SR); fo = int(fout*SR)
    env = np.ones(n); env[:fi] = np.linspace(0,1,fi); env[-fo:] = np.linspace(1,0,fo)
    return x * env

subprocess.run(["ffmpeg","-y","-i","narration_naan_durai.mp3","-ar",str(SR),"-ac","1","narr.wav"], capture_output=True)
with wave.open("narr.wav") as w:
    narr = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)/32767
narr_dur = len(narr)/SR          # ~4.05s

DUR = 7.0
NARR_AT = 1.4                    # voice starts early; ends ~5.45s
N = int(DUR*SR); t = np.arange(N)/SR
rng = np.random.default_rng(7)

# RAIN (quick fade in)
noise = rng.standard_normal(N)
spec = np.fft.rfft(noise); freqs = np.fft.rfftfreq(N, 1/SR)
with np.errstate(divide='ignore'):
    shape = np.where(freqs<400, 0.25, np.where(freqs<6000, 1.0/np.sqrt(np.maximum(freqs,1)/400), 0.15))
rain = np.fft.irfft(spec*shape, N); rain /= np.max(np.abs(rain))
rain = fade(rain, 0.4, 1.0)

# MONORAIL pass 0.3-2.4s (quick, under the voice start)
mono = np.zeros(N); p0, p1 = 0.3, 2.4
seg = slice(int(p0*SR), int(p1*SR)); ts = t[seg]-p0; L = p1-p0
env = np.sin(np.pi*ts/L)**2
wn = rng.standard_normal(len(ts))
whoosh = lowpass(wn, 0.08)*env*2.2
f_dopp = 95*(1.25-0.5*ts/L)
rumble = np.sin(2*np.pi*np.cumsum(f_dopp)/SR)*env*0.8
clack = lowpass(np.abs(np.sin(2*np.pi*7.3*ts))**8*wn, 0.25)*env*1.1
mono[seg] = whoosh+rumble+clack; mono /= max(np.max(np.abs(mono)),1e-9)

# SIREN from 4.2s (after voice peak, rides the outro)
sir = np.zeros(N); s0 = 4.2
seg = slice(int(s0*SR), N); ts = t[seg]-s0
f = 850+380*np.sin(2*np.pi*0.55*ts)
tone = np.sin(2*np.pi*np.cumsum(f)/SR)+0.4*np.sin(2*np.pi*np.cumsum(2*f)/SR)
tone = lowpass(tone, 0.12)
tone *= 0.3+0.6*np.clip(ts/(DUR-s0),0,1)
e = int(0.18*SR); tone[e:] += 0.35*tone[:-e].copy()
sir[seg] = tone; sir = fade(sir, 0.3, 0.9); sir /= max(np.max(np.abs(sir)),1e-9)

# BGM (drone + 2 heartbeat thumps)
def note(fq,a): return a*(np.sin(2*np.pi*fq*t)+0.5*np.sin(2*np.pi*fq*1.003*t))
drone = note(55,0.9)+note(110,0.5)+note(164.8,0.25)
drone *= 0.55+0.45*np.sin(2*np.pi*0.14*t-np.pi/2)
beat = np.zeros(N)
for k in range(6):
    i = int(k*1.1*SR); L2 = int(0.28*SR)
    if i+L2 < N:
        td = np.arange(L2)/SR
        beat[i:i+L2] += np.sin(2*np.pi*(52-28*td/0.28)*td)*np.exp(-td*14)
bgm = drone+beat*0.9; bgm = fade(bgm, 0.6, 1.2); bgm /= np.max(np.abs(bgm))

# VOICE with echo
voice = np.zeros(N); i0 = int(NARR_AT*SR)
end = min(i0+len(narr), N); voice[i0:end] = narr[:end-i0]
e = int(0.22*SR); voice[e:] += 0.18*voice[:-e].copy()

# duck bed under voice
duck = np.ones(N)
d0, d1 = int((NARR_AT-0.3)*SR), min(int((NARR_AT+narr_dur+0.4)*SR), N)
r = int(0.3*SR)
duck[d0:d0+r] = np.linspace(1,0.35,r); duck[d0+r:d1-r] = 0.35
duck[d1-r:d1] = np.linspace(0.35,1,r)

mix = (rain*0.50+mono*0.55+sir*0.32+bgm*0.60)*duck + voice*1.0
mix = mix/np.max(np.abs(mix))*0.95
save("INTRO_MIX_7S.wav", mix)
subprocess.run(["ffmpeg","-y","-i","INTRO_MIX_7S.wav","-b:a","192k","NAAN_DURAI_INTRO_7S.mp3"], capture_output=True)
print("DONE 7.0s")
