

# 強制使用系統默認字型
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']

# 測試字型設定
plt.figure(figsize=(10, 6))
plt.text(0.5, 0.5, '測試文本', fontsize=12, ha='center')
plt.show()