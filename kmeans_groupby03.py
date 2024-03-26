import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score
import matplotlib.pyplot as plt
import warnings
#分组后存分类数据到output.csv里

warnings.filterwarnings("ignore", category=FutureWarning)
def preprocess_data(data):
    label_encoders = {}
    # 字符串转成数值
    categorical_cols = ['大类编码', '中类编码', '小类编码', '商品类型', '是否促销']
    for col in categorical_cols:
        label_encoders[col] = LabelEncoder()
        data[col] = label_encoders[col].fit_transform(data[col])
    #数值型变量列将被缩放，以确保它们具有相似的尺度，标准化。
    numerical_cols = ['销售日期', '销售数量', '销售金额', '商品单价']
    scaler = StandardScaler()
    data[numerical_cols] = scaler.fit_transform(data[numerical_cols])
    return data

def cluster_analysis(data, min_clusters=2, max_clusters=10):
    features = ['销售日期', '销售数量', '销售金额', '商品单价', '大类编码', '中类编码', '小类编码', '商品类型', '是否促销']
    X = data[features]
    silhouette_scores = []
    calinski_harabasz_scores = []
    inertia_values = []
    for n_clusters in range(min_clusters, max_clusters + 1):
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(X)
        silhouette_avg = silhouette_score(X, cluster_labels)
        silhouette_scores.append(silhouette_avg)
        calinski_harabasz_avg = calinski_harabasz_score(X, cluster_labels)
        calinski_harabasz_scores.append(calinski_harabasz_avg)
        inertia_values.append(kmeans.inertia_)
    diff = np.diff(inertia_values, 2)
    k = diff.argmax() + 2
    best_cluster_index = k if k > silhouette_scores.index(max(silhouette_scores)) else silhouette_scores.index(max(silhouette_scores))
    return silhouette_scores, calinski_harabasz_scores, inertia_values, best_cluster_index,X

def plot_evaluation_scores(silhouette_scores, calinski_harabasz_scores, inertia_values, best_cluster_index, min_clusters=2, max_clusters=10):
    plt.figure(figsize=(12, 4))

    for i, (scores, title) in enumerate(zip([silhouette_scores, calinski_harabasz_scores, inertia_values],
                                             ['Silhouette Score', 'Calinski-Harabasz Score', 'inertia_values'])):
        plt.subplot(1, 3, i+1)
        plt.plot(range(min_clusters, max_clusters + 1), scores, marker='o')
        plt.axvline(x=best_cluster_index, color='r', linestyle='--')
        plt.xlabel('Number of Clusters')
        plt.ylabel(title)
        plt.title(title)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    data = pd.read_csv('clean2_new.csv')
    data = preprocess_data(data)
    silhouette_scores, calinski_harabasz_scores, inertia_values, best_cluster_index, X = cluster_analysis(data)
    print(f"根据轮廓系数，建议选择 {best_cluster_index + 2} 个聚类。")
    print(f"根据Calinski-Harabasz指数，建议选择 {calinski_harabasz_scores.index(max(calinski_harabasz_scores)) + 2} 个聚类。")
    plot_evaluation_scores(silhouette_scores, calinski_harabasz_scores, inertia_values, best_cluster_index)
    n_clusters = best_cluster_index + 2
    calinski = calinski_harabasz_scores.index(max(calinski_harabasz_scores)) + 2
    # 进行KMeans聚类
    # kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans2 = KMeans(n_clusters=calinski, random_state=42)
    # data['cluster轮廓系数'] = kmeans.fit_predict(X)
    data['clusterCalinski-Harabasz指数'] = kmeans2.fit_predict(X)
    # 将结果写入新的CSV文件
    data.to_csv('output.csv', index=False)
    print("结果存到output.csv中")
