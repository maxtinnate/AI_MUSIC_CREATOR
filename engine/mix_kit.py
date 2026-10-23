# 【免费分享声明】
# 创作者：reaesteve
# 本项目（技能说明、作曲引擎代码、示例曲与项目文档）由创作者 reaesteve 免费分享，仅供个人学习与非商业使用。
# 禁止以任何名义出售、转售或打包售卖本项目，禁止通过付费下载、付费会员、付费课程、付费社群、
# “打赏/关注后获取”、引流收费等任何形式收取费用或设置付费门槛。
# 可以免费转发与修改，但必须注明出处、保留本声明，并以相同许可免费分享。
# 用本技能创作的音乐归创作者本人所有；以上限制针对的是本项目本身。
# 许可：知识共享 署名-非商业性使用-相同方式共享 4.0 国际（CC BY-NC-SA 4.0）
# https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans
# 第三方组件（GeneralUser GS 音色库、TinySoundFont）沿用其各自的原始许可。
# 如果你是付费获得本项目的，请注意：它本来就是免费的。
#
# [Free-sharing notice]
# This project (skill guide, composition engine code, example song and project documents) is shared by its creator, reaesteve, free of
# charge for personal, non-commercial use. Selling, reselling or bundling it for sale is prohibited, as is
# charging for access in any form or under any pretext: paid downloads, memberships, courses, paid groups,
# "tip/follow to unlock", or lead-generation paywalls. You may share and adapt it for free, with credit,
# keeping this notice, under the same licence. Music you create with it belongs to you; these limits apply
# to the project itself.
# Licence: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0)
# https://creativecommons.org/licenses/by-nc-sa/4.0/
# Third-party components (GeneralUser GS SoundFont, TinySoundFont) keep their own original licences.
# If you paid for this project, you were charged for something that is free.

"""
mix_kit — mixes the rendered stems into song.wav.

Reads mix.json (written by compose_kit.export) and stems/chNN.raw (written by render),
then: per-channel gain, pan, high-pass and Haas widening; a synthetic hall reverb;
gentle bus compression; loudness normalisation; a lookahead peak limiter; a tail fade.
Usage: python mix_kit.py [out.wav]
"""
import json, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve, lfilter
from scipy.ndimage import minimum_filter1d

SR = 48000
REVERB_TIME = (2.9, 2.4, 1.3)   # RT60 seconds for low / mid / high bands
REVERB_MIX = 0.55
LOUDNESS = 0.20                 # RMS target of the loudest 30% of the music
CEILING = 0.93                  # peak ceiling (about -0.6 dBFS)

cfg = json.load(open('mix.json'))
N = int(cfg['total'] * SR)
rng = np.random.default_rng(3)


def hp(x, f):
    return sosfilt(butter(2, f, 'highpass', fs=SR, output='sos'), x, axis=0)


dry = np.zeros((N, 2))
send = np.zeros((N, 2))
for ch, c in cfg['channels'].items():
    x = np.fromfile(f'stems/ch{int(ch):02d}.raw', dtype=np.float32).reshape(-1, 2)[:N].astype(np.float64)
    x = np.pad(x, ((0, N - len(x)), (0, 0)))
    if c['hpf']:
        x = hp(x, c['hpf'])
    if c['haas']:
        d, m = int(c['haas'] * SR / 1000), x.mean(1)
        x = np.stack([m, np.concatenate([np.zeros(d), m[:-d]])], 1)
    x[:, 0] *= min(1, 1 - c['pan'])
    x[:, 1] *= min(1, 1 + c['pan'])
    x *= c['gain']
    dry += x
    send += x * c['reverb']

# hall reverb: band-split decaying noise + early reflections
L = int(3.2 * SR)
t = np.arange(L) / SR
ir = np.zeros((L, 2))
for (lo, hi), rt in zip([(None, 400), (400, 3000), (3000, None)], REVERB_TIME):
    n = rng.standard_normal((L, 2))
    sos = butter(2, [lo, hi], 'bandpass', fs=SR, output='sos') if lo and hi else \
        butter(2, hi, 'lowpass', fs=SR, output='sos') if hi else butter(2, lo, 'highpass', fs=SR, output='sos')
    ir += sosfilt(sos, n, axis=0) * np.exp(-6.91 * t / rt)[:, None]
pre = int(0.022 * SR)
ir = np.concatenate([np.zeros((pre, 2)), ir])[:L]
ir[:int(0.08 * SR)] *= np.linspace(0, 1, int(0.08 * SR))[:, None] ** 2
for d_ms, a in [(11, .5), (17, .4), (23, .35), (31, .3), (43, .22), (57, .18)]:
    k = int(d_ms * SR / 1000)
    ir[k, 0] += a * 6
    ir[k + int(rng.integers(3, 40)), 1] += a * 6
ir /= np.sqrt((ir ** 2).sum(0)).mean()
wet = hp(np.stack([fftconvolve(send[:, i], ir[:, i])[:N] for i in range(2)], 1), 120)
mix = dry + wet * REVERB_MIX

# bus compression (RMS, 2:1 above threshold)
a = np.exp(-1 / (0.25 * SR))
env = np.sqrt(lfilter([1 - a], [1, -a], (mix ** 2).mean(1)) + 1e-12)
mix *= np.where(env > 0.12, (0.12 / env) ** 0.5, 1.0)[:, None]
mix += sosfilt(butter(1, 9000, 'highpass', fs=SR, output='sos'), mix, axis=0) * 0.25   # a little air

# loudness, then a 4 ms lookahead limiter
act = mix[int(min(2.0, cfg['total'] / 4) * SR):]
loud = np.sqrt(np.mean(np.sort((act ** 2).mean(1))[-int(len(act) * 0.3):]))
mix *= LOUDNESS / max(loud, 1e-9)
need = np.minimum(1.0, CEILING / np.maximum(np.abs(mix).max(1), 1e-9))
la = int(0.004 * SR)
g = minimum_filter1d(need, size=2 * la + 1)
rel = np.exp(-1 / (0.08 * SR))
g = np.minimum(lfilter([1 - rel], [1, -rel], g - 1) + 1, minimum_filter1d(need, size=2 * la + 1))
mix = np.clip(mix * g[:, None], -0.99, 0.99)
fl = int(min(3.0, cfg['total'] / 4) * SR)
mix[-fl:] *= np.linspace(1, 0, fl)[:, None] ** 2

out = sys.argv[1] if len(sys.argv) > 1 else 'song.wav'
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print(f'{out}: {N / SR:.1f} s, peak {np.abs(mix).max():.2f}, limiter min gain {g.min():.2f}')
