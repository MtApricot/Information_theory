import collections
import random

file_name = 'EnText.txt'

with open(file_name, 'r', encoding='utf-8') as f:
    text = f.read().lower()

counts = collections.Counter(text)
total = len(text)

transitions = collections.defaultdict(lambda: collections.defaultdict(int))
for i in range(len(text) - 1):
    prev = text[i]
    curr = text[i+1]
    transitions[prev][curr] += 1

random.seed(42)
generate = ""

chars = list(counts.keys())
weights = [counts[c] / total for c in chars]
current_char = random.choices(chars, weights=weights, k=1)[0] 
generate += current_char

for _ in range(99):
    next_chars = list(transitions[current_char].keys())
    
    if not next_chars: 
        current_char = random.choices(chars, weights=weights, k=1)[0]
    else:
        next_weights = [transitions[current_char][c] for c in next_chars]
        current_char = random.choices(next_chars, weights=next_weights, k=1)[0]
    
    generate += current_char

print("【(2-3) 単純マルコフ情報源から生成されたテキスト】")
print("-" * 50)
print(generate)
print("-" * 50)