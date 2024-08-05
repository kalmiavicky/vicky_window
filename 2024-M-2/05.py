# 設置支持中文的字體(macbook => Arial Unicode MS)
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 箱型圖
plt.figure(figsize=(3,5))
plt.boxplot(anal_data['平均價(元/公斤)'],showmeans=True)
plt.title('平均價(元/公斤)')
plt.show()
