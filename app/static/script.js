const API_URL = "https://adriano02.pythonanywhere.com/api/recipes";

// Fetch and display all recipes
async function fetchAllRecipes() {
  try {
    const response = await fetch(API_URL);
    const recipes = await response.json();
    displayRecipes(recipes);
  } catch (error) {
    console.error("Error fetching recipes:", error);
  }
}

// Display recipes in the grid
function displayRecipes(recipes) {
  const container = document.getElementById("recipes-container");
  container.innerHTML = ""; // Clear previous content

  recipes.forEach((recipe) => {
    const card = document.createElement("div");
    card.classList.add("card");

    // Replace \r\n with <br> for better readability
    const formattedInstructions = recipe.instructions.replace(/\\r\\n/g, "<br>");

    card.innerHTML = `
      <img src="https://adriano02.pythonanywhere.com/${recipe.image}" alt="${recipe.name}">
      <h3>${recipe.name}</h3>
      <p><span class="ingredients">Ingredients:</span> ${recipe.ingredients.join(", ")}</p>
      <p><span class="instructions">Instructions:</span> ${formattedInstructions}</p>
      <button class="delete-btn" onclick="deleteRecipe(${recipe.id})">Delete</button>
    `;
    container.appendChild(card);
  });
}

// Search recipes by ID
async function searchById() {
  const id = document.getElementById("search-id").value;
  if (!id) return alert("Please enter an ID to search.");

  try {
    const response = await fetch(`${API_URL}/search/${id}`);
    if (response.ok) {
      const recipe = await response.json();
      displayRecipes([recipe]); // Display single recipe
    } else {
      alert("Recipe not found");
    }
  } catch (error) {
    console.error("Error searching by ID:", error);
  }
}

// Search recipes by Name
async function searchByName() {
  const name = document.getElementById("search-name").value;
  if (!name) return alert("Please enter a name to search.");

  try {
    const response = await fetch(`${API_URL}/search/${name}`);
    if (response.ok) {
      const recipes = await response.json();
      displayRecipes(recipes);
    } else {
      alert("No recipes found");
    }
  } catch (error) {
    console.error("Error searching by name:", error);
  }
}

// Function to create a new recipe (POST) with image upload
async function createRecipe() {
  const formData = getFormDataWithFile();
  if (!formData) return;

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      body: formData,
    });
    if (response.ok) {
      alert("Recipe created successfully!");
      fetchAllRecipes(); // Refresh recipe list
    } else {
      alert("Failed to create recipe");
    }
  } catch (error) {
    console.error("Error creating recipe:", error);
  }
}

// Function to update a recipe entirely (PUT) with image upload
async function updateRecipe() {
  const id = document.getElementById("recipe-id").value;
  if (!id) return alert("Please provide an ID for updating");

  const formData = getFormDataWithFile();
  if (!formData) return;

  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: "PUT",
      body: formData,
    });
    if (response.ok) {
      alert("Recipe updated successfully!");
      fetchAllRecipes(); // Refresh recipe list
    } else {
      alert("Failed to update recipe");
    }
  } catch (error) {
    console.error("Error updating recipe:", error);
  }
}

// Function to partially update a recipe (PATCH) with image upload
async function patchRecipe() {
  const id = document.getElementById("recipe-id").value;
  if (!id) return alert("Please provide an ID for patching");

  const formData = getFormDataWithFile(true); // Allow partial data
  if (!formData) return alert("No data to update");

  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: "PATCH",
      body: formData,
    });
    if (response.ok) {
      alert("Recipe patched successfully!");
      fetchAllRecipes(); // Refresh recipe list
    } else {
      alert("Failed to patch recipe");
    }
  } catch (error) {
    console.error("Error patching recipe:", error);
  }
}

// Utility function to get data from form with file support
function getFormDataWithFile(allowPartial = false) {
  const formData = new FormData();
  const id = document.getElementById("recipe-id").value.trim();
  const name = document.getElementById("recipe-name").value.trim();
  const imageFile = document.getElementById("recipe-image").files[0];
  const ingredients = document.getElementById("recipe-ingredients").value.trim();
  const instructions = document.getElementById("recipe-instructions").value.trim();
  const location = document.getElementById("recipe-location").value.trim();

  if (id) formData.append("id", id);
  if (name || !allowPartial) formData.append("name", name);
  if (imageFile || !allowPartial) formData.append("image", imageFile); // Append file
  if (ingredients || !allowPartial)
    formData.append(
      "ingredients",
      ingredients
        .split(",")
        .map((i) => i.trim())
        .join(",")
    );
  if (instructions || !allowPartial) formData.append("instructions", instructions);
  if (location || !allowPartial) formData.append("location", location);

  if (formData.has("name") || formData.has("image") || formData.has("ingredients") || formData.has("instructions") || formData.has("location")) {
    return formData;
  } else {
    alert("No data provided");
    return null;
  }
}

// Delete a recipe by ID
async function deleteRecipe(id) {
  if (!confirm("Are you sure you want to delete this recipe?")) return;

  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: "DELETE",
    });
    if (response.ok) {
      alert("Recipe deleted successfully!");
      fetchAllRecipes(); // Refresh recipe list
    } else {
      alert("Failed to delete recipe");
    }
  } catch (error) {
    console.error("Error deleting recipe:", error);
  }
}

// Fetch all recipes on page load
fetchAllRecipes();
