const apiUrl = "https://adriano02.pythonanywhere.com/api/recipes";
const recipeContainer = document.getElementById("recipe-container");

// Fetch and display recipes
async function fetchRecipes() {
  try {
    const response = await fetch(apiUrl);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const recipes = await response.json();
    displayRecipes(recipes);
  } catch (error) {
    recipeContainer.innerHTML = `<p>Error: ${error.message}</p>`;
  }
}

function displayRecipes(recipes) {
  if (recipes.length === 0) {
    recipeContainer.innerHTML = `<p>No recipes found.</p>`;
    return;
  }

  recipeContainer.innerHTML = ""; // Clear existing content

  recipes.forEach((recipe) => {
    const card = document.createElement("div");
    card.className = "recipe-card";

    const ingredients = recipe.ingredients.map((ing) => `<li>${ing}</li>`).join("");
    const instructions = recipe.instructions.replace(/\\r\\n/g, "<br>");

    card.innerHTML = `
      <img src="https://adriano02.pythonanywhere.com/${recipe.image}" alt="${recipe.name}">
      <div class="info">
        <h3>${recipe.name}</h3>
        <p><strong>Location:</strong> ${recipe.location}</p>
        <p><strong>Ingredients:</strong></p>
        <ul>${ingredients}</ul>
      </div>
      <div class="instructions">
        <p><strong>Instructions:</strong></p>
        <p>${instructions}</p>
        <button onclick="deleteRecipe(${recipe.id})">Delete</button>
        <button onclick="editRecipe(${recipe.id})">Edit</button>
      </div>
    `;
    recipeContainer.appendChild(card);
  });
}

// POST a new recipe
async function addRecipe(recipeData, imageFile) {
  const formData = new FormData();
  Object.keys(recipeData).forEach((key) => formData.append(key, recipeData[key]));
  if (imageFile) formData.append("image", imageFile);

  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      body: formData,
    });
    if (!response.ok) throw new Error("Failed to add recipe");
    const newRecipe = await response.json();
    console.log("Added:", newRecipe);
    fetchRecipes();
  } catch (error) {
    console.error(error.message);
  }
}

// PUT (update) a recipe
async function updateRecipe(id, recipeData, imageFile) {
  const formData = new FormData();
  Object.keys(recipeData).forEach((key) => formData.append(key, recipeData[key]));
  if (imageFile) formData.append("image", imageFile);

  try {
    const response = await fetch(`${apiUrl}/${id}`, {
      method: "PUT",
      body: formData,
    });
    if (!response.ok) throw new Error("Failed to update recipe");
    const updatedRecipe = await response.json();
    console.log("Updated:", updatedRecipe);
    fetchRecipes();
  } catch (error) {
    console.error(error.message);
  }
}

// PATCH (partial update) a recipe
async function partialUpdateRecipe(id, recipeData, imageFile) {
  const formData = new FormData();
  Object.keys(recipeData).forEach((key) => formData.append(key, recipeData[key]));
  if (imageFile) formData.append("image", imageFile);

  try {
    const response = await fetch(`${apiUrl}/${id}`, {
      method: "PATCH",
      body: formData,
    });
    if (!response.ok) throw new Error("Failed to partially update recipe");
    const updatedRecipe = await response.json();
    console.log("Partially Updated:", updatedRecipe);
    fetchRecipes();
  } catch (error) {
    console.error(error.message);
  }
}

// DELETE a recipe
async function deleteRecipe(id) {
  try {
    const response = await fetch(`${apiUrl}/${id}`, {
      method: "DELETE",
    });
    if (!response.ok) throw new Error("Failed to delete recipe");
    const result = await response.json();
    console.log(result.message);
    fetchRecipes();
  } catch (error) {
    console.error(error.message);
  }
}

// Initialize
document.addEventListener("DOMContentLoaded", fetchRecipes);
