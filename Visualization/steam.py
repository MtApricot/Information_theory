import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import platform

# 1. 日本語フォントの設定（環境自動判定）
system = platform.system()
if system == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'Hiragino Sans'
elif system == 'Windows':  # Windows
    plt.rcParams['font.family'] = 'MS Gothic'
else:  # Linux/その他
    plt.rcParams['font.family'] = 'DejaVu Sans'

# 2. データの読み込みと前処理
df = pd.read_csv("steam_games_for_GC54091_utf8bom.csv")
df = df[df['price_usd'] >= 0].copy()

# 価格帯の分類
bins = [-0.01, 0, 5, 15, 30, 10000]
labels = ['Free', '$0-5', '$5-15', '$15-30', '$30+']
df['price_tier'] = pd.cut(df['price_usd'], bins=bins, labels=labels)

# ジャンルのクレンジング
df['genres'] = df['genres'].apply(lambda x: ';'.join([g.strip() for g in str(x).split(';')]))
df_exploded = df.assign(genres=df['genres'].str.split(';')).explode('genres')

# ジャンル名対応表
target_genres = ['Action', 'Adventure', 'Indie', 'Casual', 'Simulation', 'RPG', 'Strategy']
df_filtered = df_exploded[df_exploded['genres'].isin(target_genres)]

# 3. 重み付き平均の計算
def weighted_mean(group):
    w = group['review_count']
    return np.average(group['review_score'], weights=w) if w.sum() > 0 else np.nan

pivot_weighted = df_filtered.groupby(['price_tier', 'genres']).apply(weighted_mean, include_groups=False).unstack()

# 4. パラレルコーディネートの描画
plt.figure(figsize=(12, 6))
x = np.arange(len(target_genres))

for tier in pivot_weighted.index:
    y = pivot_weighted.loc[tier, target_genres]
    plt.plot(x, y, marker='o', linewidth=3, label=tier)

# 軸の固定と日本語設定
plt.xticks(x, target_genres)
plt.xlim(0, len(target_genres) - 1)
plt.ylim(50, 100)

# タイトルとラベルを日本語で
plt.title('Steam市場: 価格帯別 重み付きレビュースコア推移', fontsize=14, fontweight='bold')
plt.ylabel('重み付き平均レビュースコア (%)', fontsize=12)
plt.xlabel('ジャンル', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title='価格帯')

plt.tight_layout()
plt.savefig('steam.png', dpi=300)
plt.show()