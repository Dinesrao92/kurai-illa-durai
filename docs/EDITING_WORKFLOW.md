# 🎬 KURAI ILLA, DURAI — 60s TRAILER
## CAPCUT EDITING WORKFLOW · DIRECTOR'S CUT SHEET
*Editor: DR · Format: 9:16 vertical · Target: 60.0s exact*

---

# 🗺️ WORKFLOW OVERVIEW

```
PHASE 0          PHASE 1          PHASE 2          PHASE 3
GATHER    ──▶    SETUP     ──▶    PICTURE   ──▶    AUDIO
assets           project          lock             layers
                                    │                │
PHASE 6          PHASE 5          PHASE 4           │
EXPORT    ◀──    SUBS +    ◀──    GRADE +    ◀──────┘
& QC             TITLES           POLISH
```

Rule of the house: **LOCK PICTURE FIRST. Audio second. Grade third. Subs last.**
Never grade or sub a timeline that's still moving.

---

# 📦 PHASE 0 — GATHER ASSETS

## 0.1 Video (from Drive `footage/` — download all to phone)
| File | Status |
|---|---|
| shot01_cold_open.mp4 | ✅ pre-cut 4s, approved |
| shot02 THE HANDS.mp4 | ✅ watermark already removed |
| shot03 DURAI REVEAL.mp4 | ✅ |
| shot04 KAVIN.mp4 | ✅ |
| Shot 05 TEN YEARS.mp4 | ✅ needs salvage trim (see 2.2) |
| Shot 6.MP4 | ✅ needs beat surgery (see 2.2) |
| SHOT 10 — LORRY ATTACK.MP4 | ✅ use FULL 5s |
| SHOT 11 — THE STILL MAN.MP4 | ✅ |
| SHOT 12 — DURAI MOVES.MP4 | ✅ |
| SHOT 13 — KAVIN'S SECRET.MP4 | ✅ |
| SHOT 14 — MAARAN RAGES.MP4 | ✅ |
| Shot 08 / 09 / 15 / 16A / 16B | 🟠 generating — slot in as they land |

## 0.2 Audio
| Asset | Source | Use |
|---|---|---|
| Durai VO (10.03s narration) | repo `durai_voice/` | Spine of Act 1 + title smash |
| Maaran lines | repo `maaran_final/` | VO over Shot 14 |
| Kavin lines | repo `final_cast/` | Shot 04 (already fitted 6.00s) |
| Rain / city / truck / beeps / birds / whoosh | repo `sfx/` (6 files) | Hits & beds |
| Trailer music (dark hybrid/percussion) | CapCut Audio library — pick 60s+ track | Full bed |

## 0.3 Stills & titles
- Title card (umbrella photo, "DIRECTED BY DR") — repo `posters/`
- Cold-open flash stills — repo `refs/` + `scenes_v4/`
- Motion titles (black bg clips) — repo `motion_titles/` → CapCut Blend mode **Screen**

---

# ⚙️ PHASE 1 — PROJECT SETUP

1. New project → ratio **9:16** → resolution **1080×1920**
2. Frame rate: **30fps** (footage is 24fps — CapCut conforms automatically, do NOT "speed match")
3. Create track layout before dropping anything:
   - **V1** = main picture
   - **V2** = flash stills / motion titles / overlays
   - **A1** = VO & dialogue
   - **A2** = music bed
   - **A3** = SFX hits
   - **A4** = ambience beds (rain/city)
4. Turn ON "Snap" in timeline settings — every cut lands on the grid.

---

# 🎞️ PHASE 2 — PICTURE LOCK (the master cut sheet)

## 2.1 Assembly order
Lay shots left to right in slot order. Trim per table. Don't touch audio yet.

| # | Slot | Shot | Source trim | Speed | Cut note |
|---|---|---|---|---|---|
| 01 | 0:00–0:04 | COLD OPEN | as delivered (4.0s) | 100% | Black + still flashes — LOCKED, don't retouch |
| 02 | 0:04–0:07 | THE HANDS | 0.0 → 3.0s | 100% | Macro push-in |
| 03 | 0:07–0:10 | DURAI REVEAL | 2.06 → 5.06s | 100% | Eyes come up last |
| 04 | 0:10–0:14 | KAVIN | 0.2 → 4.2s | 100% | Dialogue clip, audio comes in Phase 3 |
| 05 | 0:14–0:18 | TEN YEARS | trim to the hand-take moment | **70%** slow | SALVAGE: keep only the clean hand-take, slow it to fill 4s |
| 06 | 0:18–0:22 | JOHOR ARRIVES | beats 1 + 3 only | 100% | SURGERY: cut out the maroon middle beat entirely; butt-join 1→3 |
| 07 | 0:22–0:26 | THE PACKAGE | still `s3_D_packet_smile.png` | — | EDIT shot: 4s still + slow zoom-in (keyframe scale 100→108%) + rack-focus feel via slight blur keyframe |
| 08 | 0:26–0:30 | THE LINE | best 4s of stare | 100% | Hands thread garland, eyes never move |
| 09 | 0:30–0:34 | RAHIM | slide → taps → nod | 100% | Cut ON the nod |
| 10 | 0:34–0:39 | LORRY ATTACK | FULL 0.0 → 5.0s | 100% | Optional: 0.8–2.0s garland fall at 60% if you want more pain |
| 11 | 0:39–0:43 | STILL MAN | 2.2 → 5.0s | 100% | THE HEART — eyes rise |
| 12 | 0:43–0:47 | DURAI MOVES | 0.0 → 3.4s | 100% | End ON the buckle. (Alt: run to 4.4s arm-lock) |
| 13 | 0:47–0:51 | KAVIN'S SECRET | 0.3 → 5.06s | 100% | KEEP the 4.9s bulb-dim — it's your free cut-to-black |
| 14 | 0:51–0:54 | MAARAN RAGES | best 3s of rise | 100% | End on the cold upright stare |
| 15 | 0:54–0:56 | BIGGER SHADOW | cleanest 2s around the tap | 100% | Tap = the trigger |
| 16 | 0:56–0:58 | FINAL COLLISION | 0.4s micro-cuts (recipe below) | 100% | See 2.3 |
| 17 | 0:58–1:00 | TITLE SMASH | title card | — | See 2.4 |

## 2.2 Salvage notes (shots 05 + 06)
- **Shot 05:** scrub to the exact frame the hand takes the garland. In-point ≈ 1s before contact, out-point ≈ after contact. Apply 70% speed → clip stretches to fill the 4s slot. Smooth slow-mo ON (optical flow) if your CapCut has it.
- **Shot 06:** split the clip at the maroon-suit middle section. Delete the middle. The jump from beat 1 (wheel/shoe) to beat 3 (crane up) reads as an intentional jump-cut — that's the style, no transition needed.

## 2.3 Shot 16 — the 2-second collision recipe
Cut 5 micro-slices, each **0.4s**, alternating sources:

```
[16A ropes/sleeve 0.4] [16B Maaran looks up 0.4] [16A smile dies 0.4]
[16B head tilt down 0.4] [16A step forward 0.4] → HARD CUT TO BLACK
```

No transitions. No fades. Raw butt-cuts — the speed IS the violence.

## 2.4 Shot 17 — title smash
1. 2 frames of pure black after the last 16A slice
2. Title card SMASHES in (scale keyframe 130%→100% over 3 frames)
3. Hold title to exactly 1:00.0
4. Final Durai VO line rides over black + title (Phase 3)

## 2.5 Picture-lock QC gate ✋
- [ ] Timeline = exactly 60.0s
- [ ] Every cut on a beat (play it 3× — any cut that "trips" = move it)
- [ ] No accidental transitions (CapCut loves auto-inserting them — check every joint)
- [ ] Watch ONCE muted. If the story reads silent, picture is locked.

---

# 🔊 PHASE 3 — AUDIO BUILD

## 3.1 Layer order (build in this order, not all at once)
1. **A1 — VO & dialogue** (the spine)
2. **A2 — music** (the engine)
3. **A4 — ambience beds** (the world)
4. **A3 — SFX hits** (the punches — LAST, they sit on top)

## 3.2 VO / dialogue placement
| Line | Slot | Timing note |
|---|---|---|
| Durai narration (VO part 1) | 0:00–0:14 | Same placement as approved ACT1 preview — VO starts ≈0:04.4 over THE HANDS |
| Kavin intro line | 0:10–0:14 | Fitted 6.00s audio — trim tail to slot |
| "Naan Maaran illa. Idhu Brickfields." | Shot 08 | "Idhu Brickfields" lands in the FINAL second → hard cut |
| "Monthly." | Shot 09 | Lands exactly on the finger taps |
| "Anna... idhu Durai anna oda load." / "Theriyum." | Shot 10 | "Theriyum" lands as camera reaches the dead jasmine |
| "Manushan-a illa..." | Shot 11 | Lands as the eyes rise (2.2s into clip) |
| Maaran: "Durai-a touch panna sollala naan... Brickfields-a touch panna sonnen" | Shot 14 | Pure VO — clip has no lip movement BY DESIGN |
| Final Durai line: "Kurai illa... Durai." | Shot 17 | Over black + title. THE button. |

**Levels:** dialogue/VO = reference level (0dB clip gain), everything else ducks under it.

## 3.3 Music bed (A2)
- One continuous dark percussion/hybrid track, 0:00 → 1:00
- Volume: **~30%** under VO, can breathe up to 50% in gaps
- Map the track's natural drop to **0:34 (LORRY ATTACK)** — slide the music left/right until its biggest hit lands there
- Second escalation 0:47 → 0:58, then MUSIC OUT dead at the cut to black (0:58). Title plays in silence + VO. Silence = power.

## 3.4 Ambience beds (A4) — volume ~25%
| Bed | Where |
|---|---|
| Rain | Shots 10, 12 (both are rain scenes) |
| City night | Shots 13, 15 |
| Market day murmur | Shots 02, 05, 08, 09 |

Crossfade beds 0.5s at scene changes. Beds NEVER audible over VO — they're felt, not heard.

## 3.5 SFX hits (A3)
| Hit | Timecode | Note |
|---|---|---|
| Whoosh → every cold-open flash | 0:00–0:04 | Whoosh peak hits 0.55s after file start → start file 0.55s BEFORE the cut |
| Bass hit | 0:14 (ten years match-cut) | |
| Truck rumble | 0:18 (Johor arrives) | |
| Bass + whip | 0:43 + ~1.8s = **0:44.8** (the wrist CATCH in Shot 12) | The money hit |
| Sub-bass swell | 0:54 (shadow tap) + soft UI tick on the tap frame | |
| 5× impact hits | 0:56–0:58 — ONE on every 0.4s collision cut | Machine-gun |
| Title smash impact + silence | 0:58 | Biggest hit of the trailer, then nothing |

## 3.6 Audio QC gate ✋
- [ ] Full watch with eyes CLOSED — story must work as radio
- [ ] No VO word masked by a hit
- [ ] Phone-speaker test (most viewers = phone speakers)
- [ ] Levels: nothing clipping, dialogue always king

---

# 🎨 PHASE 4 — GRADE & POLISH

1. **One look, applied globally:** teal-orange cinematic (match the ACT1 preview grade — that's the approved reference)
2. Per-shot balance pass: day shots (02/05/08/09) slightly warm · night shots (10/12/13/15) teal shadows, sodium highlights
3. **Consistency check:** scrub the whole timeline at 2× — skin tones must not jump between cuts
4. Optional: film grain at 5–10% opacity over EVERYTHING (unifies AI footage beautifully)
5. Vignette subtle (≤15%) on night shots only
6. NO glow/bloom/beauty filters — kills the realism

---

# 💬 PHASE 5 — SUBTITLES & TITLES

## 5.1 Subtitle rules (NON-NEGOTIABLE)
- Dialogue shown in **Thanglish** exactly as written, English translation beneath OR English-only subs — pick ONE style, keep it 60s consistent
- **"anna" / "thambi" NEVER translated as father/son.** Keep as anna/thambi or "big brother"
- Font: clean bold sans, white + thin black outline, bottom-third, SAFE from CapCut/TikTok UI zones
- Max 2 lines, on screen minimum 1s, out BEFORE the cut (never ride across a cut)

## 5.2 Title elements
- Motion titles (black-bg clips) → V2 track → Blend mode **Screen**
- End title card: hold 0:58–1:00, nothing else on screen
- NO watermarks anywhere in frame — check all 4 corners at full brightness

---

# 📤 PHASE 6 — EXPORT & FINAL QC

## 6.1 Export settings
| Setting | Value |
|---|---|
| Resolution | 1080×1920 |
| Frame rate | 30fps |
| Bitrate | Highest / "Recommended+" |
| Codec | H.264 |
| HDR | OFF |

## 6.2 FINAL QC — watch the export file, not the timeline
- [ ] Duration exactly 1:00
- [ ] Watch on phone, full brightness, volume 50%
- [ ] Watch once MUTED (picture test)
- [ ] Watch once EYES CLOSED (audio test)
- [ ] Corner check: no watermarks, no UI, no readable signage/plates
- [ ] Subtitle pass: every line, zero typos, anna-thambi correct
- [ ] The 3 kill-shots hit: 0:34 lorry drop · 0:44.8 wrist catch · 0:58 title smash
- [ ] Send to one person who knows nothing about the project — if they ask "when's the full film?", SHIP IT 🚀

---

*Repo = source of truth · Drive = delivery mirror · Director DR edits, agent QCs*
🥀 **KURAI ILLA, DURAI** — Chapter 1 · Malaysian Indian Tamil Drama
