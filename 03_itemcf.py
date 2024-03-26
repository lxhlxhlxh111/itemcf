import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

def read_data(file_path):
    data = pd.read_csv(file_path)
    return data

def create_item_name_map(data):
    item_name_map = dict(zip(data['商品编码'], data['小类名称']))
    return item_name_map

def calculate_item_similarity(data):
    item_sales_matrix = data.pivot_table(index='商品编码', columns='顾客编号', values='销售金额', fill_value=0)
    item_sim_matrix = cosine_similarity(item_sales_matrix)
    return item_sales_matrix, item_sim_matrix

def generate_recommendations(data, item_sales_matrix, item_sim_matrix, item_name_map, user_id, num_rec=5):
    user_purchases = data[data['顾客编号'] == user_id]['商品编码'].unique()
    similar_items = defaultdict(float)

    for item in user_purchases:
        item_idx = item_sales_matrix.index.get_loc(item)
        similar_items.update({i: sim_score for i, sim_score in enumerate(item_sim_matrix[item_idx])})

    for item in user_purchases:
        del similar_items[item_sales_matrix.index.get_loc(item)]

    recommendations = sorted(similar_items.items(), key=lambda x: x[1], reverse=True)[:num_rec]
    rec_with_names = [(item_sales_matrix.index[item_idx], sim_score) for item_idx, sim_score in recommendations]
    rec_with_names = [(item_code, sim_score, item_name_map[item_code]) for item_code, sim_score in rec_with_names]

    return rec_with_names

def get_user_id():
    return int(input("请输入顾客编号: "))

def get_num_recommendations():
    return int(input("请输入要推荐的商品个数: "))

def print_recommendations(user_id, recommendations):
    print(f"用户 {user_id} 的推荐:")
    for item_code, sim_score, item_name in recommendations:
        print(f"商品编码: {item_code}, 商品名称: {item_name}, 相似度: {sim_score}")

def main():
    file_path = 'clean2_new.csv'
    data = read_data(file_path)
    item_name_map = create_item_name_map(data)
    item_sales_matrix, item_sim_matrix = calculate_item_similarity(data)

    user_id = get_user_id()
    num_recommendations = get_num_recommendations()
    recommendations = generate_recommendations(data, item_sales_matrix, item_sim_matrix, item_name_map, user_id, num_recommendations)
    print_recommendations(user_id, recommendations)

if __name__ == "__main__":
    main()
