FLAG = b"fwectf{**REDACTED**}"

assert len(FLAG) < 30

"""
novel.txtはChatGPT 5 Autoによって生成された、UTF-8(BOMなし、改行LF)で書かれた小説です。

プロンプト(一部修正):
「**REDACTED**」という単語から連想される、1500字程度の小説を書いてください。
"""
novel = open("novel.txt", "rb").read()

encrypted = bytes([a ^ FLAG[i % len(FLAG)] for i, a in enumerate(novel)])
open("encrypted.txt", "wb").write(encrypted)