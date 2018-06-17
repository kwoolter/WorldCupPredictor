import csv
import datetime


class Team:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Fixture:
    def __init__(self, team_a: Team, team_b: Team, when: datetime, group: str = {"X"}, score: str = None):
        self.team_a = team_a
        self.team_b = team_b
        self.when = datetime.datetime.strptime(when, "%d/%m/%Y")
        self.group = group
        self.score = Score(score)
        self.points = None

    def __str__(self):
        str = "Group {4}: {0} {3} {1} [{2}]".format(self.team_a,
                                                    self.team_b,
                                                    datetime.datetime.strftime(self.when, "%d/%m/%Y"),
                                                    self.score,
                                                    self.group)
        if self.points is not None:
            str += "(points={0})".format(self.points)

        return str

    def is_played(self):
        if self.score.is_valid() is True:
            return True
        else:
            return False


class Score:
    WIN = "win"
    DRAW = "draw"
    LOSE = "lose"
    INVALID = "invalid"

    EXACT = 3
    CORRECT = 1
    WRONG = 0

    def __init__(self, score: str = None):

        if score is not None and score.find(":") > 0:
            a, b = score.split(":")
            self.score_a = int(a)
            self.score_b = int(b)
        else:
            self.score_a = "-"
            self.score_b = "-"

    def __str__(self):
        return "{0}:{1}".format(self.score_a, self.score_b)

    def is_valid(self):
        if self.score_a == "-" or self.score_b == "-":
            return False
        else:
            return True

    def result(self):

        if self.is_valid() is False:
            return Score.INVALID
        elif self.score_a > self.score_b:
            return Score.WIN
        elif self.score_a == self.score_b:
            return Score.DRAW
        else:
            return Score.LOSE

    def compare(self, other_score):

        points = 0

        if self.is_valid() is False or other_score.is_valid() is False:
            points = 0
        elif self.score_a == other_score.score_a and self.score_b == other_score.score_b:
            points = Score.EXACT
        elif self.result() == other_score.result():
            points = Score.CORRECT

        return points


class Player:
    def __init__(self, name: str):
        self.name = name


class FixtureFactory:
    def __init__(self):
        self.fixtures = []
        self.predictions = {}
        self.scores = {}
        self.groups = {}
        self.teams = set()

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
                print(str(row))
                group = row.get("Group")
                team_a = row.get("TeamA")
                team_b = row.get("TeamB")
                when = row.get("When")
                score = row.get("Score")

                self.fixtures.append(Fixture(team_a, team_b, when, group, score))

                if group not in self.groups.keys():
                    self.groups[group] = set()

                self.groups[group] = self.groups[group] | {team_a, team_b}
                self.teams = self.teams | {team_a, team_b}

                # loop through all of the header fields except the first 5 columns...
                for i in range(5, len(header)):

                    player_name = header[i]

                    # Get the next field name from the header row
                    predicted_score = row.get(player_name)

                    if player_name not in self.predictions.keys():
                        self.predictions[player_name] = []

                    if player_name not in self.scores.keys():
                        self.scores[player_name] = 0

                    prediction = Fixture(team_a, team_b, when, group, predicted_score)
                    actual = Score(score)
                    predo = Score(predicted_score)
                    points = actual.compare(predo)
                    prediction.points = points
                    self.scores[player_name] += points
                    self.predictions[player_name].append(prediction)
                    # print("Player {0} score {1}".format(player_name,self.scores[player_name]))

            # Close the file
            object_file.close()

    def print(self):

        print("\nTeams")
        print("{0}".format(self.teams))

        print("\nGroups")
        for group in sorted(list(self.groups.keys())):
            teams = sorted(list(self.groups[group]))
            print("Group {0}:".format(group))
            for team in teams:
                print("\t{0}".format(team))

        print("\nResults")
        for fixture in self.fixtures:
            if fixture.is_played() is True:
                print(fixture)

        print("\nPredictions")
        for player in self.predictions.keys():
            print("Player {0} predictions".format(player))
            for prediction in self.predictions[player]:
                print(prediction)


    def print_player_scores(self):
        hst = HighScoreTable("World Cup Predictor")

        for player in self.scores.keys():
            # print("Player {0}: {1}".format(player, self.scores[player]))
            hst.add(player, self.scores[player])

        hst.print()
        print("\n")

    def print_groups(self):
        print("\nGroups")
        for group in sorted(list(self.groups.keys())):
            teams = sorted(list(self.groups[group]))
            print("Group {0}:".format(group))
            for team in teams:
                print("\t{0}".format(team))
        print("\n")


from operator import itemgetter
import pickle
import logging


class HighScoreTable():
    def __init__(self, name="default", max_size=10, prefix=""):
        self.name = name
        self.max_size = max_size
        self.prefix = prefix
        self.table = []

    def add(self, name: str, score: float, auto_save=False):

        added = False

        # If the specified score makes it into the high score table...
        if self.is_high_score(score):
            # Add it and re-sort the table
            self.table.append((name, score))
            self.table.sort(key=itemgetter(1, 0), reverse=True)
            added = True

        # Trim the size of the table to be the maximum size
        while len(self.table) > self.max_size:
            del self.table[-1]

        if auto_save is True:
            self.save()

        return added

    def is_high_score(self, score):
        if len(self.table) < self.max_size:
            return True
        else:
            name, lowest_score = self.table[len(self.table) - 1]
            if score > lowest_score:
                return True
            elif score == lowest_score and len(self.table) < self.max_size:
                return True
            else:
                return False

    def save(self):
        file_name = self.name + ".hst"
        game_file = open(file_name, "wb")
        pickle.dump(self, game_file)
        game_file.close()

        logging.info("%s saved." % file_name)

    def load(self):

        file_name = self.name + ".hst"

        try:
            game_file = open(file_name, "rb")

            new_table = pickle.load(game_file)

            self.table = new_table.table
            self.max_size = new_table.max_size

            game_file.close()

            logging.info("\n%s loaded.\n" % file_name)

        except IOError:

            logging.warning("High Score Table file %s not found." % file_name)

    def print(self):
        print("%s High Score Table - top %i scores" % (self.name, self.max_size))

        if len(self.table) == 0:
            print("No high scores recorded.")
        else:
            for i in range(len(self.table)):
                name, score = self.table[i]
                print("%i. %s - %s%s" % (i + 1, name, self.prefix, format(score, ",d")))
