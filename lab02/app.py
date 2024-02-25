from flask import Flask, jsonify, request, send_file
import os

app = Flask(__name__)

ICONS_FOLDER = os.path.join(os.getcwd(), 'icons')
app.config['ICONS_FOLDER'] = ICONS_FOLDER

products = []
ids = []


def add_product_to_data(product):
    products.append(product)
    ids.append(product['id'])

def get_free_id()-> int:
    i = 0
    while i in ids:
        i += 1
    return i

add_product_to_data( {"id": 1, "name": "Product 1", "description": "Description for product 1", "ico_name" : "ico1.png"})
add_product_to_data( {"id": 2, "name": "Product 2", "description": "Description for product 2", "ico_name" : "ico2.png"})


# добавить новый продукт
@app.route('/product', methods=['POST'])
def create_product():
    request_data = request.get_json()
    if 'name' not in request_data or 'description' not in request_data:
        return jsonify({'error': 'request must be: "name" : "...",  "description" : "..." '})
    product = {
        'id': get_free_id(),
        'name': request_data['name'],
        'description': request_data['description']
    }
    add_product_to_data(product)
    return jsonify(product)

def get_product_n_from_data(product_id : int) -> int:
    for i, product in enumerate(products):
        if product['id'] == product_id:
            return i
    return -1

# получить продукт по id
@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    n = get_product_n_from_data(product_id)
    if n == -1:
        return jsonify({'error' : 'no product id'}), 400
    return jsonify(products[n]), 200

# обновить продукт по id
@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    n = get_product_n_from_data(product_id)
    if n == -1:
        return jsonify({'error' : 'no product id'}), 400
        
    if "name" in request.json:
        products[n]['name'] = request.json['name']
    if "description" in request.json:
        products[n]['description'] = request.json['description']
    return jsonify(products[n]), 200


# DELETE /product/{product_id}
@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    n = get_product_n_from_data(product_id)
    if n == -1:
        return jsonify({'error' : 'no product id'}), 400
    product = products[n]
    products.pop(n)
    return jsonify(product), 200

@app.route('/products', methods=['GET'])
def get_products_list():
    return jsonify(products)

@app.route('/product/<int:product_id>/image', methods=['GET'])
def get_product_icon(product_id):
    n = get_product_n_from_data(product_id)
    if n == -1:
        return jsonify({'error' : 'no product id'}), 400

    product = products[n]
    image_path = os.path.join(ICONS_FOLDER, product['ico_name'])
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png'), 200
    else:
        return jsonify({'error' : 'no product ico'}), 200
    

@app.route('/product/<int:product_id>/image', methods=['POST'])
def post_product_icon(product_id):
    n = get_product_n_from_data(product_id)
    if n == -1:
        return jsonify({'error' : 'no product id'}), 400

    if 'icon' not in request.files:
        return jsonify({'error': 'file is missing'}), 400
    icon_file = request.files['icon']

    product = products[n]

    if icon_file.filename == '':
        return jsonify({'error': 'no selected icon file.'}), 400
    
    icon_path = os.path.join(app.config['ICONS_FOLDER'], icon_file.filename)
    icon_file.save(icon_path)
    product['ico_name'] = icon_file.filename
    return jsonify(product), 200

if __name__ == '__main__':
    app.run(debug=True)