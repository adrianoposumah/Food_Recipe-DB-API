# Food Recipe API Documentation

## Base URL

```
https://adriano02.pythonanywhere.com/api/recipes
```

---

## Endpoints

### GET

#### 1. **Get All Recipes**

```
GET /api/recipes
```

**Description**: Retrieve a list of all available recipes.

#### 2. **Search Recipes by Name**

```
GET /api/recipes/search/<string:keyword>
```

**Description**: Retrieve recipes that match the specified keyword in their name.

**Parameters**:

- `<string:keyword>`: A string representing the recipe name or part of it.

#### 3. **Search Recipe by ID**

```
GET /api/recipes/search/<int:id>
```

**Description**: Retrieve a specific recipe by its unique ID.

**Parameters**:

- `<int:id>`: An integer representing the recipe ID.

---

### POST

#### **Add a New Recipe**

```
POST /api/recipes
```

**Description**: Create a new recipe.

**Request Body** (JSON):

```json
{
  "name": "Nasi Goreng",
  "ingredients": "Daging sapi cincang, Roti burger, Keju cheddar, Bawang bombay, Selada, Tomat, Saus tomat, Mayones, Mustard, Garam, Merica, Minyak goreng",
  "instructions": "Buat Patty. Campur daging sapi cincang dengan garam dan merica. Bentuk adonan daging menjadi patty bulat pipih.\r\nPanggang Patty. Panaskan sedikit minyak goreng di wajan datar. Panggang patty hingga matang kecoklatan di kedua sisi.\r\nPanggang Roti. Panggang roti burger di wajan atau oven hingga sedikit kecoklatan.\r\nTata Burger. Olesi bagian bawah roti burger dengan saus tomat dan mustard. Letakkan patty di atasnya, lalu tambahkan keju cheddar, bawang bombay, selada, dan tomat.\r\nTutup Burger. Olesi bagian atas roti burger dengan mayones, lalu tutup burger.\r\nSajikan. Cheese burger siap disajikan.",
  "location": "Amerika",
  "image": "file.jpg/png/jpeg"
}
```

**Headers**:

- `Content-Type: multipart/form-data`

---

### PUT

#### **Update an Entire Recipe**

```
PUT /api/recipes/<int:id>
```

**Description**: Update all details of a specific recipe by its ID.

**Parameters**:

- `<int:id>`: The ID of the recipe to be updated.

**Request Body**: Same as POST.

---

### PATCH

#### **Partially Update a Recipe**

```
PATCH /api/recipes/<int:id>
```

**Description**: Partially update specific fields of a recipe by its ID.

**Parameters**:

- `<int:id>`: The ID of the recipe to be updated.

**Request Body**: Same as POST.

---

### DELETE

#### **Delete a Recipe**

```
DELETE /api/recipes/<int:id>
```

**Description**: Remove a specific recipe by its ID.

**Parameters**:

- `<int:id>`: The ID of the recipe to be deleted.

---

## Example Usage

### **Retrieve All Recipes**

Request:

```
GET https://adriano02.pythonanywhere.com/api/recipes
```

Response:

```json
[
  {
    "id": 1,
    "name": "Cheese Burger",
    "location": "Amerika",
    "ingredients": "Daging sapi cincang, Roti burger, Keju cheddar, ...",
    "instructions": "Buat Patty. Campur daging sapi cincang ...",
    "image": "cheeseburger.jpg"
  }
]
```

### **Add a New Recipe**

Request:

```
POST https://adriano02.pythonanywhere.com/api/recipes
```

Headers:

```
Content-Type: multipart/form-data
```

Body:

```
name=Nasi Goreng
ingredients=Daging sapi cincang, Roti burger, Keju cheddar, ...
instructions=Buat Patty. Campur daging sapi cincang ...
location=Amerika
image=file.jpg
```

Response:

```json
{
  "message": "Recipe created successfully!",
  "recipe_id": 2
}
```
