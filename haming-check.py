import numpy as np
from itertools import product

H = np.array([
    [0, 0, 0, 1, 1, 1, 1],
    [0, 1, 1, 0, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 1]
], dtype=int)

print("パリティ検査行列 H:")
print(H)

H_standard = np.array([
    [0, 1, 1, 1, 1, 0, 0],
    [1, 0, 1, 1, 0, 1, 0],
    [1, 1, 0, 1, 0, 0, 1]
], dtype=int)

print("\n標準形のパリティ検査行列 H':")
print(H_standard)

G_R = H_standard[:, :4]
print("\nG_R行列:")
print(G_R)


I_k = np.eye(4, dtype=int)
G = np.vstack([I_k, G_R])

print("\n生成行列 G:")
print(G)

print("\n【確認】H'G = O:")
result = np.dot(H_standard, G) % 2
print(result)

print(f"\nH'G = O が成立: {np.all(result == 0)}")

def find_all_codewords(gen_matrix):
    k = gen_matrix.shape[1]
    codewords = []
    for bits in product([0, 1], repeat=k):
        u = np.array(bits, dtype=int)
        x = np.dot(gen_matrix, u) % 2
        codewords.append(x)
    return codewords

print("\n--- すべての符号語の列挙 ---")
all_cw = find_all_codewords(G)
weights = []

for i, cw in enumerate(all_cw):
    w = np.sum(cw)
    weights.append(w)
    print(f"No.{i+1:2d}: {''.join(map(str, cw))} (重み: {w})")

non_zero_weights = [w for w in weights if w > 0]
if non_zero_weights:
    print(f"\n最小ハミング距離 : {min(non_zero_weights)}")