import collections

file_name = 'EnText.txt'

with open(file_name, 'r', encoding='utf-8') as f:
    text = f.read().lower()

# 総文字数
total = len(text)

# 出現回数カウント
char_counts = collections.Counter(text)

# 出現回数が多い順にソート
sorted_chars = sorted(char_counts.items(), key=lambda x: x[1], reverse=True)

# 結果の表示
print(f"総文字数: {total} 文字\n")
print("-" * 45)
print(f"{'文字':<10} | {'出現回数':<10} | {'出現確率':<10}")
print("-" * 45)

for char, count in sorted_chars:
    p = count / total

    display = char
    if char == '\n':
        display = '改行'
    elif char == ' ':
        display = '空白'
    elif char == '\r':
        display = '復帰'
    elif char == '\t':
        display = 'タブ'
    
    print(f"{display:<8} | {count:<10} | {p:.6f}")