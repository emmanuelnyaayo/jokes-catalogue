"""
jokes.py
------------------------------------------------
This GUI program displays jokes loaded from 'data.txt' (in JSON format).
Users can click "Laugh" or "Groan" to rate each joke. The rating is saved,
and the next joke is displayed until all jokes have been rated.
"""

import tkinter
from tkinter import messagebox
import json
import random


class ProgramGUI:
    """GUI class responsible for displaying and managing the Joke Catalogue."""

    def __init__(self):
        """Constructor - sets up the main window, loads joke data, and initializes the interface."""
        # Create main window
        self.window = tkinter.Tk()
        self.window.title("Joke Catalogue")

        # Attempt to load data from JSON file
        # Addition and Enhancement 5: for random order
        try:
            with open("data.txt", "r") as file:
                self.data = json.load(file)
            if not isinstance(self.data, list) or not self.data:
                raise ValueError
            random.shuffle(self.data)  # Shuffle jokes once at start
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            messagebox.showerror("Error", "Missing/Invalid file.")
            self.window.destroy()
            return

        # Track current joke index
        self.current_joke = 0

        # Create GUI layout
        self.setup_label = tkinter.Label(self.window, text="", font=("Arial", 14, "bold"), wraplength=400, justify="center")
        self.setup_label.pack(pady=(20, 10))

        self.punchline_label = tkinter.Label(self.window, text="", font=("Arial", 12, "italic"), wraplength=400, justify="center")
        self.punchline_label.pack(pady=(0, 20))

        # Buttons frame
        button_frame = tkinter.Frame(self.window)
        button_frame.pack(pady=10)

        # Addition and Enhancement 1: Add "Abstain" button
        tkinter.Button(button_frame, text="Laugh 😂", width=12, command=lambda: self.rate_joke('laughs')).grid(row=0, column=0, padx=10)
        tkinter.Button(button_frame, text="Abstain 😐", width=12, command=self.abstain_joke).grid(row=0, column=1, padx=10)
        tkinter.Button(button_frame, text="Groan 🙄", width=12, command=lambda: self.rate_joke('groans')).grid(row=0, column=2, padx=10)

        # Addition and Enhancement 3: show current position (Joke X/Y)
        self.progress_label = tkinter.Label(self.window, text="", font=("Arial", 10))
        self.progress_label.pack(pady=(10, 5))

        # Display first joke
        self.show_joke()

        # Start GUI event loop
        self.window.mainloop()

    # ----------------------------------------------------------------
    # Method 1: show_joke()
    # ----------------------------------------------------------------
    def show_joke(self):
        """Displays the current joke (setup and punchline) in the GUI."""
        joke = self.data[self.current_joke]

        # Update setup
        self.setup_label.configure(text=joke["setup"])
        # Hide punchline initially
        self.punchline_label.configure(text="(Click to reveal punchline)")

        # Addition and Enhancement 2: Show rating info
        laughs, groans = joke["laughs"], joke["groans"]
        if laughs == 0 and groans == 0:
            info_text = "New joke — no ratings yet."
        else:
            info_text = f"Laughs: {laughs}   Groans: {groans}"

        # Addition and Enhancement 3: show current position (Joke X/Y)
        self.progress_label.configure(
            text=f"Joke {self.current_joke + 1}/{len(self.data)}   |   {info_text}"
        )

        # Addition and Enhancement 4: Reveal punchline on click
        self.punchline_label.bind("<Button-1>", lambda e: self.reveal_punchline(joke["punchline"]))

    # ----------------------------------------------------------------
    # Addition and Enhancement 4: Reveal punchline on click
    # ----------------------------------------------------------------
    def reveal_punchline(self, text):
        """Displays the punchline when the user clicks on the placeholder."""
        self.punchline_label.configure(text=text)

    # ----------------------------------------------------------------
    # Method 2: rate_joke()
    # ----------------------------------------------------------------
    def rate_joke(self, rating):
        """
        Records the user's rating ('laughs' or 'groans') for the current joke.
        Updates the data file, then moves to the next joke or ends the program.
        """
        # Increment rating counter in the joke dictionary
        self.data[self.current_joke][rating] += 1

        # Save updated data back to file
        with open("data.txt", "w") as file:
            json.dump(self.data, file, indent=4)

        # Check if this was the last joke
        if self.current_joke == len(self.data) - 1:
            messagebox.showinfo("Rating Recorded", "That was the last joke. Thanks for rating!")
            self.window.destroy()
        else:
            # Addition and Enhancement: thank the user after each joke
            messagebox.showinfo(
                "Rating Recorded",
                "Thank you for rating!\nThe next joke will now appear."
            )

            # Move to next joke and refresh the display
            self.current_joke += 1
            self.show_joke()

    # ----------------------------------------------------------------
    # Addition and Enhancement 1: Abstain button functionality
    # ----------------------------------------------------------------
    def abstain_joke(self):
        """Skips to the next joke without rating."""
        if self.current_joke == len(self.data) - 1:
            messagebox.showinfo("End", "That was the last joke. No rating recorded.")
            self.window.destroy()
        else:
            messagebox.showinfo("Skipped", "You abstained from rating.\nThe next joke will now appear.")
            self.current_joke += 1
            self.show_joke()


# Create an object of the ProgramGUI class to begin the program.
if __name__ == "__main__":
    gui = ProgramGUI()
