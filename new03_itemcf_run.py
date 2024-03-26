from flask import Flask, request
from flask_cors import CORS
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

app = Flask(__name__)
CORS(app, resources=r'*')


def read_data(file_path):
    data = pd.read_csv(file_path)
    return data


def create_item_name_map(data):
    item_name_map = dict(zip(data['goods_id'], data['小类名称']))
    return item_name_map

def calculate_item_similarity(data):
    item_sales_matrix = data.pivot_table(index='goods_id', columns='user_id', values='销售金额', fill_value=0)
    item_sim_matrix = cosine_similarity(item_sales_matrix)
    return item_sales_matrix, item_sim_matrix

def generate_recommendations(data, item_sales_matrix, item_sim_matrix, item_name_map, user_id, num_rec):
    user_purchases = data[data['user_id'] == user_id]['goods_id'].unique()
    print(user_purchases)
    similar_items = defaultdict(float)

    for item in user_purchases:
        item_idx = item_sales_matrix.index.get_loc(item)
        similar_items.update({i: sim_score for i, sim_score in enumerate(item_sim_matrix[item_idx])})

    for item in user_purchases:
        del similar_items[item_sales_matrix.index.get_loc(item)]

    recommendations = sorted(similar_items.items(), key=lambda x: x[1], reverse=True)[:num_rec]

    rec_with_names = [(item_sales_matrix.index[item_idx], sim_score, item_name_map[item_sales_matrix.index[item_idx]])
                      for item_idx, sim_score in recommendations]
    return rec_with_names


def get_recommendations(user_id, recommendations):
    output = f"用户 {user_id} 的推荐:\n"
    for item_code, sim_score, item_name in recommendations:
        output += f"商品编码: {item_code}, 商品名称: {item_name}, 相似度: {sim_score}\n"
    return output


@app.route('/', methods=['GET'])
def index():
    return "Welcome to the recommendation service!"



@app.route('/rec', methods=['POST'])
def get_rec():
    request_data = request.get_json()
    user_id = int(request_data.get('user_id'))
    num_recommendations = int(request_data.get('num_recommendations'))
    file_path = 'clean2_new.csv'
    data = read_data(file_path)
    item_name_map = create_item_name_map(data)
    item_sales_matrix, item_sim_matrix = calculate_item_similarity(data)

    recommendations = generate_recommendations(data, item_sales_matrix, item_sim_matrix, item_name_map, user_id,
                                               num_recommendations)
    output = get_recommendations(user_id, recommendations)


    return output




if __name__ == "__main__":
    app.run(port=5003, debug=True)
