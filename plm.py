import os
import sys
import pandas as pd
import inquirer

class Book:
    def __init__(self, title, author, publishing_year=0, rating=0.0):
        self.title = title
        self.author = author
        self.publishing_year = publishing_year
        self.rating = rating

    def __str__(self):
        return f"📖 {self.title} by {self.author} ({self.publishing_year}) - ⭐ {self.rating}/5"

    def add_book(self):
        print("\n➕ Add new Book\n")
        self.title = input("Title of the book: ")
        self.author = input("Author: ")

        try:
            self.publishing_year = int(input("Publishing Year: "))
            self.rating = float(input("Rating (out of 5): "))
        except ValueError:
            print("❌ Invalid input. Please enter numbers only.")
            return

        print("✅ Book added successfully")

        column_names = ["Title", "Author", "Publishing Year", "Rating"]
        data = [self.title, self.author, self.publishing_year, self.rating]
        df = pd.DataFrame([data], columns=column_names)

        store_book_list = inquirer.confirm("Do you want to store the book list?", default=True)
        if store_book_list:
            df.to_csv("book_list.csv", mode='a', header=not os.path.exists("book_list.csv"), index=False)
            print("📤 Book list stored successfully")
        
        return df

    def sort_book_list(self):
        print("\n🗂️ Sort your list\n")
        if not os.path.exists("book_list.csv"):
            print("⚠️ No book list found. Add some books first.")
            return

        sort_by = inquirer.list_input("Sort by:", choices=[
            "Title", "Author", "Publishing Year", "Rating"
        ])
        df = pd.read_csv("book_list.csv")
        sorted_df = df.sort_values(by=sort_by)
        print(f"📊 Sorted Book List by {sort_by}:\n", sorted_df)

    def load_book_list(self):
        if os.path.exists("book_list.csv"):
            df = pd.read_csv("book_list.csv")
            print("\n📥 Loaded Book List:\n", df)
        else:
            print("⚠️ No saved book list found. Please add a book first.")

    def main(self):
        while True:
            action = inquirer.list_input("What would you like to do?", choices=[
                "➕ Add new Book",
                "📥 Load your Book List",
                "🗂️ Sort your list",
                "🚪 Exit"
            ])

            if action == "➕ Add new Book":
                while True:
                    self.add_book()
                    add_more = inquirer.confirm("Do you want to add another book?", default=True)
                    if not add_more:
                        break

            elif action == "🗂️ Sort your list":
                self.sort_book_list()

            elif action == "📥 Load your Book List":
                self.load_book_list()
            
            elif action == "🚪 Exit":
                print("👋 Exiting the program. Goodbye!")
                sys.exit()

if __name__ == "__main__":
    Book("", "").main()