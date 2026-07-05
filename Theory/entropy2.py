import collections
import math

file_name = 'EnText.txt'

with open(file_name, 'r', encoding='utf-8') as f:
    text = f.read().lower()

counts = collections.Counter(text)
total_all = len(text)

transitions = collections.defaultdict(lambda: collections.defaultdict(int))
for i in range(len(text) - 1):
    prev = text[i]
    curr = text[i+1]
    transitions[prev][curr] += 1

entropy_rate = 0

for prev_char, count in counts.items():
    p = count / total_all

    total_transitions = sum(transitions[prev_char].values())

    if total_transitions == 0:
        continue

    cond_entropy = 0
    for curr_char, countj in transitions[prev_char].items():
        p_cond = countj / total_transitions
        if p_cond > 0:
            cond_entropy -= p_cond * math.log2(p_cond)

    entropy_rate += p * cond_entropy

print(f"総文字数: {total_all} 文字")
print(f"単純マルコフ情報源のエントロピーレート H: {entropy_rate:.6f} [bit/文字]")