from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

# กำหนด URI ของ MongoDB
mongo_uri = "mongodb+srv://domdypol:Dompol19@cluster0.hxrw0cv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# เชื่อมต่อ MongoDB
client = MongoClient(mongo_uri)
db = client["myStudent"]
collection = db["product"]

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/products/", methods=["GET"])
def get_all_products():
    products_list = []
    products = collection.find()
    for product in products:
        products_list.append({
            "id":product["id"],
            "name": product["name"],
            "price": product["price"]
        })
    return jsonify(products_list)

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    product = collection.find_one({"id": product_id}, {"_id": 0})
    if product:
        return jsonify(product)
    else:
        return jsonify({"error": "Product not found"}), 404

@app.route("/products/", methods=["POST"])
def add_product():
    data = request.json
    product_id = collection.insert_one(data).inserted_id
    return jsonify({"id":product_id})

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    result = collection.delete_one({"id": product_id})
    if result.deleted_count == 1:
        return jsonify({"message": "Product deleted successfully"})
    else:
        return jsonify({"error": "Product not found"}), 404

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    update_data = {"$set": data}
    result = collection.update_one({"id": product_id}, update_data)
    if result.modified_count == 1:
        return jsonify({"message": "Product updated successfully"})
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)