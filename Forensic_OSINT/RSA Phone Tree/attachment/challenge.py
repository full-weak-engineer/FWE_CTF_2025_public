import numpy as np
from scipy.io.wavfile import write
from Crypto.Util.number import getPrime, bytes_to_long
import random

dtmf_freqs = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477), 'A': (697, 1633),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477), 'B': (770, 1633),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477), 'C': (852, 1633),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477), 'D': (941, 1633),
}

def text_to_tone(text, filename, fs=8000, tone_time=0.08, silence_time=0.10):
    samples = []
    for char in text:
        if char not in dtmf_freqs:
            continue
        f1, f2 = dtmf_freqs[char]
        t = np.linspace(0, tone_time, int(fs * tone_time), endpoint=False)
        
        phase1 = random.uniform(0, 2 * np.pi)
        phase2 = random.uniform(0, 2 * np.pi)
        tone = 0.5 * np.sin(2 * np.pi * f1 * t + phase1) + 0.5 * np.sin(2 * np.pi * f2 * t + phase2)
        samples.append(tone)
        samples.append(np.zeros(int(fs * silence_time)))
    sig = np.concatenate(samples)
    sig = (sig * 32767).astype(np.int16)
    write(filename, fs, sig)

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 65537

flag = b"dummy{What is Your Telephone Number? *^_^* }"
m = bytes_to_long(flag)
c = pow(m, e, n)

p_str = str(p)
q_str = str(q)
c_str = str(c)

text_to_tone(p_str, "p_dial.wav")
text_to_tone(q_str, "q_dial.wav")
text_to_tone(c_str, "message.wav")
