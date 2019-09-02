import pandas as pd
import re
import matplotlib.pyplot as plt

def changeFormat(s):
    '''清洗数据'''
    num = 0
    if s == 'no time':
        return 0
    h = re.search(re.compile(r'[0-9]{0,2}h'), s)
    if h is not None:
        h = h.group(0).replace('h', '')
        if h != '':
            num = int(h) * 60
    m = re.search(re.compile(r'[0-9]{0,2}m'), s)
    if m is not None:
        m = m.group(0).replace('m', '')
        if m != '':
            num += int(m)

    return num

data = pd.read_excel('19.8.xlsx')
data = data.set_index('Date')
data = data.fillna('0')

data = data.applymap(changeFormat)  # 清洗数据
data.index = [x for x in range(1, 32)]


# 计算8月详细时间分配
total = data.sum()

total_1 = total.iloc[3:8]
figure_pie = plt.pie(total_1.values, labels=total_1.index, autopct='%3.1f%%',
        colors=['b', 'royalblue', 'gray', 'coral', 'orangered'])
plt.title('Time Distribution')
plt.savefig('Time_Distribution')


total_detailed = total.iloc[9:]
total_detailed[1],total_detailed[2] = total_detailed[2],total_detailed[1]
print(total_detailed)
plt.pie(total_detailed.values, labels=total_detailed.index, autopct='%3.1f%%')
plt.title('Detailed Time Distribution')
plt.savefig('Detailed_Time_Distribution')

# 每日总时间
figure1 = data['TotalTime'].plot(color='b', alpha=0.5)
x = range(1, 32)
y = range(0, 660)

_x_ticks = ["Day{}".format(i) for i in x if i < 32]
plt.xticks(x[::3], _x_ticks[::3], rotation=45)
plt.ylim((0, 660))
plt.title('Total Time on Computer in August')
plt.ylabel('Time/min')
plt.xlabel('Date')
plt.savefig('Total_Time_on_Computer_in_August')

data_main = data[['VeryProductiveTime', 'ProductiveTime', 'NeutralTime', 'DistractingTime', 'VeryDistractingTime']]
figure2 = data_main.plot.barh(stacked=True, color=['b', 'royalblue', 'gray', 'coral', 'orangered'], alpha=0.7)
plt.title('Detailed Time on Computer in August')
plt.savefig('Detailed_Time_on_Computer_in_August')
plt.show()


