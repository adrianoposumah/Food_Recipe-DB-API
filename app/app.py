from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
import json
from flasgger import Swagger

app = Flask(__name__)

template = {
    "swagger": "2.0",
    "info": {
        "title": "Food Recipe API",
        "description": "This API was developed using Python Flask",
        "version": "0.0.1",
    },
}

Swagger(app, template=template)

UPLOAD_FOLDER = "./app/static/images"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

JSON_FILE = "./app/static/data.json"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def read_json():
    if not os.path.exists(JSON_FILE):
        return []
    with open(JSON_FILE, "r") as file:
        return json.load(file)


def write_json(data):
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)


"""
info:
  title: API DOCS
  description: Testd
  version:"1.0.0"
"""

@app.route("/")
def index():
    """
    Serve the index.html page
    ---
    responses:
      200:
        description: Rendered homepage
    """
    return render_template("index.html")


@app.route("/api/recipes", methods=["GET"])
def get_recipes():
    """
    Get all recipes
    ---
    tags:
      - Recipes
    responses:
      200:
        description: A list of all recipes
        schema:
          type: array
          items:
            $ref: '#/definitions/Recipe'
    """
    recipes = read_json()
    return jsonify(recipes)


@app.route("/api/recipes/search/<int:id>", methods=["GET"])
def get_recipe(id):
    """
    Retrieve a specific recipe by its ID.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the recipe
    tags:
      - Recipes
    responses:
      200:
        description: A single recipe
        schema:
          id: Recipe
          properties:
            id:
              type: integer
              description: The recipe ID
            name:
              type: string
              description: The name of the recipe
            ingredients:
              type: array
              items:
                type: string
              description: List of ingredients
            instructions:
              type: string
              description: The cooking instructions
            location:
              type: string
              description: The recipe's origin
            image:
              type: string
              description: The file path to the recipe's image
      404:
        description: Recipe not found
    """
    recipes = read_json()
    recipe = next((r for r in recipes if r["id"] == id), None)
    if recipe:
        return jsonify(recipe)
    return jsonify({"message": "Resep tidak ditemukan"}), 404


@app.route("/api/recipes/search/<string:keyword>", methods=["GET"])
def search_recipes(keyword):
    """
    Search for recipes by keyword
    ---
    parameters:
      - name: keyword
        in: path
        type: string
        required: true
        description: The keyword to search in recipe names
    tags:
      - Recipes
    responses:
      200:
        description: Matching recipes
        schema:
          type: array
          items:
            $ref: '#/definitions/Recipe'
      404:
        description: No recipes found
    """
    try:
        recipes = read_json()
        matched_recipes = [
            r for r in recipes if keyword.lower().strip() in r["name"].lower().strip()
        ]
        if matched_recipes:
            return jsonify(matched_recipes), 200
        return jsonify({"message": "Resep tidak ditemukan"}), 404
    except Exception as e:
        return jsonify({"message": f"Terjadi kesalahan: {str(e)}"}), 500


@app.route("/api/recipes", methods=["POST"])
def add_recipe():
    """
    Add a new recipe
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        description: The name of the recipe
      - name: ingredients
        in: formData
        type: string
        required: true
        description: Comma-separated list of ingredients
      - name: instructions
        in: formData
        type: string
        required: true
        description: Recipe instructions
      - name: location
        in: formData
        type: string
        required: true
        description: The origin or location of the recipe
      - name: image
        in: formData
        type: file
        required: true
        description: An image of the recipe
    tags:
      - Recipes
    responses:
      201:
        description: Recipe created successfully
        schema:
          $ref: '#/definitions/Recipe'
      400:
        description: Bad Request
    """
    data = request.form
    file = request.files.get("image")
    recipes = read_json()

    if not all(
        [
            data.get("name"),
            data.get("ingredients"),
            data.get("instructions"),
            data.get("location"),
        ]
    ):
        return jsonify({"message": "Semua data harus diisi"}), 400

    if file:
        if not allowed_file(file.filename):
            return (
                jsonify(
                    {
                        "message": "Ekstensi file tidak diperbolehkan. Hanya file png, jpg, jpeg, gif yang diizinkan"
                    }
                ),
                400,
            )
        if file.content_length > app.config["MAX_CONTENT_LENGTH"]:
            return jsonify({"message": "Ukuran file terlalu besar. Maksimal 16MB"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        filepath = os.path.normpath(filepath)
    else:
        return jsonify({"message": "Gambar tidak valid atau tidak ada"}), 400

    new_recipe = {
        "id": len(recipes) + 1,
        "name": data.get("name"),
        "ingredients": data.get("ingredients").split(","),
        "instructions": data.get("instructions"),
        "location": data.get("location"),
        "image": filepath,
    }

    recipes.append(new_recipe)
    write_json(recipes)

    return jsonify(new_recipe), 201


@app.route("/api/recipes/<int:id>", methods=["PUT"])
def update_recipe(id):
    """
    Update a recipe completely
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the recipe to update
      - name: name
        in: formData
        type: string
        description: The new name of the recipe
      - name: ingredients
        in: formData
        type: string
        description: The new ingredients, comma-separated
      - name: instructions
        in: formData
        type: string
        description: The new instructions
      - name: location
        in: formData
        type: string
        description: The new location
      - name: image
        in: formData
        type: file
        description: The new image
    tags:
      - Recipes
    responses:
      200:
        description: Recipe updated successfully
        schema:
          $ref: '#/definitions/Recipe'
      404:
        description: Recipe not found
    """
    recipes = read_json()
    recipe = next((r for r in recipes if r["id"] == id), None)
    if not recipe:
        return jsonify({"message": "Resep tidak ditemukan"}), 404

    data = request.form
    file = request.files.get("image")

    if file:
        if file.content_length > app.config["MAX_CONTENT_LENGTH"]:
            return jsonify({"message": "Ukuran file terlalu besar. Maksimal 16MB"}), 400

        if not allowed_file(file.filename):
            return jsonify({"message": "Ekstensi file tidak diperbolehkan"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        filepath = os.path.normpath(filepath)
        recipe["image"] = filepath

    recipe["name"] = data.get("name", recipe["name"])
    recipe["ingredients"] = data.get(
        "ingredients", ",".join(recipe["ingredients"])
    ).split(",")
    recipe["instructions"] = data.get("instructions", recipe["instructions"])
    recipe["location"] = data.get("location", recipe["location"])

    write_json(recipes)
    return jsonify(recipe)


@app.route("/api/recipes/<int:id>", methods=["PATCH"])
def partial_update_recipe(id):
    """
    Partially update a recipe.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the recipe to update.
      - name: name
        in: formData
        type: string
        required: false
        description: The updated name of the recipe.
      - name: ingredients
        in: formData
        type: string
        required: false
        description: The updated ingredients of the recipe (comma-separated).
      - name: instructions
        in: formData
        type: string
        required: false
        description: The updated cooking instructions for the recipe.
      - name: location
        in: formData
        type: string
        required: false
        description: The updated location of the recipe.
      - name: image
        in: formData
        type: file
        required: false
        description: An updated image for the recipe.
    tags:
      - Recipes
    responses:
      200:
        description: Recipe successfully updated.
        schema:
          id: PartialRecipeUpdateResponse
          properties:
            id:
              type: integer
              description: The ID of the recipe.
            name:
              type: string
              description: The name of the recipe.
            ingredients:
              type: array
              items:
                type: string
              description: The list of ingredients.
            instructions:
              type: string
              description: Cooking instructions.
            location:
              type: string
              description: The location of the recipe.
            image:
              type: string
              description: The file path of the recipe's image.
      404:
        description: Recipe not found.
      400:
        description: Invalid input.
    """
    recipes = read_json()
    recipe = next((r for r in recipes if r["id"] == id), None)
    if not recipe:
        return jsonify({"message": "Resep tidak ditemukan"}), 404

    data = request.form
    file = request.files.get("image")

    if file:
        if file.content_length > app.config["MAX_CONTENT_LENGTH"]:
            return jsonify({"message": "Ukuran file terlalu besar. Maksimal 16MB"}), 400

        if not allowed_file(file.filename):
            return jsonify({"message": "Ekstensi file tidak diperbolehkan"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        filepath = os.path.normpath(filepath)
        recipe["image"] = filepath

    if "name" in data:
        recipe["name"] = data["name"]
    if "ingredients" in data:
        recipe["ingredients"] = data["ingredients"].split(",")
    if "instructions" in data:
        recipe["instructions"] = data["instructions"]
    if "location" in data:
        recipe["location"] = data["location"]

    write_json(recipes)
    return jsonify(recipe)


@app.route("/api/recipes/<int:id>", methods=["DELETE"])
def delete_recipe(id):
    """
    Delete a recipe.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the recipe to delete.
    tags:
      - Recipes
    responses:
      200:
        description: Recipe successfully deleted.
        schema:
          id: DeleteRecipeResponse
          properties:
            message:
              type: string
              description: Confirmation message.
      404:
        description: Recipe not found.
    """
    try:
        recipes = read_json()
        updated_recipes = [r for r in recipes if r["id"] != id]
        write_json(updated_recipes)

        if len(updated_recipes) == len(recipes):
            return jsonify({"message": "Resep tidak ditemukan"}), 404

        return jsonify({"message": "Resep berhasil dihapus"}), 200
    except Exception as e:
        return jsonify({"message": f"Terjadi kesalahan: {str(e)}"}), 500


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(JSON_FILE):
        write_json([])
    app.run(port=8000, debug=True)
