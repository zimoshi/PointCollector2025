from json import load, dump
print("PointCollector 2025 version")
class Team:
    def __init__(self, name): # type: ignore[attr-defined]
        self.name = name
        self.points = 0

    def add_points(self, points): # type: ignore[attr-defined]
        self.points += points # type: ignore[attr-defined]

    def __str__(self):
        return f"{self.name}: {self.points} points" # type: ignore[attr-defined]
teams : dict[str, Team] = {}
while True:
    i = input("Type a command ('exit', 'help', 'addteam', 'addpoint', \
'showteams', 'showpoints', 'deletepoint', 'deleteteam', 'save', 'load'): ")
    if i == "exit":
        print("Exiting PointCollector 2025.")
        break
    elif i == "help":
        print("Available commands: 'exit', 'help', 'addteam', 'addpoint', \
'showteams', 'showpoints', 'deletepoint', 'deleteteam', 'save', 'load'")
    elif i == "addteam":
        t = input("Enter team name: ")
        teams.update({t: Team(t)})
        print(f"Team '{t}' added.")
    elif i == "addpoint":
        t = input("Enter team name: ")
        if t in teams:
            p = int(input("Enter points to add: "))
            teams[t].add_points(p) # type: ignore[attr-defined]
            print(f"Added {p} points to team '{t}'.")
        else:
            print(f"Team '{t}' does not exist.")
    elif i == "showteams":
        print("Teams:")
        for team in teams.values():
            print(team)
    elif i == "showpoints":
        print("Points:")
        for team in teams.values():
            print(team)
    elif i == "deletepoint":
        t = input("Enter team name: ")
        if t in teams:
            p = int(input("Enter points to delete: "))
            if p <= teams[t].points: # type: ignore[attr-defined]
                teams[t].add_points(-p) # type: ignore[attr-defined]
                print(f"Deleted {p} points from team '{t}'.")
            else:
                print(f"Cannot delete {p} points from team '{t}' as it has only {teams[t].points} points.") # type: ignore[attr-defined]
        else:
            print(f"Team '{t}' does not exist.")
    elif i == "deleteteam":
        t = input("Enter team name: ")
        if t in teams:
            del teams[t]
            print(f"Team '{t}' deleted.")
        else:
            print(f"Team '{t}' does not exist.")
    elif i == "save":
        with open("teams.json", "w") as f:
            dump({name: team.points for name, team in teams.items()}, f) # type: ignore[attr-defined]
        print("Teams saved to 'teams.json'.")
    elif i == "load":
        try:
            with open("teams.json", "r") as f:
                loaded_teams = load(f)
                teams = {name: Team(name) for name in loaded_teams.keys()}
                for name, points in loaded_teams.items():
                    teams[name].add_points(points) # type: ignore[attr-defined]
            print("Teams loaded from 'teams.json'.")
        except FileNotFoundError:
            print("No saved teams found. Please save teams first.")
    else:
        print("Unknown command. Type 'help' for a list of commands.")
print("PointCollector 2025 session ended.")
print("Thank you for using PointCollector 2025!")
print("Goodbye!")