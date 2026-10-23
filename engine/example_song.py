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
Example: a short original piece (about 45 s) showing every helper in compose_kit.
Copy this file, rename it, and write your own music in it.
Run:  build.bat example_song.py     (Windows)   or   sh build.sh example_song.py
"""
from compose_kit import *

# instruments: channel, name, GM program (0-based), mix settings
channel(0, 'piano', 0, gain=1.4, pan=-0.05, reverb=0.30)
channel(1, 'strings', 49, gain=0.45, reverb=0.45, hpf=110, haas=14)
channel(2, 'cello', 42, gain=0.9, pan=-0.15, reverb=0.20)
channel(3, 'flute', 73, gain=0.8, pan=0.25, reverb=0.40, hpf=250)
channel(9, 'drums', 0, gain=1.0, reverb=0.12)

# 92 BPM, a ritardando into the last bar
tempo([(0, 56, 92, 92), (56, 64, 92, 70)], intro=0.5, tail=4.0, seed=7)

prog = [('Am', 4), ('F', 4), ('C', 4), ('G', 4)]

# bars 1-4: piano melody over arpeggios
melody(0, bar(1), [('E5', 1), ('A5', 1), ('G5', 0.5), ('E5', 1.5), ('D5', 1), ('C5', 1), ('D5', 2),
                   ('E5', 1), ('G5', 1), ('C6', 1.5), ('B5', 0.5), ('A5', 2), ('G5', 2)], vel=78, tag='theme')
chords(0, bar(1), prog, vel=50, lo=52, hi=72, n=3, style='arp')

# bars 5-8: cello bass and strings join, flute answers
bass(2, bar(5), prog, vel=70)
chords(1, bar(5), prog, vel=62)
expression(1, bar(5), bar(9), 40, 110)
melody(3, bar(5) + 2, [('C6', 1), ('B5', 1), ('A5', 2), (None, 2), ('E6', 1), ('D6', 1), ('C6', 2), (None, 2),
                       ('G5', 1), ('A5', 1), ('B5', 2)], vel=72)
melody(0, bar(5), [('E5', 1), ('A5', 1), ('G5', 0.5), ('E5', 1.5), ('D5', 4), ('E5', 1), ('G5', 1), ('C6', 2),
                   ('B5', 4)], vel=80, tag='theme')

# bars 9-14: full band with drums
groove = {'kick': 'x.......x.x.....', 'snare': '....x.......x...', 'hat': 'x.x.x.x.x.x.x.x.'}
drums(bar(9), 6, groove, vel=84)
note(9, DRUM['crash'], bar(9), 1, 100)
prog2 = prog + [('Am', 4), ('F', 4)]
bass(2, bar(9), prog2, vel=78, pattern=[(0, 1.5), (1.5, 0.5), (2, 2)])
chords(1, bar(9), prog2, vel=70)
chords(0, bar(9), prog2, vel=54, lo=52, hi=72, n=3, style='arp')
melody(0, bar(9), [('A5', 1), ('C6', 1), ('B5', 0.5), ('A5', 1.5), ('G5', 1), ('E5', 1), ('G5', 2),
                   ('A5', 1), ('C6', 1), ('E6', 1.5), ('D6', 0.5), ('C6', 2), ('B5', 2),
                   ('A5', 1), ('C6', 1), ('B5', 0.5), ('A5', 1.5), ('G5', 1), ('E5', 3)], vel=88, tag='theme')
melody(3, bar(9), [('E6', 4), ('F6', 4), ('E6', 4), ('D6', 4), ('C6', 4), ('C6', 4)], vel=60)

# bars 15-16: ending on A minor with a ritardando
chords(1, bar(15), [('Am', 8)], vel=60)
bass(2, bar(15), [('Am', 8)], vel=66)
melody(0, bar(15), [('E5', 2), ('C5', 2), ('A4', 4)], vel=70, tag='theme')
note(9, DRUM['crash'], bar(15), 1, 80)

export(end_beat=bar(17))
