#!/usr/bin/env python3
"""Build the 'Naan Durai' intro: narration + rain + monorail + distant siren + dark BGM."""
import numpy as np, wave, subprocess, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SR = 44100

def save(name, x, gain=1.0):
    x = x * gain
    m = np.max(np.abs(x))
    if m > 0.98: x = x / m * 0.98
    data = (x * 32767).astype(np.int16)
    with wave.open(name, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(data.tobytes())

def lowpass(x, alpha):
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc += alpha * (x[i] - acc); y[i] = acc
    return y

def fade(x, fin=0.5, fout=1.0):
    n = len(x); fi = int(fin*SR); fo = int(fout*SR)
    env = np.ones(n)
    env[:fi] = np.linspace(0, 1, fi)
    env[-fo:] = np.linspace(1, 0, fo)
    return x * env

# ---- get narration ----
subprocess.run(["ffmpeg","-y","-i","narration_naan_durai.mp3","-ar",str(SR),"-ac","1","narr.wav"],
               capture_output=True)
with wave.open("narr.wav") as w:
    narr = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)/32767
narr_dur = len(narr)/SR
print("narration:", round(narr_dur,2), "s")

NARR_AT = 4.0                      # narration starts at 4s
DUR = max(14.0, NARR_AT + narr_dur + 4.0)
N = int(DUR*SR)
t = np.arange(N)/SR
rng = np.random.default_rng(7)

# ---- RAIN: filtered noise, steady ----
noise = rng.standard_normal(N)
spec = np.fft.rfft(noise); freqs = np.fft.rfftfreq(N, 1/SR)
shape = np.where(freqs<400, 0.25, np.where(freqs<6000, 1.0/np.sqrt(freqs/400), 0.15))
rain = np.fft.irfft(spec*shape, N)
rain /= np.max(np.abs(rain))
rain *= 1 + 0.12*np.sin(2*np.pi*0.23*t) + 0.07*np.sin(2*np.pi*0.61*t+1.3)   # gentle swells
rain = fade(rain, 1.2, 2.0)
save("sfx_rain.wav", rain, 0.9)

# ---- MONORAIL: rumble + whoosh pass at 1.0-4.5s ----
mono = np.zeros(N)
p0, p1 = 1.0, 4.5
seg = slice(int(p0*SR), int(p1*SR))
ts = t[seg] - p0; L = p1 - p0
env = np.sin(np.pi*ts/L)**2                      # rise and fall
wn = rng.standard_normal(len(ts))
whoosh = lowpass(wn, 0.08) * env * 2.2           # air rush
f_dopp = 95*(1.25 - 0.5*ts/L)                    # pitch falls as it passes
rumble = np.sin(2*np.pi*np.cumsum(f_dopp)/SR)*env*0.8
clack = lowpass(np.abs(np.sin(2*np.pi*7.3*ts))**8 * wn, 0.25) * env * 1.1  # track joints
mono[seg] = whoosh + rumble + clack
mono /= max(np.max(np.abs(mono)), 1e-9)
save("sfx_monorail.wav", mono, 0.9)

# ---- SIREN: distant police wail, 6.5s to end, approaching slightly ----
sir = np.zeros(N)
s0 = 6.5
seg = slice(int(s0*SR), N)
ts = t[seg] - s0
f = 850 + 380*np.sin(2*np.pi*0.42*ts)            # wail sweep
tone = np.sin(2*np.pi*np.cumsum(f)/SR)
tone += 0.4*np.sin(2*np.pi*np.cumsum(2*f)/SR)    # harmonic
tone = lowpass(tone, 0.12)                       # distant = muffled
grow = np.clip(ts/(DUR-s0), 0, 1)
tone *= (0.25 + 0.55*grow)                       # approaching
echo = int(0.21*SR)                              # city echo
tone[echo:] += 0.35*tone[:-echo].copy()
sir[seg] = tone
sir = fade(sir, 0.8, 1.5)
sir /= max(np.max(np.abs(sir)), 1e-9)
save("sfx_siren.wav", sir, 0.9)

# ---- BGM: dark drone + tension pulse ----
def note(freq, amp=1.0):
    return amp*(np.sin(2*np.pi*freq*t) + 0.5*np.sin(2*np.pi*freq*1.003*t))
drone = note(55, 0.9) + note(110, 0.5) + note(164.8, 0.25)         # A1 power chord
drone *= 0.55 + 0.45*np.sin(2*np.pi*0.1*t - np.pi/2)               # slow swell
minor = (np.sin(2*np.pi*220*t) + np.sin(2*np.pi*261.63*t) + np.sin(2*np.pi*329.63*t))
minor *= 0.12*(0.5+0.5*np.sin(2*np.pi*0.07*t+2.2))                 # faint Am pad
beat = np.zeros(N); period = 1.1
for k in range(int(DUR/period)):
    i = int(k*period*SR); L2 = int(0.28*SR)
    if i+L2 < N:
        td = np.arange(L2)/SR
        beat[i:i+L2] += np.sin(2*np.pi*(52-28*td/0.28)*td)*np.exp(-td*14)   # deep thump
bgm = drone + minor + beat*0.9
bgm = fade(bgm, 2.0, 2.5)
bgm /= np.max(np.abs(bgm))
save("bgm_dark_pulse.wav", bgm, 0.9)

# ---- narration track with placement + slight echo for cinema feel ----
voice = np.zeros(N)
i0 = int(NARR_AT*SR)
voice[i0:i0+len(narr)] = narr
echo = int(0.25*SR)
voice[echo:] += 0.18*voice[:-echo].copy()
save("narration_track.wav", voice, 1.0)

# ---- duck background under the voice ----
duck = np.ones(N)
d0, d1 = int((NARR_AT-0.4)*SR), int((NARR_AT+narr_dur+0.6)*SR)
r = int(0.4*SR)
duck[d0:d0+r] = np.linspace(1, 0.35, r)
duck[d0+r:d1-r] = 0.35
duck[d1-r:d1] = np.linspace(0.35, 1, r)

mix = (rain*0.50 + mono*0.55 + sir*0.30 + bgm*0.60) * duck + voice*1.0
m = np.max(np.abs(mix)); mix = mix/m*0.95
save("INTRO_MIX.wav", mix)

subprocess.run(["ffmpeg","-y","-i","INTRO_MIX.wav","-b:a","192k","NAAN_DURAI_INTRO.mp3"], capture_output=True)
for f in ["sfx_rain.wav","sfx_monorail.wav","sfx_siren.wav","bgm_dark_pulse.wav","narration_track.wav"]:
    subprocess.run(["ffmpeg","-y","-i",f,"-b:a","192k",f.replace(".wav",".mp3")], capture_output=True)
print("duration:", DUR, "s  DONE")
