import collections
import heapq

file_name = 'EnText.txt'

with open(file_name, 'r', encoding='utf-8') as f:
    text = f.read().lower()

total = len(text)
char_counts = collections.Counter(text)

heap = [[count / total, [char, ""]] for char, count in char_counts.items()]
heapq.heapify(heap)

while len(heap) > 1:
    lo = heapq.heappop(heap)
    hi = heapq.heappop(heap)

    for pair in lo[1:]:
        pair[1] = '0' + pair[1]
    for pair in hi[1:]:
        pair[1] = '1' + pair[1]

    heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

huffman = {item[0]: item[1] for item in heapq.heappop(heap)[1:]}

print(f"{'文字':<10} | {'確率 (p)':<10} | {'符号語':<15} | {'長さ (li)'}")
print("-" * 55)

L_bar = 0
for char, count in sorted(char_counts.items(), key=lambda x: x[1], reverse=True):
    p = count / total
    code = huffman[char]
    li = len(code)

    L_bar += p * li

    label = char
    if char == '\n': label = '改行'
    elif char == ' ': label = '空白'
    elif char == '\r': label = '復帰'
    elif char == '\t': label = 'タブ'
    
    print(f"{label:<10} | {p:.6f} | {code:<15} | {li}")

print("-" * 55)
print(f"平均符号語長 L = {L_bar:.6f} [bit/文字]")