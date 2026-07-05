import collections

file_name = 'EnText.txt'

with open(file_name, 'r', encoding='utf-8') as f:
    text = f.read().lower()

counts = collections.Counter(text)

transitions = collections.defaultdict(lambda: collections.defaultdict(int))
for i in range(len(text) - 1):
    prev = text[i]
    curr = text[i+1]
    transitions[prev][curr] += 1

sorted_chars = sorted(counts.items(), key=lambda x: x[1], reverse=True)

print(f"{'前の文字':<6} | {'次の文字':<6} | {'条件付き確率 P(j|i)':<15}")
print("-" * 50)

for prev_char, _ in sorted_chars[:5]: 

    display_prev = prev_char
    if prev_char == '\n': display_prev = '改行'
    elif prev_char == ' ': display_prev = '空白'

    total = sum(transitions[prev_char].values())

    next_chars = sorted(transitions[prev_char].items(), key=lambda x: x[1], reverse=True)
    
    for curr_char, count in next_chars[:3]: 
        p = count / total
        
        display_curr = curr_char
        if curr_char == '\n': display_curr = '改行'
        elif curr_char == ' ': display_curr = '空白'
        
        print(f"{display_prev:<10} | {display_curr:<10} | {p:.6f}")
    print("-" * 50)