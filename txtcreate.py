import collections
import random

file_name = 'EnText.txt'

with open(file_name, 'r', encoding='utf-8') as f:
    text = f.read().lower()

char_counts = collections.Counter(text)
total = len(text)

chars = list(char_counts.keys())
weights = [char_counts[c] / total for c in chars]

random.seed(42) 
create_list = random.choices(chars, weights=weights, k=100)
create_text = "".join(create_list)

print("【(1-5) 生成された100文字のテキスト】")
print("-" * 50)
print(create_text)
print("-" * 50)