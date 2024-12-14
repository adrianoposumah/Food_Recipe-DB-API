const apiUrl = "https://adriano02.pythonanywhere.com/api/recipes";
const recipeContainer = document.getElementById("recipe-container");

async function fetchRecipes() {
  try {
    const response = await fetch(apiUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
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
      <h3>${recipe.name}</h3>
      <p><strong>Location:</strong> ${recipe.location}</p>
      <p><strong>Ingredients:</strong></p>
      <ul>${ingredients}</ul>
      <p><strong>Instructions:</strong></p>
      <p>${instructions}</p>
    `;
    recipeContainer.appendChild(card);
  });
}

document.addEventListener("DOMContentLoaded", fetchRecipes);
