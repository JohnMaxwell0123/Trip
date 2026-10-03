#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
西行壮歌 · 丝路与额济纳自驾大环线
电影级程序化交响配乐与环境音效生成器 (Soundtrack & Foley Synthesizer)

技术指标：
- 采样率: 48,000 Hz
- 声道数: 双声道立体声 (Stereo)
- 位深: 16-bit Signed Integer PCM
- 时长: 120.0 秒 (5,760,000 采样点)
- 对应帧率: 30 FPS / 3600 帧电影时间轴精准对齐
- 纯程序化数学合成 (无需外部音频采样包，基于 numpy 与 wave 库)
"""

import sys
import math
import wave
import struct
import numpy as np

# 适配 Windows 控制台编码
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SAMPLE_RATE = 48000
DURATION_SEC = 120.0
TOTAL_SAMPLES = int(SAMPLE_RATE * DURATION_SEC)
TIME = np.linspace(0.0, DURATION_SEC, TOTAL_SAMPLES, endpoint=False)

# 16 镜头时间节点 (秒)
SHOT_CUES = [
    {"id": 1,  "name": "兰州启程",     "t0": 0.0,   "t1": 7.0},
    {"id": 2,  "name": "临泽丹霞",     "t0": 7.0,   "t1": 14.0},
    {"id": 3,  "name": "河西戈壁",     "t0": 14.0,  "t1": 22.0},
    {"id": 4,  "name": "额济纳胡杨",   "t0": 22.0,  "t1": 31.0},
    {"id": 5,  "name": "怪树林黑城",   "t0": 31.0,  "t1": 39.0},
    {"id": 6,  "name": "嘉峪关雄关",   "t0": 39.0,  "t1": 47.0},
    {"id": 7,  "name": "瓜州大地之子", "t0": 47.0,  "t1": 54.0},
    {"id": 8,  "name": "敦煌莫高窟",   "t0": 54.0,  "t1": 63.0},
    {"id": 9,  "name": "鸣沙山月牙泉", "t0": 63.0,  "t1": 71.0},
    {"id": 10, "name": "当金山口3648", "t0": 71.0,  "t1": 79.0},
    {"id": 11, "name": "大柴旦翡翠湖", "t0": 79.0,  "t1": 87.0},
    {"id": 12, "name": "茶卡天空之镜", "t0": 87.0,  "t1": 95.0},
    {"id": 13, "name": "青海湖圣湖",   "t0": 95.0,  "t1": 104.0},
    {"id": 14, "name": "塔尔寺宗喀巴", "t0": 104.0, "t1": 110.0},
    {"id": 15, "name": "西宁大环线凯旋","t0": 110.0, "t1": 116.0},
    {"id": 16, "name": "终章余韵",     "t0": 116.0, "t1": 120.0},
]


def smooth_gate(t, t_start, t_end, fade_in=1.0, fade_out=1.0):
    """平滑梯形门控包络"""
    gate = np.zeros_like(t)
    active = (t >= t_start) & (t <= t_end)
    # 上升沿
    in_idx = (t >= t_start) & (t < t_start + fade_in)
    gate[in_idx] = 0.5 * (1.0 - np.cos(np.pi * (t[in_idx] - t_start) / max(1e-4, fade_in)))
    # 稳态
    sustain_idx = (t >= t_start + fade_in) & (t <= t_end - fade_out)
    gate[sustain_idx] = 1.0
    # 下降沿
    out_idx = (t > t_end - fade_out) & (t <= t_end)
    gate[out_idx] = 0.5 * (1.0 + np.cos(np.pi * (t[out_idx] - (t_end - fade_out)) / max(1e-4, fade_out)))
    return gate


def synth_ambient_drone(time):
    """
    1. 贯穿全篇的电影级深沉低频氛围垫音 (Cinematic Sub-Bass Drone & Harmonic Pads)
    基频 55Hz (A1) / 65.4Hz (C2)，辅以丰富谐波、微失真与温暖低通慢速调制
    """
    print("[1/5] 合成电影级深沉氛围低频垫底 (Ambient Drone)...")
    left = np.zeros_like(time)
    right = np.zeros_like(time)

    # 慢速 LFO 调制
    lfo1 = 0.5 + 0.5 * np.sin(2 * np.pi * 0.08 * time)
    lfo2 = 0.5 + 0.5 * np.cos(2 * np.pi * 0.05 * time)

    # 基频与八度分量
    freq_base = 65.41  # C2
    detune1 = 65.25
    detune2 = 65.60

    osc_sub = 0.35 * np.sin(2 * np.pi * (freq_base / 2) * time)  # 32.7Hz 次低音
    osc_fund_l = 0.30 * np.sin(2 * np.pi * detune1 * time + 0.2)
    osc_fund_r = 0.30 * np.sin(2 * np.pi * detune2 * time + 0.7)

    # 五度和声 (G2 = 98Hz)
    osc_fifth_l = 0.20 * np.sin(2 * np.pi * 98.0 * time + lfo1)
    osc_fifth_r = 0.20 * np.sin(2 * np.pi * 98.2 * time + lfo2)

    # 八度泛音 (C3 = 130.8Hz, G3 = 196Hz)
    osc_oct_l = 0.15 * np.sin(2 * np.pi * 130.81 * time)
    osc_oct_r = 0.15 * np.sin(2 * np.pi * 131.05 * time)

    left += osc_sub + osc_fund_l + osc_fifth_l + osc_oct_l
    right += osc_sub + osc_fund_r + osc_fifth_r + osc_oct_r

    # 全局总淡入与终章淡出
    overall_env = smooth_gate(time, 0.0, 120.0, fade_in=3.5, fade_out=4.0)
    return left * overall_env * 0.45, right * overall_env * 0.45


def synth_chords_and_harmonics(time):
    """
    2. 随行程海拔与地域心境流动的丝路五声交响和弦群 (Silk Road Modal Harmonies)
    - 兰州/河西: 苍茫开阔五度和弦 (C - G - D)
    - 额济纳: 明亮温润金秋大和弦 (C - E - G - B - D)
    - 怪树林: 凄清萧瑟小调和声 (D - F - A - C)
    - 嘉峪关: 雄浑军旅四度/五度铜管感
    - 敦煌/塔尔寺: 佛国梵音空灵八度和弦 (高泛音飘渺)
    - 当金山 (3648m): 随海拔飙升的张力升音与冷冽泛音
    - 翡翠湖/茶卡: 晶莹玻璃清脆空灵琶音
    - 青海湖/西宁: 浩瀚大调交响凯旋和弦
    """
    print("[2/5] 合成随海拔与地域流动的丝路交响和弦群 (Modal Harmonies)...")
    left = np.zeros_like(time)
    right = np.zeros_like(time)

    # 各乐段和弦配置 (时段, 频率列表, 音量)
    progressions = [
        # Shot 01: 兰州黄河 (0-7s)
        {"t0": 0.0, "t1": 7.0, "freqs": [130.8, 196.0, 261.6, 392.0], "vol": 0.28},
        # Shot 02: 临泽丹霞 (7-14s)
        {"t0": 7.0, "t1": 14.0, "freqs": [146.8, 220.0, 293.7, 440.0], "vol": 0.32},
        # Shot 03: 河西千里戈壁 (14-22s)
        {"t0": 14.0, "t1": 22.0, "freqs": [110.0, 164.8, 220.0, 329.6], "vol": 0.30},
        # Shot 04: 额济纳金秋胡杨 (22-31s) - 璀璨金黄五声
        {"t0": 22.0, "t1": 31.0, "freqs": [196.0, 246.9, 293.7, 392.0, 493.9, 587.3], "vol": 0.38},
        # Shot 05: 怪树林与黑城 (31-39s) - 苍凉孤寂
        {"t0": 31.0, "t1": 39.0, "freqs": [146.8, 174.6, 220.0, 261.6], "vol": 0.34},
        # Shot 06: 嘉峪关天下雄关 (39-47s) - 雄浑威严
        {"t0": 39.0, "t1": 47.0, "freqs": [130.8, 196.0, 261.6, 392.0, 523.2], "vol": 0.40},
        # Shot 07: 瓜州大地之子 (47-54s) - 温润宁静
        {"t0": 47.0, "t1": 54.0, "freqs": [174.6, 220.0, 261.6, 349.2, 440.0], "vol": 0.30},
        # Shot 08: 敦煌莫高窟 (54-63s) - 佛窟灵音
        {"t0": 54.0, "t1": 63.0, "freqs": [220.0, 329.6, 440.0, 659.2, 880.0], "vol": 0.42},
        # Shot 09: 鸣沙山月牙泉 (63-71s) - 沙泉五声
        {"t0": 63.0, "t1": 71.0, "freqs": [196.0, 246.9, 293.7, 392.0, 440.0], "vol": 0.35},
        # Shot 10: 当金山 3648m (71-79s) - 高原攀升冷冽张力
        {"t0": 71.0, "t1": 79.0, "freqs": [261.6, 311.1, 392.0, 523.2, 622.2], "vol": 0.45},
        # Shot 11: 大柴旦翡翠湖 (79-87s) - 晶莹纯净
        {"t0": 79.0, "t1": 87.0, "freqs": [329.6, 440.0, 554.4, 659.2, 880.0], "vol": 0.36},
        # Shot 12: 茶卡天空之镜 (87-95s) - 镜面倒影空灵
        {"t0": 87.0, "t1": 95.0, "freqs": [261.6, 392.0, 523.2, 784.0, 1046.5], "vol": 0.35},
        # Shot 13: 青海湖圣湖 (95-104s) - 碧波万顷浩瀚大调
        {"t0": 95.0, "t1": 104.0, "freqs": [130.8, 164.8, 196.0, 261.6, 329.6, 392.0], "vol": 0.45},
        # Shot 14: 塔尔寺宗喀巴 (104-110s) - 庄严肃穆梵音
        {"t0": 104.0, "t1": 110.0, "freqs": [110.0, 164.8, 220.0, 329.6, 440.0], "vol": 0.42},
        # Shot 15: 西宁大环线凯旋 (110-116s) - 壮丽凯旋大交响
        {"t0": 110.0, "t1": 116.0, "freqs": [130.8, 196.0, 261.6, 329.6, 392.0, 523.2, 659.2], "vol": 0.50},
        # Shot 16: 终章余韵 (116-120s) - 温暖回响渐隐
        {"t0": 116.0, "t1": 120.0, "freqs": [130.8, 196.0, 261.6, 392.0], "vol": 0.25}
    ]

    for prog in progressions:
        idx0 = max(0, int(prog["t0"] * SAMPLE_RATE))
        idx1 = min(TOTAL_SAMPLES, int(prog["t1"] * SAMPLE_RATE))
        sub_time = time[idx0:idx1]
        gate = smooth_gate(sub_time, prog["t0"], prog["t1"], fade_in=1.2, fade_out=1.2)
        chord_sig_l = np.zeros_like(sub_time)
        chord_sig_r = np.zeros_like(sub_time)

        for i, f in enumerate(prog["freqs"]):
            pan = 0.5 + 0.3 * ((-1) ** i)
            phase_l = (i * 0.7) % (2 * np.pi)
            phase_r = (i * 1.3) % (2 * np.pi)
            sig = np.sin(2 * np.pi * f * sub_time + phase_l) + 0.25 * np.sin(2 * np.pi * (f * 2) * sub_time + phase_r)
            chord_sig_l += sig * (1.0 - pan)
            chord_sig_r += sig * pan

        scale = prog["vol"] / len(prog["freqs"])
        left[idx0:idx1] += chord_sig_l * gate * scale
        right[idx0:idx1] += chord_sig_r * gate * scale

    return left, right


def synth_foley_effects(time):
    """
    3. 电影级拟音工程 (Procedural Foley Sound FX):
    - 黄河与青海湖水波涛声 (River flow & ocean surf)
    - 戈壁长途高速公路轮胎风噪与引擎低鸣 (Highway hum & engine rumble)
    - 额济纳大漠风沙与胡杨落叶纷飞声 (Desert wind gusts & foliage whisper)
    - 丝路驼队清脆铜铃 (Camel Caravan Bells)
    - 敦煌石窟与塔尔寺空灵青铜大钟/铜钵回响 (Bronze temple chime / singing bowl)
    - 大柴旦/茶卡盐湖快门快照拟音 (Camera shutter clicks)
    - 当金山口高海拔呼啸风雪 (Alpine blizzard gale)
    """
    print("[3/5] 合成电影级全景拟音工程 (Procedural Foley FX)...")
    np.random.seed(42)
    left = np.zeros_like(time)
    right = np.zeros_like(time)

    # ----------------------------------------------------
    # A. 滔滔流水声 (黄河 0-7s & 青海湖 95-104s)
    # ----------------------------------------------------
    white_noise = np.random.normal(0, 1, TOTAL_SAMPLES)

    # 黄河奔流 (低频滚滚)
    river_gate = smooth_gate(time, 0.0, 7.0, fade_in=1.5, fade_out=1.5)
    river_surf = np.sin(2 * np.pi * 0.4 * time) * 0.5 + 0.5
    river_audio = white_noise * (0.15 + 0.25 * river_surf) * river_gate * 0.20
    left += river_audio * 0.8
    right += river_audio * 0.7

    # 青海湖波涛 (起伏涌浪)
    lake_gate = smooth_gate(time, 95.0, 104.0, fade_in=1.8, fade_out=1.8)
    lake_surf = (np.sin(2 * np.pi * 0.25 * time) * 0.5 + 0.5) ** 2
    lake_audio = white_noise * lake_surf * lake_gate * 0.25
    left += lake_audio * 0.65
    right += lake_audio * 0.85

    # ----------------------------------------------------
    # B. 戈壁公路引擎低鸣与胎噪 (Shot 03: 14-22s & Shot 10: 71-79s)
    # ----------------------------------------------------
    gobi_gate = smooth_gate(time, 14.0, 22.0, fade_in=1.5, fade_out=1.5)
    dangjin_gate = smooth_gate(time, 71.0, 79.0, fade_in=1.2, fade_out=1.2)
    engine_rumble = (
        0.5 * np.sin(2 * np.pi * 58.0 * time) +
        0.3 * np.sin(2 * np.pi * 116.0 * time) +
        0.2 * np.sin(2 * np.pi * 174.0 * time)
    )
    left += engine_rumble * gobi_gate * 0.22 + engine_rumble * dangjin_gate * 0.28
    right += engine_rumble * gobi_gate * 0.22 + engine_rumble * dangjin_gate * 0.28

    # ----------------------------------------------------
    # C. 呼啸沙漠风沙与怪树林古风 (Shot 03, Shot 05, Shot 10)
    # ----------------------------------------------------
    wind_gate_5 = smooth_gate(time, 31.0, 39.0, fade_in=1.2, fade_out=1.2)
    wind_gate_10 = smooth_gate(time, 71.0, 79.0, fade_in=1.0, fade_out=1.0)
    wind_lfo = (np.sin(2 * np.pi * 0.15 * time) * 0.5 + 0.5) ** 1.5
    wind_sound = white_noise * wind_lfo * 0.30
    left += wind_sound * wind_gate_5 * 0.35 + wind_sound * wind_gate_10 * 0.45
    right += wind_sound * wind_gate_5 * 0.40 + wind_sound * wind_gate_10 * 0.40

    # ----------------------------------------------------
    # D. 丝路大漠古骆驼铃铛 (Camel Bells: Shot 03 & Shot 09)
    # ----------------------------------------------------
    def add_bell(t_event, bell_freq, bell_gain):
        idx = int(t_event * SAMPLE_RATE)
        dur = int(1.8 * SAMPLE_RATE)
        if idx + dur < TOTAL_SAMPLES:
            decay_t = np.linspace(0, 1.8, dur)
            env = np.exp(-decay_t * 3.8)
            bell_sig = (
                np.sin(2 * np.pi * bell_freq * decay_t) +
                0.6 * np.sin(2 * np.pi * (bell_freq * 2.76) * decay_t) +
                0.3 * np.sin(2 * np.pi * (bell_freq * 5.4) * decay_t)
            ) * env * bell_gain
            left[idx:idx + dur] += bell_sig * 0.7
            right[idx:idx + dur] += bell_sig * 0.5

    # 鸣沙山月牙泉 (63-71s) 驼队行进铃声 (每 1.4 秒一声)
    for bt in np.arange(64.0, 70.5, 1.35):
        add_bell(bt, 880.0, 0.28)
        add_bell(bt + 0.12, 1174.0, 0.22)

    # ----------------------------------------------------
    # E. 敦煌莫高窟与塔尔寺青铜大钟/铜磬 (Temple Bells: Shot 08 & Shot 14)
    # ----------------------------------------------------
    def add_temple_gong(t_event, base_f, gain):
        idx = int(t_event * SAMPLE_RATE)
        dur = int(6.0 * SAMPLE_RATE)
        if idx + dur < TOTAL_SAMPLES:
            decay_t = np.linspace(0, 6.0, dur)
            env = np.exp(-decay_t * 0.9)
            gong_sig = (
                1.0 * np.sin(2 * np.pi * base_f * decay_t) +
                0.7 * np.sin(2 * np.pi * (base_f * 2.02) * decay_t) +
                0.5 * np.sin(2 * np.pi * (base_f * 3.14) * decay_t) +
                0.3 * np.sin(2 * np.pi * (base_f * 4.45) * decay_t)
            ) * env * gain
            left[idx:idx + dur] += gong_sig * 0.6
            right[idx:idx + dur] += gong_sig * 0.6

    add_temple_gong(54.2, 185.0, 0.45)  # 莫高窟开篇梵钟
    add_temple_gong(104.2, 146.8, 0.48) # 塔尔寺庄严巨钟
    add_temple_gong(116.2, 130.8, 0.35) # 终章余韵铭钟

    # ----------------------------------------------------
    # F. 单反快门声 (Camera Shutter: 盐湖/翡翠湖 Shot 11 & 12)
    # ----------------------------------------------------
    def add_shutter(t_event):
        idx = int(t_event * SAMPLE_RATE)
        dur = int(0.12 * SAMPLE_RATE)
        if idx + dur < TOTAL_SAMPLES:
            st = np.linspace(0, 0.12, dur)
            click = np.random.normal(0, 1, dur) * np.exp(-st * 60) * 0.35
            left[idx:idx + dur] += click
            right[idx:idx + dur] += click

    add_shutter(81.5)
    add_shutter(89.5)

    return left, right


def synth_glockenspiel_and_arpeggios(time):
    """
    4. 高音灵动华彩乐段 (Glockenspiel, Harp & Starlight Shimmer)
    在额济纳胡杨、茶卡盐湖、全景凯旋与终章星空中绽放清脆华彩
    """
    print("[4/5] 合成高音清亮华彩与星空琶音 (Shimmer & Arpeggios)...")
    left = np.zeros_like(time)
    right = np.zeros_like(time)

    def add_ping(t_event, f, pan, gain):
        idx = int(t_event * SAMPLE_RATE)
        dur = int(1.2 * SAMPLE_RATE)
        if idx + dur < TOTAL_SAMPLES:
            decay_t = np.linspace(0, 1.2, dur)
            env = np.exp(-decay_t * 5.0)
            ping = (np.sin(2 * np.pi * f * decay_t) + 0.3 * np.sin(2 * np.pi * f * 2 * decay_t)) * env * gain
            left[idx:idx + dur] += ping * (1.0 - pan)
            right[idx:idx + dur] += ping * pan

    # 额济纳金秋胡杨 (23-30s) 金叶闪烁清亮琶音
    notes_ejina = [523.2, 587.3, 659.2, 784.0, 880.0, 1046.5]
    for i, t_hit in enumerate(np.arange(23.0, 30.5, 0.4)):
        note = notes_ejina[i % len(notes_ejina)]
        pan = 0.2 + 0.6 * ((i % 5) / 4.0)
        add_ping(t_hit, note, pan, 0.22)

    # 茶卡盐湖 (88-94s) 天空之镜水滴轻吟
    notes_chaka = [880.0, 1046.5, 1318.5, 1568.0, 1760.0]
    for i, t_hit in enumerate(np.arange(88.0, 94.5, 0.6)):
        note = notes_chaka[i % len(notes_chaka)]
        pan = 0.5 + 0.4 * ((-1) ** i)
        add_ping(t_hit, note, pan, 0.24)

    # 终章星空 (116-119s) 银河繁星点点
    for i, t_hit in enumerate(np.arange(116.5, 119.5, 0.35)):
        note = 1200.0 + (i * 173) % 800
        add_ping(t_hit, note, (i % 7) / 6.0, 0.18)

    return left, right


def master_and_export_wav(left, right, output_path="soundtrack.wav"):
    """
    5. 母带工程处理与导出 (Mastering Limiter & 16-bit 48kHz WAV Export)
    - 软削波与软饱和限制器 (Soft-knee Limiting)
    - 动态峰值规范化 (-1.0 dBFS Headroom)
    - 标准 16-bit PCM 立体声写入
    """
    print("[5/5] 母带限制与 48kHz 16-bit 双声道立体声封装导出...")
    # 混音总轨叠加
    master_l = left
    master_r = right

    # 检查峰值并软限幅
    peak = max(np.max(np.abs(master_l)), np.max(np.abs(master_r)))
    print(f"-> 混音总轨原始峰值: {peak:.3f}")

    if peak > 0.95:
        # 类似双曲正切软饱和限制
        master_l = np.tanh(master_l / peak * 1.2) * 0.92
        master_r = np.tanh(master_r / peak * 1.2) * 0.92
    else:
        gain = 0.92 / max(1e-4, peak)
        master_l = master_l * gain
        master_r = master_r * gain

    final_peak = max(np.max(np.abs(master_l)), np.max(np.abs(master_r)))
    print(f"-> 母带处理后目标峰值 (-0.7 dBFS): {final_peak:.3f}")

    # 转换至 16-bit signed integer (-32768 ~ 32767)
    int_l = np.int16(np.clip(master_l * 32767.0, -32768, 32767))
    int_r = np.int16(np.clip(master_r * 32767.0, -32768, 32767))

    # 交错双声道数据 [L0, R0, L1, R1, ...]
    interleaved = np.empty((TOTAL_SAMPLES * 2,), dtype=np.int16)
    interleaved[0::2] = int_l
    interleaved[1::2] = int_r

    # 写入标准 WAV
    with wave.open(output_path, "wb") as wav_file:
        wav_file.setnchannels(2)        # 立体声双声道
        wav_file.setsampwidth(2)        # 16-bit = 2 字节
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(interleaved.tobytes())

    file_size_mb = (TOTAL_SAMPLES * 4 + 44) / (1024 * 1024)
    print(f"✔ 成功生成高保真立体声母带: {output_path}")
    print(f"  格式: 48,000 Hz, 16-bit, 2-Channel Stereo PCM")
    print(f"  时长: {DURATION_SEC} 秒 ({TOTAL_SAMPLES} 采样点)")
    print(f"  文件大小: {file_size_mb:.2f} MB")


def main():
    print("==================================================================")
    print(" 西行壮歌 · 丝路与额济纳自驾大环线电影级配乐音效合成流水线")
    print("==================================================================")
    drone_l, drone_r = synth_ambient_drone(TIME)
    chord_l, chord_r = synth_chords_and_harmonics(TIME)
    foley_l, foley_r = synth_foley_effects(TIME)
    glock_l, glock_r = synth_glockenspiel_and_arpeggios(TIME)

    # 汇总总声道
    mix_left = drone_l + chord_l + foley_l + glock_l
    mix_right = drone_r + chord_r + foley_r + glock_r

    master_and_export_wav(mix_left, mix_right, "soundtrack.wav")
    print("==================================================================")
    print(" 所有 16 个镜头时间轴配乐与 Foley 音效已严丝合缝对齐！")
    print("==================================================================")


if __name__ == "__main__":
    main()
