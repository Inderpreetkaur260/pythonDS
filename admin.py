dict=[ { "name": "Forrest Gump", "year": 1994, "duration": 142, "genres": ["Drama", "Romance"] },
{ "name": "Avengers: Endgame", "year": 2019, "duration": 181, "genres": ["Action",
"Adventure", "Drama"] }, { "name": "Back to the Future", "year": 1985, "duration": 114,
"genres": ["Adventure", "Comedy", "Sci-Fi"] } ]

print("----WELCOME----")

def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def input_something(prompt):
    while True:
        s = input(prompt)
        if s:
            return s
        else:
            print("Please enter something.")

def add():
    name = input_something("Enter movie name: ")
    year = input_int("Enter release year: ")
    duration = input_int("Enter duration in minutes: ")
    genres = input_something("Enter genres (comma-separated): ")
    genres = [genre for genre in genres]
    
    n_movie = {
        "name": name,
        "year": year,
        "duration": duration,
        "genres": genres
    }
    dict.append(n_movie)
    print("Appended",name)

def list():
    if not dict:
        print("No movies available.")
        return
    
    for i, movie in enumerate(dict, start=1):
        print(i, ")", movie["name"]+ str(movie["year"])+ str(movie["duration"])+ str(movie["genres"]))

def search():
    if not dict:
        print("No movies saved.")
        return
    
    s_item=input_something("Enter the movie name to search: ")
    f_item= False
    for i,movie in enumerate(dict, 1):
        if s_item in movie["name"]:
            print(i,")",movie["name"]) 
            f_item = True

        if not f_item:
                print("No movie found with that name.")
                return

def view():
    if not dict:
        print("No movies saved.")
        return
    idx=input_int("Enter index of the movie to view the details: ")
    if idx<1 or idx>len(dict):
        print("Invalid index.")
        return
    else:
        movie=dict[idx-1]
        print("Movie Name: ", movie["name"])
        print("Release Year: ", movie["year"])
        print("Duration: ", movie["duration"])
        print("Genres: ", movie["genres"])
        return

def delete():
    if not dict:
        print("No movies saved.")
        return
    idx = input_int("Enter index of the movie to delete: ")
    if idx<1 or idx>len(dict)-1:
        print("Invalid index.")
    elif not dict:
        print("No movies available.")
    else:
        del dict[idx-1]
        print("Movie deleted successfully.")
        return
    
def quit():
    print("Goodbye")

print("The list of the movies are as follows: ")
list()
while True:
    print("\na. Add a movie")
    print("l. List all movies")
    print("s. Search a movie")
    print("v. View a movie")
    print("d. Delete a movie")
    print("q. Quit")
    choice = input_something("Enter your choice: ")
    if choice == 'a':
        add()
    elif choice == 'l':
        list()
    elif choice == 's':
        search()
    elif choice == 'v':
        view()
    elif choice == 'd':
        delete()
    elif choice == 'q':
        quit()
    

def search_movies(data):
    if not data:
        print("No movies saved.\n")
        return
    term = input_something("Enter search term: ").lower()
    found = False
    for i, movie in enumerate(data, 1):
        if term in movie['name'].lower():
            print(f"{i}) {movie['name']} ({movie['year']})")
            found = True
    if not found:
        print("No matching movies found.")
    print()