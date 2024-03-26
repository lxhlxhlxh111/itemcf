import pandas as pd
# 处理input2，生成clean2

file_path = 'input2.csv'
data = pd.read_csv(file_path)

# 删除"单位"列
data.drop(columns=['单位'], inplace=True)
data.drop(columns=['规格型号'], inplace=True)
data.drop(columns=['销售月份'], inplace=True)

# 将"是否促销"列中的"是"改为"1"，"否"改为"0"
data['是否促销'] = data['是否促销'].replace({'是': 1, '否': 0})


# 找到并删除包含缺失值的行
rows_with_missing_values = data[data.isnull().any(axis=1)]
data.dropna(axis=0, how='any', inplace=True)

# 保存修改后的数据到新的CSV文件中
output_file_path = 'clean2.csv'
data.to_csv(output_file_path, index=False)

print("已删除包含缺失值的行，并保存到", output_file_path)
