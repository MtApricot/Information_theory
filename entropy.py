import collections
import math

file_name = 'EnText.txt'

with open(file_name, 'r', encoding='utf-8') as f:
    text = f.read().lower()

total = len(text)
char_counts = collections.Counter(text)

entropy = 0
for count in char_counts.values():
    p = count / total
    if p > 0:
        entropy -= p * math.log2(p)

print(f"総文字数: {total} 文字")
print(f"出現記号の種類数: {len(char_counts)} 種類")
print(f"エントロピー H(X): {entropy:.6f} [bit/文字]")