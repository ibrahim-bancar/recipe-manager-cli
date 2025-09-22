import json
import os
import time
import unicodedata

RECIPES_FILE = "recipes.json"

class RecipeManager:
    def __init__(self):
        self.recipes = []
        self.load_recipes()
    def save_recipes(self):
        try:
            with open(RECIPES_FILE, 'w', encoding="utf-8") as file:
                json.dump(self.recipes, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"There is an error that occurred while saving recipes: {e}")

    def load_recipes(self):
        if os.path.exists(RECIPES_FILE):
            try:
                with open(RECIPES_FILE, 'r', encoding="utf-8") as file:
                    self.recipes = json.load(file)
                # İçerik liste değilse sıfırla
                if not isinstance(self.recipes, list):
                    self.recipes = []
            except json.JSONDecodeError as e:
                print(f"recipes.json is corrupted (JSON error). Starting with an empty list. Details: {e}")
                self.recipes = []
                self.save_recipes()
            except Exception as e:
                print(f"There is an error that occurred while loading recipes: {e}")
                self.recipes = []
        else:
            print(" " * 35 + "WELCOME TO DELICIOUS RECIPES")
            print(" " * 35 + "*---------------------------*")
            time.sleep(1)
            print(" " * 35 + "File is creating. Please wait")
            for i in range(50):
                print("**", end="")
                time.sleep(0.1)
            print()
            self.recipes = []
            self.save_recipes()
            print("File created successfully")

    def add_recipe(self):
        print("\nTo add a recipe, follow these steps:")
        name = input("Enter the recipe name: ").strip()
        if not name:
            print("Recipe name cannot be empty.")
            return
        n = self._norm(name)
        if any(self._norm(r.get("name", "")) == n for r in self.recipes):
            print(f"Recipe '{name}' already exists.")
            return
        raw = input("Enter ingredients separated by commas: ").split(",")
        ingredients = [x.strip() for x in raw if x.strip()]
        if not ingredients:
            print("You must enter at least one ingredient.")
            return
        print("Enter instructions row by row and write 'exit' to finish:\n")
        list_instructions = []
        i = 1
        while True:
            instructions = input(str(i) + " :").strip()
            if instructions.lower() == "exit":
                break
            if instructions:
                list_instructions.append(instructions)
                i += 1
        self.recipes.append({'name': name, 'ingredients': ingredients, 'instructions': list_instructions})
        self.save_recipes()
        print(f"\nRecipe '{name}' added successfully with {len(list_instructions)} instructions and {len(ingredients)} ingredients.")

    def delete_recipe(self):
        print("\nTo delete a recipe, enter the name of the recipe.")
        print("\nEnter 'cancel' to return to the main menu.")
        name = input("Enter recipe name to delete: ").strip()
        if not name:
            print("Recipe name cannot be empty.")
            return
        if name.lower() == 'cancel':
            print("Successfully cancelled.")
            return

        target = self._norm(name)
        for i, r in enumerate(self.recipes):
            if self._norm(r.get('name', '')) == target:
                removed = self.recipes.pop(i)
                self.save_recipes()
                print(f"Recipe '{removed['name']}' deleted successfully")
                return
        print(f"Recipe '{name}' does not exist")

    def display_all_recipes(self):
        if not self.recipes:
            print("No recipes added yet.")
            return

        print(f"\nListing {len(self.recipes)} recipe(s):")
        for idx, r in enumerate(self.recipes, start=1):
            name = r.get('name', '(no name)')
            ingredients = r.get('ingredients', [])
            instructions = r.get('instructions', [])

            print("\n" + "=" * 40)
            print(f"{idx}. {name}")
            print("- Ingredients:")
            for ing in ingredients:
                print("  - " + str(ing))

            print("- Instructions:")
            for i, step in enumerate(instructions, start=1):
                print(f"  {i}. {step}")
        print("=" * 40)

    def display_recipe(self, recipe_name=None):
        if recipe_name is None:
            recipe_name = input("\nEnter recipe name to display: ").strip()
        if not recipe_name:
            print("Recipe name cannot be empty.")
            return

        target = self._norm(recipe_name)
        for r in self.recipes:
            if self._norm(r.get('name', '')) == target:
                name = r.get('name', '(no name)')
                ingredients = r.get('ingredients', [])
                instructions = r.get('instructions', [])

                print("\n" + "=" * 40)
                print(name)
                print("- Ingredients:")
                for ing in ingredients:
                    print("  - " + str(ing))
                print("- Instructions:")
                for i, step in enumerate(instructions, start=1):
                    print(f"  {i}. {step}")
                print("=" * 40)
                return

        print(f"Recipe '{recipe_name}' can not be found. Returning to main menu")

    def edit_recipe(self):
        if not self.recipes:
            print("No recipes added yet.")
            return

        print("\nTo edit a recipe, enter the name of the recipe.")
        recipe_name = input("Enter recipe name to edit: ").strip()
        if not recipe_name:
            print("Recipe name cannot be empty.")
            return

        target = self._norm(recipe_name)
        idx = None
        for i, r in enumerate(self.recipes):
            if self._norm(r.get('name', '')) == target:
                idx = i
                break

        if idx is None:
            print(f"Recipe '{recipe_name}' does not exist. Returning to main menu")
            return

        recipe = self.recipes[idx]
        print(f"\nEditing Recipe: {recipe.get('name', '(no name)')}")

        new_name = input(f"New recipe name ({recipe.get('name', '')}): ").strip()
        if not new_name:
            new_name = recipe.get('name', '')
        else:
            new_norm = self._norm(new_name)
            for j, other in enumerate(self.recipes):
                if j != idx and self._norm(other.get('name', '')) == new_norm:
                    print(f"Another recipe already uses the name '{new_name}'. Keeping the old name.")
                    new_name = recipe.get('name', '')
                    break

        # Ingredients
        raw_ing = input(
            f"New ingredients (comma-separated) or press Enter to keep "
            f"({', '.join(recipe.get('ingredients', []))}): "
        )
        if raw_ing.strip():
            new_ingredients = [x.strip() for x in raw_ing.split(",") if x.strip()]
        else:
            new_ingredients = recipe.get('ingredients', [])

        # Instructions
        print("Enter new instructions (write 'exit' to finish). Press Enter immediately to keep existing.")
        new_instructions = []
        j = 1
        while True:
            line = input(f"{j}. new instruction for {new_name}: ").strip()
            if not line:
                if j == 1:
                    new_instructions = recipe.get('instructions', [])
                break
            if line.lower() == "exit":
                if not new_instructions:
                    new_instructions = recipe.get('instructions', [])
                break
            new_instructions.append(line)
            j += 1

        self.recipes[idx] = {
            'name': new_name,
            'ingredients': new_ingredients,
            'instructions': new_instructions
        }
        self.save_recipes()
        print(f"Recipe '{recipe_name}' edited successfully")

    def search_recipe_by_keyword(self):
        if not self.recipes:
            print("No recipes added yet.")
            return

        keyword = self._norm(input("\nEnter a keyword to search in name/ingredients/instructions: "))
        if not keyword:
            print("Keyword cannot be empty.")
            return

        found_recipes = []
        for r in self.recipes:
            haystack = " ".join([
                r.get('name', ''),
                " ".join(r.get('ingredients', [])),
                " ".join(r.get('instructions', [])),
            ])
            if keyword in self._norm(haystack):
                found_recipes.append(r)

        if found_recipes:
            print(f"\nFound {len(found_recipes)} recipe(s) containing '{keyword}':")
            for recipe in found_recipes:
                print("\n" + "=" * 40)
                print(recipe.get('name', '(no name)'))
                print("- Ingredients:")
                for ing in recipe.get('ingredients', []):
                    print("  - " + str(ing))
                print("- Instructions:")
                for i, step in enumerate(recipe.get('instructions', []), start=1):
                    print(f"  {i}. {step}")
            print("=" * 40)
        else:
            print(f"No recipes found containing the keyword '{keyword}'")

    def display_user_manual(self):
        print("\nUser Manual for Recipe Manager:")
        print("Select '1' to add a new recipe")
        print("Select '2' to display recipes")
        print("Select '3' to edit a recipe")
        print("Select '4' to search for a keyword in recipes")
        print("Select '5' to delete a recipe")
        print("Select '6' to exit the program")

    def display_quick_help(self):
        print("\n[1] Add  |  [2] Show  |  [3] Edit  |  [4] Search  |  [5] Delete  |  [6] Exit")

    @staticmethod
    def _norm(s):
        if not isinstance(s, str):
            s = str(s)
        s = s.strip()
        s = s.replace("İ", "i").replace("I", "i").replace("ı", "i")
        # Case-insensitive
        s = s.casefold()
        # Remove accents/diacritics (e.g., ğ, â, é -> g, a, e)
        s = ''.join(ch for ch in unicodedata.normalize('NFKD', s)
                    if not unicodedata.combining(ch))
        return s
