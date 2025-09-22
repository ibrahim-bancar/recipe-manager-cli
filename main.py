from recipe import RecipeManager

def main():
    manager = RecipeManager()
    manager.display_user_manual()
    flag = True
    try:
        while True:
            if not flag:
                manager.display_quick_help()
            flag = False
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                manager.add_recipe()

            elif choice == "2":
                if not manager.recipes:
                    print("No recipes added yet.")
                else:
                    ans = input(f"Do you want to display all {len(manager.recipes)} recipes? (yes/no): ").strip().lower()
                    if ans == "yes":
                        manager.display_all_recipes()
                    elif ans == "no":
                        manager.display_recipe()
                    else:
                        print("Invalid choice. Returning to main menu.")

            elif choice == "3":
                manager.edit_recipe()

            elif choice == "4":
                manager.search_recipe_by_keyword()

            elif choice == "5":
                if not manager.recipes:
                    print("No recipes added yet.")
                else:
                    ans = input("Do you want to delete all recipes? (yes/no): ").strip().lower()
                    if ans == "yes":
                        manager.recipes.clear()
                        manager.save_recipes()
                        print("All recipes deleted successfully.")
                    elif ans == "no":
                        manager.delete_recipe()
                    else:
                        print("Invalid choice. Returning to main menu.")

            elif choice == "6":
                confirm = input("Are you sure you want to exit? (yes/no): ").strip().lower()
                if confirm == "yes":
                    print("Thank you for using us, Come Again! ")
                    break
                elif confirm=="no":
                    continue
                else:
                    print("Invalid choice. Returning to main menu.")

            else:
                print("Invalid choice. Returning to main menu.")
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting. Goodbye!")

if __name__ == "__main__":
    main()
