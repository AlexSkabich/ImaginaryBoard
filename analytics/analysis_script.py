import matplotlib.pyplot as pt
import pandas as pd
import numpy as np

df_monetization = pd.read_csv('imageboard_alternative_monetization_stats.csv')
df_bot_traffic = pd.read_csv('imageboard_bot_traffic_stats.csv')
df_users_cow = pd.read_csv('imageboard_users_stats.csv')

df_monetization['Weight'] = df_monetization['Platform_Role_Weight'].str.extract(r'(\d+)').astype(float)

df_bot_traffic['Total_Bot_Pct'] = df_bot_traffic['Total_Bot_Traffic_Pct'].str.replace('%', '').astype(float)
df_bot_traffic['Bad_Bots_Pct'] = df_bot_traffic['Bad_Bots_Pct'].str.replace('%', '').astype(float)

def parse_traffic(val):
    if pd.isna(val) or 'Data not found' in str(val): return 0.0
    val = str(val).lower()
    if 'million' in val or 'млн' in val:
        if 'year' in val or 'год' in val:
            return float(val.split()[0]) / 12.0
        return float(val.split()[0])
    elif 'thousand' in val or 'тысяч' in val:
        nums = [float(s) for s in val.replace('-', ' ').split() if s.replace('.','',1).isdigit()]
        avg_k = np.mean(nums) if nums else 0.0
        if 'day' in val or 'день' in val:
            return (avg_k * 30.0) / 1000.0
        return avg_k / 1000.0
    return 0.0

df_users_cow['4chan_M_Month'] = df_users_cow['4chan_Traffic'].apply(parse_traffic)
df_users_cow['2ch_M_Month'] = df_users_cow['2ch_hk_Traffic'].apply(parse_traffic)

fig, ax = pt.subplots(3, 1, figsize=(10, 12)) 

ax[0].bar(df_monetization['Monetization_Channel'], df_monetization['Weight'], color='skyblue', edgecolor='black')
ax[0].set_title('Доля каналов монетизации (Platform Role Weight)', fontsize=12)
ax[0].set_xlabel('Канал монетизации', fontsize=10)
ax[0].set_ylabel('Вес в структуре (%)', fontsize=10)
ax[0].tick_params(axis='x', rotation=15)
ax[0].grid(axis='y', alpha=0.7)

ax[1].plot(df_bot_traffic['Year'], df_bot_traffic['Total_Bot_Pct'], marker='o', label='Всего ботов (%)', color='red', linewidth=2)
ax[1].plot(df_bot_traffic['Year'], df_bot_traffic['Bad_Bots_Pct'], marker='s', label='Плохие боты (%)', color='darkred', linewidth=2)
ax[1].set_title('Динамика бот-трафика', fontsize=12)
ax[1].set_xlabel('Год', fontsize=10)
ax[1].set_ylabel('Процент трафика (%)', fontsize=10)
ax[1].legend()
ax[1].grid(alpha=0.7)

ax[2].plot(df_users_cow['Year'], df_users_cow['4chan_M_Month'], marker='o', label='4chan (млн/мес)', color='blue', linewidth=2)
ax[2].plot(df_users_cow['Year'], df_users_cow['2ch_M_Month'], marker='s', label='2ch.hk (млн/мес)', color='orange', linewidth=2)
ax[2].set_title('Динамика уникальных посетителей', fontsize=12)
ax[2].set_xlabel('Год', fontsize=10)
ax[2].set_ylabel('Млн посетителей в месяц', fontsize=10)
ax[2].legend()
ax[2].grid(alpha=0.7)

pt.tight_layout()
pt.show()
