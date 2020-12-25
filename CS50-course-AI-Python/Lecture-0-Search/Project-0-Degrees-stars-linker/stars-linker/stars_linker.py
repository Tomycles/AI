import csv
import sys

from nodes_and_frontier_class import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # For each row in te csv file, it creates a dictionary inside "people" dictionary with the actor's information.
        # i.e. every actor is a dictionary inside people dictionary whose key value is the actor's id.
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set() # This is just an empty set to be filled later on with the movies the actor played.
            }
            #  Check if the name is repeated... 
            # If it's not, stores it inside names dictionary and is linked to the id. 
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            # If it's repeated, add the new id to the repeated name dictionary
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set() 
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # The try line runs normally as long as the exception doesn't occur.
            # It links the actors with the movies inside people and movies dictionaries.
            # The exception runs only if the key value we are looking is not in the dictionary.
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    # This is just a cubersome way of defining the directory where the data is stored.
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large" # we could change to "small" here if we would want to deal with the smallest set of data, to practice for instance.

    # Load data from files into memory if it's not already loaded
    if people == {}:
        print("Loading data...")
        load_data(directory)
        print("Data loaded.")
    else:
        pass
    
    # Asks for the names of the initial and final persons.
    print("This program links two actors via the movies they starred. Choose their names!")
    Name1_incorrect= True
    while Name1_incorrect:
        source = person_id_for_name(input("Name of the first actor: "))
        if source is None:
            print("Sorry! That actor is not in my list, try another one!")
        else:
            Name1_incorrect = False
    Name2_incorrect= True        
    while Name2_incorrect:
        target = person_id_for_name(input("Name of the second actor: "))
        if target is None:
            print("Sorry! That actor is not in my list, try another one!")
        else:
            Name2_incorrect = False

    path = shortest_path(source, target)

    if path is None:
        print(str(people[source]["name"]) + " and " + str(people[target]["name"]) + " are not connected.")
    else:
        degrees = len(path)
        print(str(people[source]["name"]) + " and " + str(people[target]["name"]) + f" are separated by {degrees} movies.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    
    
    num_explored = 0
    
    # Sets the starting node. In this language, people's id is going to represent states. 
    start = Node(state=source,parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)  
    
    explored = set()
    
    # Keep looping until solution found
    while True:

        # If nothing left in frontier, then no path
        if frontier.empty():
            return None
            
        # Choose a node from the frontier
        node = frontier.remove()
        num_explored += 1

        # If node is our target, then we have a solution
        if node.state == target:
            actions = []
            states = []
            # Here we connect the target to the source starting with the former, moving backwards. 
            while node.parent is not None:
                actions.append(node.action)
                states.append(node.state)
                node = node.parent
            # When node.parent is indeed None, we reach the starting point, source, so we end the loop.
            # We reverse the path so to get the connecting path from start to end.
            actions.reverse()
            states.reverse()
            solution = [(actions[i],states[i]) for i in range(len(states)) ]
            return solution
        
        
        # Mark node as explored
        explored.add(node.state)
        
        # Add neighbors to frontier.
        # In this case, the "action" is given by the movie connecting people
        # while the state is, again, the people's id.
        for action, state in neighbors_for_person(node.state):
            # Here we check if the state is the target, if that's the case, we add it infront of the frontier to be the next node in being removed.
            if state == target:
                solution = Node(state=state, parent=node, action=action)
                frontier.add_inverse(solution)
                break
            # Here we assure not to end up in the same state again excluding the ones already in the frontier or explored.
            if not frontier.contains_state(state) and state not in explored:
                # This "child" is the next actor connecting the previous one through the movie as it was the action.
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    # This runs if the name is repeated.
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
