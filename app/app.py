from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)

UPLOAD_FOLDER = './app/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

JSON_FILE = './app/static/data.json'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_json():
    if not os.path.exists(JSON_FILE):
        return []
    with open(JSON_FILE, 'r') as file:
        return json.load(file)

def write_json(data):
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = read_json()
    return jsonify(recipes)

@app.route('/api/recipes/search/<int:id>', methods=['GET'])
def get_recipe(id):
    recipes = read_json()
    recipe = next((r for r in recipes if r['id'] == id), None)
    if recipe:
        return jsonify(recipe)
    return jsonify({"message": "Resep tidak ditemukan"}), 404

@app.route('/api/recipes/search/<string:keyword>', methods=['GET'])
def search_recipes(keyword):
    try:
        recipes = read_json() 
        matched_recipes = [
            r for r in recipes if keyword.lower().strip() in r['name'].lower().strip()
        ]
        if matched_recipes:
            return jsonify(matched_recipes), 200
        return jsonify({"message": "Resep tidak ditemukan"}), 404
    except Exception as e:
        return jsonify({"message": f"Terjadi kesalahan: {str(e)}"}), 500



@app.route('/api/recipes', methods=['POST'])
def add_recipe():
    data = request.form
    file = request.files.get('image')
    recipes = read_json()

    if not all([data.get('name'), data.get('ingredients'), data.get('instructions'), data.get('location')]):
        return jsonify({"message": "Semua data harus diisi"}), 400

    if file:
        if not allowed_file(file.filename):
            return jsonify({"message": "Ekstensi file tidak diperbolehkan. Hanya file png, jpg, jpeg, gif yang diizinkan"}), 400
        if file.content_length > app.config['MAX_CONTENT_LENGTH']:
            return jsonify({"message": "Ukuran file terlalu besar. Maksimal 16MB"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        filepath = os.path.normpath(filepath)
    else:
        return jsonify({"message": "Gambar tidak valid atau tidak ada"}), 400

    new_recipe = {
        "id": len(recipes) + 1,
        "name": data.get('name'),
        "ingredients": data.get('ingredients').split(','),
        "instructions": data.get('instructions'),
        "location": data.get('location'),
        "image": filepath
    }

    recipes.append(new_recipe)
    write_json(recipes)
    
    return jsonify(new_recipe), 201


@app.route('/api/recipes/<int:id>', methods=['PUT'])
def update_recipe(id):
    recipes = read_json()
    recipe = next((r for r in recipes if r['id'] == id), None)
    if not recipe:
        return jsonify({"message": "Resep tidak ditemukan"}), 404

    data = request.form
    file = request.files.get('image')

    if file:
        if file.content_length > app.config['MAX_CONTENT_LENGTH']:
            return jsonify({"message": "Ukuran file terlalu besar. Maksimal 16MB"}), 400

        if not allowed_file(file.filename):
            return jsonify({"message": "Ekstensi file tidak diperbolehkan"}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        filepath = os.path.normpath(filepath)
        recipe['image'] = filepath

    recipe['name'] = data.get('name', recipe['name'])
    recipe['ingredients'] = data.get('ingredients', ','.join(recipe['ingredients'])).split(',')
    recipe['instructions'] = data.get('instructions', recipe['instructions'])
    recipe['location'] = data.get('location', recipe['location'])

    write_json(recipes)
    return jsonify(recipe)


@app.route('/api/recipes/<int:id>', methods=['PATCH'])
def partial_update_recipe(id):
    recipes = read_json()
    recipe = next((r for r in recipes if r['id'] == id), None)
    if not recipe:
        return jsonify({"message": "Resep tidak ditemukan"}), 404

    data = request.form
    file = request.files.get('image')

    if file:
        if file.content_length > app.config['MAX_CONTENT_LENGTH']:
            return jsonify({"message": "Ukuran file terlalu besar. Maksimal 16MB"}), 400

        if not allowed_file(file.filename):
            return jsonify({"message": "Ekstensi file tidak diperbolehkan"}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        filepath = os.path.normpath(filepath)
        recipe['image'] = filepath

    if 'name' in data:
        recipe['name'] = data['name']
    if 'ingredients' in data:
        recipe['ingredients'] = data['ingredients'].split(',')
    if 'instructions' in data:
        recipe['instructions'] = data['instructions']
    if 'location' in data:
        recipe['location'] = data['location']

    write_json(recipes)
    return jsonify(recipe)

@app.route('/api/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipes = read_json()
    recipes = [r for r in recipes if r['id'] != id]
    write_json(recipes)
    return jsonify({"message": "Resep berhasil dihapus"})

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(JSON_FILE):
        write_json([])
    app.run(debug=True)
