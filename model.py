import datetime
import csv

class Team:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Fixture:
    def __init__(self, team_a : Team, team_b : Team, when : datetime, group : str = {"X"}, score : str = None):
        self.team_a = team_a
        self.team_b = team_b
        self.when = when
        self.group = group
        self.score = Score(score)

    def __str__(self):
        return "Group {4}: {0} {3} {1} [{2}]".format(self.team_a,
                                                     self.team_b,
                                                     self.when,
                                                     self.score,
                                                     self.group)

class Score:
    def __init__(self, score : str =  None):
        if score is not None:
            a,b = score.split(":")
            self.score_a = int(a)
            self.score_b = int(b)
        else:
            self.score_a = "-"
            self.score_b = "-"

    def __str__(self):
        return "{0}:{1}".format(self.score_a, self.score_b)

    def compare(self, other_score):
        return

class Player:
    def __init__(self, name : str):
        self.name = name

class FixtureFactory:
    def __init__(self):
        self.fixtures = []
        self.predictions = {}

    def load(self):
        print("\nLoading fixtures...")

        # Attempt to open the file
        with open(".\\data\\fixtures.csv", 'r') as object_file:

            # Load all rows in as a dictionary
            reader = csv.DictReader(object_file)

            # Get the list of column headers
            header = reader.fieldnames

            # For each row in the file....
            for row in reader:
                group = row.get("Group")
                team_a = row.get("TeamA")
                team_b = row.get("TeamB")
                when = row.get("When")
                score = row.get("Score")

                self.fixtures.append(Fixture(team_a, team_b, when, group, score))

                # loop through all of the header fields except the first 5 columns...
                for i in range(5, len(header)):

                    player_name = header[i]
                    # Get the next field name from the header row
                    prediction = row.get(player_name)

                    if player_name not in self.predictions.keys():
                        self.predictions[player_name] = []

                    self.predictions[player_name].append(Fixture(team_a, team_b, when, group, prediction))

            # Close the file
            object_file.close()

    def print(self):

        for fixture in self.fixtures:
            print(fixture)


        for player in self.predictions.keys():
            print("Player {0} predictions".format(player))
            for prediction in self.predictions[player]:
                print(prediction)
