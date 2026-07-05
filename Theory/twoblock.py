import collections
import math

file_name = 'EnText.txt'

with open(file_name, 'r', encoding='utf-8') as f:
    text = f.read().lower()

bigrams = [text[i:i+2] for i in range(len(text)-1)]
total = len(bigrams)
counts = collections.Counter(bigrams)

h2 = 0
l_sf = 0

for count in counts.values():
    p = count / total

    if p > 0:
        h2 -= p * math.log2(p)

    li = math.ceil(-math.log2(p))
    l_sf += p * li

print(f"【(1-6) 2次ブロック化の解析結果】")
print(f"全ブロック数: {total}")
print(f"ブロックの種類数: {len(counts)}")
print(f"2次エントロピー H(X^2): {h2:.6f} [bit/block]")
print(f"1文字あたりのエントロピー H(X^2)/2: {h2/2:.6f} [bit/char]")
print(f"シャノン・ファノ平均符号語長 L_SF: {l_sf:.6f} [bit/block]")
print(f"1文字あたりの平均符号語長 L_SF/2: {l_sf/2:.6f} [bit/char]")