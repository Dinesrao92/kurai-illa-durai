#!/usr/bin/env python3
import subprocess, os, wave, math, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("work/seg", exist_ok=True)

FPS = 24
W, H = 1080, 1920
TITLE_DUR = 3.0
GAP = 0.6
TAIL = 1.6

# (clip_mp3, frame_png, [english subtitle cues])
beats = [
    ("clips/01_durai.mp3", "frames/01_durai_confront.png", [
        "Dey Kavin! You think I wouldn't know?",
        "Everything that happens in Brickfields reaches my ears, da.",
        "Ten years this area has been in my hands — you forgot?",
        "Tell me... who is the traitor?"]),
    ("clips/02_kavin.mp3", "frames/02_kavin_plead.png", [
        "Anne, I'm telling the truth, anne! I didn't do anything!",
        "It's Maaran who flipped everything around. Trust me, anne, please!",
        "At least think of my family — give me one chance, anne!"]),
    ("clips/03_durai.mp3", "frames/03_durai_angry.png", [
        "A chance? Dey, chances only exist in the movies, da.",
        "I fed you, gave you a job, paid for your sister's wedding.",
        "But what did you do? Where are the goods from my lorry?",
        "Who did you hand them to?"]),
    ("clips/04_maaran.mp3", "frames/04_maaran_enter.png", [
        "Oh Durai! Still talking like the old king?",
        "Times have changed, da. These KL streets are all under MY control now.",
        "Even your own men are on my side. What will you do now?"]),
    ("clips/05_durai.mp3", "frames/05_durai_standoff.png", [
        "Maaran... I knew you would come here, da.",
        "But you forgot one thing — this Durai has never fallen.",
        "Ten years... so many came, so many went. Who are you?"]),
    ("clips/06_maaran.mp3", "frames/06_maaran_laugh.png", [
        "Haha! I AM the big shot, da. You know why?",
        "The snake inside your own house...",
        "...the Kavin you raised like a brother fed me every bit of info!",
        "Correct, right, Kavin?"]),
    ("clips/07_kavin.mp3", "frames/07_kavin_twist.png", [
        "Sorry Maaran... I was never your man, da.",
        "I only joined you because Durai anna told me to.",
        "Everything you did these six months — the police have it all as proof.",
        "Look outside... hear the sirens?"]),
    ("clips/08_maaran.mp3", "frames/08_maaran_shock.png", [
        "What?! Dey Kavin! You... you played me?!",
        "Durai! Is this fair? Let me go, da!",
        "I won't let you get away with this!"]),
    ("clips/09_durai.mp3", "frames/09_durai_calm.png", [
        "Maaran... there's a proverb in Brickfields, da.",
        "Even a starving tiger will never eat grass.",
        "But you? You sold your own people.",
        "Kavin... hand him over to the police."]),
    ("clips/10_kavin.mp3", "frames/07_kavin_twist.png", [
        "Anne... next time don't give me this acting job, anne.",
        "My knees hurt from all that kneeling!",
        "But anna... our plan worked out next level, right?"]),
    ("clips/11_durai.mp3", "frames/00_title.png", [
        "Dey thambi... kings may change in KL,",
        "but one thing in Brickfields will never change.",
        "This area... will ALWAYS be Durai's area!",
        "Come, roti canai at the mamak — my treat!"]),
]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:]); sys.exit(1)

# 1) convert all clips to uniform wav and measure durations
durs = []
for i, (clip, _, _) in enumerate(beats):
    wavp = f"work/seg/a{i:02d}.wav"
    run(["ffmpeg", "-y", "-i", clip, "-ar", "44100", "-ac", "1", "-sample_fmt", "s16", wavp])
    with wave.open(wavp) as wf:
        durs.append(wf.getnframes() / wf.getframerate())

# 2) build full audio: title silence + clips with gaps + tail
def silence_frames(sec): return b"\x00\x00" * int(44100 * sec)
out = wave.open("work/full_audio.wav", "wb")
out.setnchannels(1); out.setsampwidth(2); out.setframerate(44100)
out.writeframes(silence_frames(TITLE_DUR))
for i in range(len(beats)):
    with wave.open(f"work/seg/a{i:02d}.wav") as wf:
        out.writeframes(wf.readframes(wf.getnframes()))
    out.writeframes(silence_frames(GAP if i < len(beats) - 1 else TAIL))
out.close()

# 3) subtitles (proportional split by cue length)
def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = int(t % 60); ms = int((t % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

srt, idx = [], 1
t = TITLE_DUR
for i, (_, _, cues) in enumerate(beats):
    total = sum(len(c) for c in cues)
    ct = t
    for c in cues:
        d = durs[i] * len(c) / total
        srt.append(f"{idx}\n{ts(ct)} --> {ts(ct + d - 0.05)}\n{c}\n")
        idx += 1; ct += d
    t += durs[i] + GAP
open("work/subs.srt", "w").write("\n".join(srt))

# 4) render segments with Ken Burns
seg_specs = [("frames/00_title.png", TITLE_DUR)]
for i, (_, frame, _) in enumerate(beats):
    d = durs[i] + (GAP if i < len(beats) - 1 else TAIL)
    seg_specs.append((frame, d))

concat_list = []
for i, (frame, d) in enumerate(seg_specs):
    n = max(int(round(d * FPS)), 1)
    zoom_in = (i % 2 == 0)
    z = f"1+0.12*on/{n}" if zoom_in else f"1.13-0.12*on/{n}"
    vf = (f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,"
          f"crop={W*2}:{H*2},"
          f"zoompan=z='{z}':x='iw/2-(iw/zoom)/2':y='ih/2-(ih/zoom)/2'"
          f":d={n}:s={W}x{H}:fps={FPS},format=yuv420p")
    segp = f"work/seg/v{i:02d}.mp4"
    run(["ffmpeg", "-y", "-i", frame, "-vf", vf, "-frames:v", str(n),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", segp])
    concat_list.append(f"file '{os.path.abspath(segp)}'")
    print(f"segment {i+1}/{len(seg_specs)} done ({d:.1f}s)")

open("work/vlist.txt", "w").write("\n".join(concat_list))
run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "work/vlist.txt",
     "-c", "copy", "work/video_nosub.mp4"])

# 5) mux audio + burn subtitles
style = ("FontName=DejaVu Sans,FontSize=10,Bold=1,PrimaryColour=&H00FFFFFF,"
         "OutlineColour=&H00141414,Outline=2,Shadow=1,MarginV=28")
run(["ffmpeg", "-y", "-i", "work/video_nosub.mp4", "-i", "work/full_audio.wav",
     "-vf", f"subtitles=work/subs.srt:force_style='{style}'",
     "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
     "-c:a", "aac", "-b:a", "160k", "-shortest",
     "KURAI_ILLA_DURAI_video.mp4"])

print("TOTAL DURATION:", TITLE_DUR + sum(durs) + GAP * (len(beats) - 1) + TAIL)
print("DONE")
