// 【免费分享声明】
// 创作者：reaesteve
// 本项目（技能说明、作曲引擎代码、示例曲与项目文档）由创作者 reaesteve 免费分享，仅供个人学习与非商业使用。
// 禁止以任何名义出售、转售或打包售卖本项目，禁止通过付费下载、付费会员、付费课程、付费社群、
// “打赏/关注后获取”、引流收费等任何形式收取费用或设置付费门槛。
// 可以免费转发与修改，但必须注明出处、保留本声明，并以相同许可免费分享。
// 用本技能创作的音乐归创作者本人所有；以上限制针对的是本项目本身。
// 许可：知识共享 署名-非商业性使用-相同方式共享 4.0 国际（CC BY-NC-SA 4.0）
// https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans
// 第三方组件（GeneralUser GS 音色库、TinySoundFont）沿用其各自的原始许可。
// 如果你是付费获得本项目的，请注意：它本来就是免费的。
//
// [Free-sharing notice]
// This project (skill guide, composition engine code, example song and project documents) is shared by its creator, reaesteve, free of
// charge for personal, non-commercial use. Selling, reselling or bundling it for sale is prohibited, as is
// charging for access in any form or under any pretext: paid downloads, memberships, courses, paid groups,
// "tip/follow to unlock", or lead-generation paywalls. You may share and adapt it for free, with credit,
// keeping this notice, under the same licence. Music you create with it belongs to you; these limits apply
// to the project itself.
// Licence: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0)
// https://creativecommons.org/licenses/by-nc-sa/4.0/
// Third-party components (GeneralUser GS SoundFont, TinySoundFont) keep their own original licences.
// If you paid for this project, you were charged for something that is free.

// Minimal offline SoundFont renderer: reads a sorted event list, writes float32 stereo raw.
// events: <time_sec> <type> <ch> <a> <b>
//   P ch bank preset   (program; ch 9 => drums)
//   N ch key vel(0-127)
//   O ch key 0
//   C ch ctrl value
#define TSF_IMPLEMENTATION
#include "tsf.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { double t; char type; int ch, a, b; } Ev;

int main(int argc, char** argv) {
    if (argc < 5) { fprintf(stderr, "usage: render sf2 events out.raw total_sec\n"); return 1; }
    const int SR = 48000;
    tsf* f = tsf_load_filename(argv[1]);
    if (!f) { fprintf(stderr, "sf2 load failed\n"); return 1; }
    tsf_set_output(f, TSF_STEREO_INTERLEAVED, SR, 0.0f);
    tsf_set_max_voices(f, 256);
    for (int c = 0; c < 16; c++) tsf_channel_set_bank_preset(f, c, 0, 0);
    tsf_channel_set_presetnumber(f, 9, 0, 1);

    FILE* in = fopen(argv[2], "r");
    int cap = 1 << 16, n = 0; Ev* ev = malloc(sizeof(Ev) * cap);
    char ty;
    while (1) {
        Ev e; if (fscanf(in, "%lf %c %d %d %d", &e.t, &ty, &e.ch, &e.a, &e.b) != 5) break;
        e.type = ty; if (n == cap) { cap *= 2; ev = realloc(ev, sizeof(Ev) * cap); }
        ev[n++] = e;
    }
    fclose(in);
    double total = atof(argv[4]);
    long frames = (long)(total * SR);
    FILE* out = fopen(argv[3], "wb");
    const int BLK = 64; float buf[BLK * 2];
    int ei = 0;
    for (long pos = 0; pos < frames; pos += BLK) {
        double t = (double)pos / SR;
        while (ei < n && ev[ei].t <= t) {
            Ev* e = &ev[ei++];
            switch (e->type) {
                case 'P': if (e->ch == 9) tsf_channel_set_presetnumber(f, 9, e->b, 1); else tsf_channel_set_bank_preset(f, e->ch, e->a, e->b); break;
                case 'N': tsf_channel_note_on(f, e->ch, e->a, e->b / 127.0f); break;
                case 'O': tsf_channel_note_off(f, e->ch, e->a); break;
                case 'C': tsf_channel_midi_control(f, e->ch, e->a, e->b); break;
            }
        }
        tsf_render_float(f, buf, BLK, 0);
        fwrite(buf, sizeof(float), BLK * 2, out);
    }
    fclose(out);
    return 0;
}
