"""
admin.py
-----------------------------------------------
This program allows the user to manage a collection of jokes stored in a JSON file.
Each joke has a setup, punchline, and laugh/groan counts.
Users can add, list, search, view, and delete jokes via a simple CLI interface.
"""

import json
from textwrap import shorten

# -------------------------------------------------------
# Helper Functions
# -------------------------------------------------------

def input_int(prompt):
    """
    Repeatedly prompts the user until they enter a valid integer >= 1.
    Returns the integer value.
    """
    while True:
        try:
            value = int(input(prompt))
            if value >= 1:
                return value
            else:
                print("Please enter a number of 1 or higher.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def input_something(prompt):
    """
    Repeatedly prompts the user until they enter non-whitespace text.
    Returns the string value.
    """
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("Input cannot be blank. Please try again.")


def save_data(data_list):
    """
    Saves the provided data list to 'data.txt' in JSON format.
    Overwrites the file each time it is called.
    """
    with open("data.txt", "w") as file:
        json.dump(data_list, file, indent=4)


# -------------------------------------------------------
# Program Initialization
# -------------------------------------------------------

# Load data from file, or initialize an empty list if file missing/corrupted.
try:
    with open("data.txt", "r") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError
except (FileNotFoundError, json.JSONDecodeError, ValueError):
    data = []

print("Welcome to the Joke Catalogue Admin Program.")

# -------------------------------------------------------
# Main Menu Loop
# -------------------------------------------------------
while True:
    print("\nChoose [a]dd, [l]ist, [s]earch, [v]iew, [d]elete, [t]op or [q]uit.")
    user_input = input("> ").strip()

    # ----------------------------------------------------------------------------
    # Addition and Enhancement 5: Split combined commands like "s hobbit" or "v 2"
    # ----------------------------------------------------------------------------
    parts = user_input.split(maxsplit=1)
    choice = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else None

    # ---------------------------------------------------
    # Add a new joke
    # ---------------------------------------------------
    if choice == 'a':
        setup = input_something("Enter setup of joke: ")
        punchline = input_something("Enter punchline of joke: ")

        joke = {
            "setup": setup,
            "punchline": punchline,
            "laughs": 0,
            "groans": 0
        }

        data.append(joke)
        save_data(data)
        print("Joke added.")

    # ---------------------------------------------------
    # List all jokes
    # ---------------------------------------------------
    elif choice == 'l':
        if not data:
            print("No jokes saved.")
        else:
            print("List of jokes:")
            # ------------------------------------------------------------------
            # Addition and Enhancement 2: Use shorten function to shorten setups
            # ------------------------------------------------------------------
            for i, joke in enumerate(data, start=1):
                short_setup = shorten(joke["setup"], width=50, placeholder="...")
                print(f"{i}) {short_setup}")

    # ---------------------------------------------------
    # Search jokes
    # ---------------------------------------------------
    elif choice == 's':
        if not data:
            print("No jokes saved.")
        else:
            term = arg.lower() if arg else input_something("Enter search term: ").lower()
            results_found = False
            print("Search results:")
            # ------------------------------------------------------------------
            # Addition and Enhancement 2: Use shorten function to shorten setups
            # ------------------------------------------------------------------
            for i, joke in enumerate(data, start=1):
                if term in joke["setup"].lower() or term in joke["punchline"].lower():
                    short_setup = shorten(joke["setup"], width=50, placeholder="...")
                    print(f"{i}) {short_setup}")
                    results_found = True
            # --------------------------------------------------
            # Addition and Enhancement 1: Show No results found
            # ---------------------------------------------------
            if not results_found:
                print("No results found.")

    # ---------------------------------------------------
    # View a specific joke
    # ---------------------------------------------------
    elif choice == 'v':
        if not data:
            print("No jokes saved.")
        else:
            index = int(arg) - 1 if arg and arg.isdigit() else input_int("Joke number to view: ") - 1
            if 0 <= index < len(data):
                joke = data[index]
                print(f"\n{joke['setup']}\n{joke['punchline']}")
                laughs, groans = joke['laughs'], joke['groans']

                if laughs == 0 and groans == 0:
                    print("This joke has not been rated.")
                else:
                    total = laughs + groans
                    laugh_pct = (laughs / total) * 100 if total else 0
                    groan_pct = (groans / total) * 100 if total else 0
                    print(f"Laughs: {laughs} ({laugh_pct:.1f}%), Groans: {groans} ({groan_pct:.1f}%)")

                    # --------------------------------------------------------------
                    # Addition and Enhancement 3: Extra commentary based on ratings
                    # --------------------------------------------------------------
                    if laughs >= 5 and groans == 0:
                        print("This joke is hilarious!")
                    elif groans >= 5 and laughs == 0:
                        print("This joke is groantastic!")
                    elif laughs >= 4 * groans and groans > 0:
                        print("This joke is hilarious!")
                    elif groans >= 4 * laughs and laughs > 0:
                        print("This joke is groantastic!")
            else:
                print("Invalid index number.")

    # ---------------------------------------------------
    # Delete a joke
    # ---------------------------------------------------
    elif choice == 'd':
        if not data:
            print("No jokes saved.")
        else:
            index = int(arg) - 1 if arg and arg.isdigit() else input_int("Joke number to delete: ") - 1
            if 0 <= index < len(data):
                del data[index]
                save_data(data)
                print("Joke deleted.")
            else:
                print("Invalid index number.")

    # ---------------------------------------------------
    # Addition and Enhancement 4: Display top-rated jokes
    # ---------------------------------------------------
    elif choice == 't':
        if not data:
            print("No jokes saved.")
        else:
            # Find jokes with max laughs and max groans
            top_laughs = max(data, key=lambda j: j["laughs"])
            top_groans = max(data, key=lambda j: j["groans"])

            print("\nTop Laughs Joke:")
            print(f"{top_laughs['setup']}")
            print(f"Punchline: {top_laughs['punchline']}")
            print(f"Laughs: {top_laughs['laughs']}, Groans: {top_laughs['groans']}")

            print("\nTop Groans Joke:")
            print(f"{top_groans['setup']}")
            print(f"Punchline: {top_groans['punchline']}")
            print(f"Laughs: {top_groans['laughs']}, Groans: {top_groans['groans']}")

    # ---------------------------------------------------
    # Quit program
    # ---------------------------------------------------
    elif choice == 'q':
        print("Goodbye!")
        break

    # ---------------------------------------------------
    # Invalid option
    # ---------------------------------------------------
    else:
        print("Invalid choice. Please try again.")
