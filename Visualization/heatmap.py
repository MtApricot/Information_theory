import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import platform

# 1. 日本語フォントの設定
system = platform.system()
if system == 'Darwin': plt.rcParams['font.family'] = 'Hiragino Sans'
elif system == 'Windows': plt.rcParams['font.family'] = 'MS Gothic'
else: plt.rcParams['font.family'] = 'DejaVu Sans'

# 2. データの読み込みと前処理
df = pd.read_csv("steam_games_for_GC54091_utf8bom.csv")

df['price_usd'] = pd.to_numeric(df['price_usd'], errors='coerce')
df['review_score'] = pd.to_numeric(df['review_score'], errors='coerce')
df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce')
df = df.dropna(subset=['price_usd', 'review_score', 'review_count'])
df = df[df['price_usd'] >= 0].copy()

# 価格帯のビン分割 
bins = [-0.01, 0, 5, 15, 30, 10000]
# 【修正箇所】下から上へ配置するため、並び順（インデックス）をはじめから逆順にする
labels_reversed = ['$30+', '$15-30', '$5-15', '$0-5', 'Free']
df['price_tier'] = pd.cut(df['price_usd'], bins=bins, labels=['Free', '$0-5', '$5-15', '$15-30', '$30+'])

# ジャンルの展開 
df['genres'] = df['genres'].apply(lambda x: ';'.join([g.strip() for g in str(x).split(';')]))
df_exploded = df.assign(genres=df['genres'].str.split(';')).explode('genres')

target_genres = ['Action', 'Adventure', 'Casual', 'Indie', 'RPG', 'Simulation', 'Strategy']
df_filtered = df_exploded[df_exploded['genres'].isin(target_genres)]

# 3. 重み付き平均の計算 
def weighted_mean(group):
    w = group['review_count'].values
    s = group['review_score'].values
    return np.average(s, weights=w) if np.sum(w) > 0 else np.nan

pivot_score = df_filtered.groupby(['price_tier', 'genres']).apply(weighted_mean, include_groups=False).unstack()
pivot_count = df_filtered.groupby(['price_tier', 'genres']).size().unstack()

# 【修正箇所】価格帯の順序を逆順（上から順に $30+ -> Free）にして並び替える
# これにより、imshow(origin='upper') で描画した際に、一番下が Free、一番上が $30+ になります
pivot_score = pivot_score.reindex(index=labels_reversed, columns=target_genres)
pivot_count = pivot_count.reindex(index=labels_reversed, columns=target_genres)

# 4. 階層化ロジック（切り捨て基準）
def bin_score(val):
    if pd.isna(val): return 0
    truncated_val = int(val)
    if truncated_val >= 91: return 4
    elif truncated_val >= 81: return 3
    elif truncated_val >= 71: return 2
    elif truncated_val >= 61: return 1
    else: return 0

pivot_binned = pivot_score.map(bin_score)

# 5段階のグレー（白に近い〜黒に近い）を固定
colors = ['#f7f7f7', '#d9d9d9', '#969696', '#636363', '#252525']
cmap = mcolors.ListedColormap(colors)
norm = mcolors.BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5, 4.5], cmap.N)

# 5. ヒートマップの描画
fig, ax = plt.subplots(figsize=(10, 7))
heatmap = ax.imshow(pivot_binned.values, cmap=cmap, norm=norm, aspect='auto', origin='upper')

# 数値のテキスト描画と赤枠処理
for i in range(len(pivot_score)):
    for j in range(len(pivot_score.columns)):
        val = pivot_score.iloc[i, j]
        binned_val = pivot_binned.iloc[i, j]
        
        text_color = 'white' if binned_val == 4 else 'black' 
        
        if not pd.isna(val):
            ax.text(j, i, f"{int(val)}", ha='center', va='center', color=text_color, fontweight='bold', fontsize=12)
        
        if pivot_count.iloc[i, j] < 10: 
            rect = patches.Rectangle((j-0.5, i-0.5), 1, 1, linewidth=2.8, edgecolor='red', facecolor='none') 
            ax.add_patch(rect) 

# 軸の設定
ax.set_xticks(np.arange(len(pivot_score.columns)))
ax.set_xticklabels(pivot_score.columns)
ax.set_yticks(np.arange(len(pivot_score.index)))
ax.set_yticklabels(pivot_score.index)

ax.set_xlabel('ジャンル', fontsize=12)
ax.set_ylabel('価格帯', fontsize=12)
ax.set_title('Steam市場: 価格帯×ジャンル別 レビュースコア階層マップ', fontsize=14)

cbar = plt.colorbar(heatmap, ticks=[0, 1, 2, 3, 4])
cbar.ax.set_yticklabels(['60以下', '61-70', '71-80', '81-90', '91-100'])
cbar.set_label('重み付き平均レビュースコア (%)', rotation=270, labelpad=15)

plt.tight_layout()
plt.savefig('steam_heatmap_ja.png', dpi=300)
plt.show()