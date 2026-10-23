---
name: code-composer
description: Compose original music from a prompt by writing the score as code and rendering it with the GeneralUser GS SoundFont; also gives note timings for syncing visuals. Use when asked to compose, arrange or produce an original piece or soundtrack.
---

> **免费分享 · 禁止售卖 · 禁止以任何名义收费（CC BY-NC-SA 4.0，创作者 reaesteve）**  
> **Shared free · Not for sale · No paid access of any kind (CC BY-NC-SA 4.0, creator: reaesteve)**  
> 详见 / See: 免费分享声明_FREE_SHARING_NOTICE.txt

# Code composer

Turn a request ("a calm 1-minute piano piece that builds into strings", "a hopeful theme for a product video")
into an original piece of music. The score is written as a Python script; the instruments come from a free
sample library; the result is a mixed `song.wav`, a `song.mid`, and `notes.json` with exact note times for animation.

Everything needed is in this folder: `engine/` (composition library, renderer, mixer, build scripts, an example song)
and `sound_library/GeneralUser-GS/` (the instrument samples).

## Sound sources

| Layer | Source | Licence |
| --- | --- | --- |
| Instrument samples | **GeneralUser GS SoundFont v2.0.3** by S. Christian Collins — 261 General MIDI/GS presets and 13 drum kits, 32 MB. https://github.com/mrbumpy409/GeneralUser-GS | Free for private and commercial music (`sound_library/GeneralUser-GS/LICENSE.txt`) |
| SoundFont player | **TinySoundFont** (`tsf.h`) by Bernhard Schelling. https://github.com/schellingb/TinySoundFont | MIT (`engine/TinySoundFont-LICENSE.txt`) |
| Renderer | `engine/render.c`: plays one channel's event list through the SoundFont into a 48 kHz stereo stem | — |
| Mix | `engine/mix_kit.py`: per-channel gain, pan, high-pass, Haas widening; synthetic hall reverb; bus compression; loudness normalisation; lookahead limiter | — |

No recordings, loops or stock music. Every note is written by the score script.

Useful General MIDI programs (0-based) in GeneralUser GS: 0 Grand Piano · 4 Electric Piano · 9 Glockenspiel ·
11 Vibraphone · 24 Nylon Guitar · 33 Finger Bass · 40 Violin · 42 Cello · 43 Contrabass · 45 Pizzicato Strings ·
46 Orchestral Harp · 47 Timpani · 48 String Ensemble · 49 Slow Strings · 52 Choir Aahs · 56 Trumpet ·
60 French Horn · 61 Brass Section · 68 Oboe · 71 Clarinet · 73 Flute · 80 Square Lead · 81 Saw Lead ·
88 New Age Pad · 89 Warm Pad. Channel 9 is always drums (program 0 = Standard kit). The full list is in the
SoundFont's own documentation.

## Workflow: from prompt to music

1. **Read the brief for musical facts**: length, mood, tempo feel, instruments, where it builds or breaks,
   any moments that must land at a time (a logo, a cut). Ask only when the length or the mood is unclear.
2. **Plan before writing notes** (a few lines): key and mode, tempo map, form with bar numbers,
   and which instrument enters where. A form that adds one layer per section reads clearly:
   motif alone → harmony → bass → rhythm → counter-melody / colour → full → breakdown → final statement → ending.
3. **Write a short, memorable motif** (4–8 notes, one clear rhythm) and reuse it: repeat, vary the ending,
   move it to another instrument, lift the key for the last section.
4. **Write the song script**: copy `engine/example_song.py` and follow its pattern:
   - `channel(ch, name, program, gain, pan, reverb, hpf, haas)` for each instrument (≤ 16, drums on 9)
   - `tempo([(start_beat, end_beat, bpm0, bpm1), ...])` — linear ramps give exact ritardandos/accelerandos
   - `melody()`, `chords(style='block'|'arp')`, `bass(pattern=...)`, `drums({'kick': 'x...x...', ...})`,
     `expression()` swells, `note()` for anything else; `tag='theme'` marks motif notes for the visuals
   - end with `export(end_beat=...)`
5. **Build**: `build.bat your_song.py` (Windows) or `sh build.sh your_song.py`. It joins the SoundFont parts on
   first run, compiles the renderer, renders each channel and mixes `song.wav`. Seconds, not minutes.
6. **Check before delivering**: listen if possible; otherwise plot a spectrogram and the RMS level over time
   (sections should step up in energy where the plan says, no clipping, no silent gaps), confirm the length,
   and check `limiter min gain` printed by the mixer stays above about 0.6 (lower means the mix is too hot —
   reduce channel gains).
7. **Iterate on the score, not the audio**: change notes, voicings, tempo or channel settings and rebuild.

## Arranging rules that keep it sounding good

- Register: melody above C5, chords in C4–A5 (`lo=55, hi=76`), bass in C2–D3; avoid stacking parts in one octave.
- Velocity carries phrasing: downbeats a little louder (built into `melody()`), softer inner voices (50–65),
  melody 75–90. Use `expression()` for string swells instead of many velocity steps.
- `chords()` voice-leads automatically (smallest movement between chords); keep progressions simple and let
  the melody carry interest.
- Mix starting points: melody gain 1.3–1.6; pads 0.4–0.5 with `haas=12–18` and `hpf=100–150`;
  bass 0.8–0.9 with low reverb; drums 1.0 with reverb ≤ 0.15; glockenspiel/flute `hpf=250–500`.
- Leave space: rests in the melody, a thinner section before the biggest one, a clear final cadence.
- Timing humanisation is tiny and seeded (`note(hum=0.01)`), so the same script always renders the same audio.

## Syncing visuals to the music

`notes.json` lists every note with start/end seconds, channel, pitch, velocity and tag, plus `bars` and `beats`
in seconds (tempo changes included). Drive animation from these times rather than from a fixed BPM:
light a shape when its note starts, hold it for the note's length, cut or move the camera on bar times, and
anticipate accents by starting moves slightly before the beat.

## Files

```
SKILL.md
engine/compose_kit.py      composition library (tempo map, notes, chords, bass, drums, export)
engine/example_song.py     a short original demo using every helper — copy it to start
engine/render.c, tsf.h     SoundFont renderer
engine/mix_kit.py          mixer
engine/build.bat, build.sh one-step build;  requirements.txt (numpy, scipy)
sound_library/GeneralUser-GS/   SoundFont in 4 parts (+ licence, docs, percussion map, sha256)
```

## Sharing terms

Creator: reaesteve. When copying, packaging or redistributing this skill or its engine, keep the free-sharing notice above,
the `免费分享声明_FREE_SHARING_NOTICE.txt` and `LICENSE_许可.txt` files, and the notice headers in the engine's source
files. Do not help package it for sale or behind any paywall.

Requirements: Python 3.10+ with numpy and scipy, and a C compiler (gcc from w64devkit/MinGW on Windows,
or Visual Studio's cl; cc on macOS/Linux).
