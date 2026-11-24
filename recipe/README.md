# Recipes and Ingredients

A small kitchen data model. Ingredient amounts carry real units (grams, millilitres, pounds), and the checker knows which are masses and which are volumes.

## What's inside

- **`DietaryTag`**: a fixed list of values: `Vegan`, `Vegetarian`, `GlutenFree`, `DairyFree`.
- **`Ingredient`**: a named ingredient, with optional `caloriesPerGram`.
- **`RecipeIngredient`**: one recipe line. It links an `Ingredient` to a `massAmount` or a `volumeAmount`.
- **`Recipe`**: a dish with `servings`, optional `ovenTemperature`, one or more `ingredients`, and `dietaryTags`.
- **Facts**: ingredients `flour`, `milk`, `egg`, and recipes `pancakeBatter` and `bananaBread`.
- **`flag_large_batch`**: a rule that marks recipes as `LargeBatchRecipe` when `servings >= 8`.

## Try it

- Read `pancakeBatter` in `recipe.dlf`. It mixes `quantity(250 g)` and `quantity(300 mL)`.
- Look at `bananaBread`. It has 10 servings, so `flag_large_batch` should tag it as a `LargeBatchRecipe`. `pancakeBatter` has 4, so it is not tagged.
- Try putting `quantity(500 mL)` into `massAmount`. The comments in `recipe.dlf` say this is a dimension-mismatch error at compile time.

## Learn more

- `quantity(...)` literals with unit checking (`mass`, `volume`, `temperature`).
- `one of:` enumerations and `optional` / `some` properties.
