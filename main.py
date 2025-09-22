# 动态可视化：读取 CSV 并动态展示温度随时间变化

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import font_manager

# 设置支持中文的字体（如SimHei）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 修改为你的 CSV 路径
csv_path = r"c:\\Users\\37503\\OneDrive\\Desktop\\CLMMAXT_HKO_.csv"


# 自动检测分隔符
import csv
with open(csv_path, 'r', encoding='utf-8') as f:
	sample = f.read(1024)
	sniffer = csv.Sniffer()
	dialect = sniffer.sniff(sample)
	delimiter = dialect.delimiter

# 跳过前两行说明，从第3行开始用逗号分隔读取
df = pd.read_csv(csv_path, skiprows=2, header=None, encoding='utf-8')
# 只保留前5列：年、月、日、温度、完整性
df = df.iloc[:, :5]
df.columns = ['year', 'month', 'day', 'temperature', 'integrity']

# 过滤掉包含非数字（如'年/Year'）的行
df = df[df['year'].apply(lambda x: str(x).isdigit())]
# 温度转为数值
df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
# 去除无效温度
df = df.dropna(subset=['temperature'])
# 合成日期，跳过无效日期
def try_make_date(row):
	try:
		return pd.Timestamp(int(row['year']), int(row['month']), int(row['day']))
	except Exception:
		return pd.NaT
df['date'] = df.apply(try_make_date, axis=1)
df = df.dropna(subset=['date'])

# 显示前几行，便于调试
print(df.head())

# 动态可视化
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot([], [], 'b-', lw=2)

def init():
	ax.set_xlim(df['date'].iloc[0], df['date'].iloc[-1])
	ax.set_ylim(df['temperature'].min(), df['temperature'].max())
	line.set_data([], [])
	return line,

def update(frame):
	x_data.append(df['date'].iloc[frame])
	y_data.append(df['temperature'].iloc[frame])
	line.set_data(x_data, y_data)
	return line,

ani = FuncAnimation(fig, update, frames=range(len(df)), init_func=init, blit=True, interval=10)
plt.xlabel('Date')
plt.ylabel('Daily maximum temperature(℃)')
plt.title('Hong Kong Observatory Daily Maximum Temperature Variations')
plt.tight_layout()
plt.show()
