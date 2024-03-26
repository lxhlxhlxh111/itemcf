import pandas as pd

# 读取input2.csv和clean2.csv文件
input2_df = pd.read_csv('output.csv')
clean2_df = pd.read_csv('clean2.csv')

# 从output.csv中提取“cluster轮廓系数”列
cluster_silhouette_series = input2_df['clusterCalinski-Harabasz指数']

# 将提取的“cluster轮廓系数”列添加到clean2_df的最后一列
clean2_df['cluster轮廓系数'] = cluster_silhouette_series
clean2_df['clusterCalinski-Harabasz指数'] = cluster_silhouette_series

# 保存合并后的clean2_new.csv文件
clean2_df.to_csv('clean2_new.csv', index=False)
