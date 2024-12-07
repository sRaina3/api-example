from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps
from bson import ObjectId  # Import ObjectId to handle the conversion

# Initialize the Flask application
app = Flask(__name__)

# Set up MongoDB client
client = MongoClient('mongodb+srv://saranshraina1:convergent@api-example.sxo9x.mongodb.net/?retryWrites=true&w=majority&appName=api-example')  # Change this to your MongoDB URI
db = client['mydatabase']  # Database name
collection = db['fruits']  # Collection name

# Sample route to get all documents in the collection
@app.route('/api/fruits', methods=['GET'])
def get_fruits():
    fruits = collection.find()
    return dumps(fruits)  # Convert MongoDB data to JSON format

# Sample route to add a new document to the collection
@app.route('/api/fruits', methods=['POST'])
def add_fruit():
    data = request.get_json()  # Get the JSON data sent in the request
    result = collection.insert_one(data)
    return jsonify({"message": "Fruit added", "id": str(result.inserted_id)})

# Sample route to get a fruit by ID
@app.route('/api/fruits/<fruit_id>', methods=['GET'])
def get_fruit(fruit_id):
    try:
        # Convert the string ID to an ObjectId
        fruit = collection.find_one({"_id": ObjectId(fruit_id)})
        if fruit:
            return dumps(fruit)  # Return the fruit document as JSON
        else:
            return jsonify({"message": "Fruit not found"}), 404
    except Exception as e:
        return jsonify({"message": "Invalid ObjectId", "error": str(e)}), 400

# Root route to show all fruits
@app.route('/', methods=['GET'])
def show_all_fruits():
    fruits = collection.find()
    return dumps(fruits)  # Convert MongoDB data to JSON format

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
