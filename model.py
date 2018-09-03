import csv
import datetime


class Team:
    def __init__(self, name):
        self.name = name
        self.won = 0
        self.lost = 0
        self.drawn = 0
        self.goals_for = 0
        self.goals_against = 0

    def __str__(self):
        return self.name

    @property
    def points(self):
        return self.won * 3 + self.drawn

    @property
    def played(self):
        return self.won + self.drawn + self.lost

    @property
    def goal_diff(self):
        return self.goals_for - self.goals_against

    def __lt__(self, other_team):
        if self.points > other_team.points:
            return False
        elif self.points < other_team.points:
            return True
        else:
            if self.goal_diff > other_team.goal_diff:
                return False
            elif self.goal_diff < other_team.goal_diff:
                return True
            elif self.goals_for < other_team.goals_for:
                return True
            else:
                return self.name > other_team.name


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

    def __lt__(self, other_fixture):
        if self.group > other_fixture.group:
            return False
        elif self.when > other_fixture.when:
            return False
        elif self.team_a.name > other_fixture.team_a.name:
            return False
        else:
            return True

    def is_played(self):
        if self.score.is_valid() is True:
            return True
        else:
            return False

    def calc_stats(self):

        if self.score.is_valid() is True:

            self.team_a.goals_for += self.score.score_a
            self.team_a.goals_against += self.score.score_b
            self.team_b.goals_for += self.score.score_b
            self.team_b.goals_against += self.score.score_a

            if self.score.result() == Score.WIN:
                self.team_a.won += 1
                self.team_b.lost += 1
            elif self.score.result() == Score.DRAW:
                self.team_a.drawn += 1
                self.team_b.drawn += 1
            if self.score.result() == Score.LOSE:
                self.team_b.won += 1
                self.team_a.lost += 1


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
        self.correct_result = 0
        self.exact_result = 0


class FixtureFactory:
    def __init__(self):
        self.fixtures = []
        self.predictions = {}
        self.scores = {}
        self.groups = {}
        self.teams = {}

    def load(self):
        print("\nLoading fixtures...")

        # Attempt to open the file
        with open(".\\data\\PL_fixtures.csv", 'r') as object_file:

            # Load all rows in as a dictionary
            reader = csv.DictReader(object_file)

            # Get the list of column headers
            header = reader.fieldnames

            # For each row in the file....
            for row in reader:
                # print(str(row))
                group = row.get("Group")
                team_a_name = row.get("TeamA")
                team_b_name = row.get("TeamB")
                when = row.get("When")
                score = row.get("Score")

                if team_a_name not in self.teams.keys():
                    self.teams[team_a_name] = Team(team_a_name)

                if team_b_name not in self.teams.keys():
                    self.teams[team_b_name] = Team(team_b_name)

                team_a = self.teams[team_a_name]
                team_b = self.teams[team_b_name]

                result = Fixture(team_a, team_b, when, group, score)
                result.calc_stats()
                self.fixtures.append(result)

                if group not in self.groups.keys():
                    self.groups[group] = set()

                self.groups[group] = self.groups[group] | {team_a_name, team_b_name}

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

        self.print_groups()
        self.print_teams()

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
            team_names = list(self.groups[group])
            teams = []
            for team_name in team_names:
                teams.append(self.teams[team_name])

            teams.sort(reverse=True)
            print("\nGroup {0}".format(group))
            row_format = "{0:^25} {1:^3} {2:^3} {3:^3} {4:^3} {5:^3} {6:^3} {7:^3} {8:^3}"
            print(row_format.format("Team", "P", "W", "D", "L", "F", "A", "GD", "Pts"))
            for team in teams:
                print(row_format.format(team.name, team.played, team.won, team.drawn, team.lost,
                                        team.goals_for, team.goals_against, team.goal_diff, team.points))
        print("\n")

    def print_teams(self):
        print("\nTeams")
        row_format = "{0:^25} {1:^3} {2:^3} {3:^3} {4:^3} {5:^3} {6:^3} {7:^3} {8:^3}"
        print(row_format.format("Team", "P", "W", "D", "L", "F", "A", "GD", "Pts"))
        for team_name in sorted(list(self.teams.keys())):
            team = self.teams[team_name]
            print(row_format.format(team.name, team.played, team.won, team.drawn, team.lost,
                                    team.goals_for, team.goals_against, team.goal_diff, team.points))
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


def pick(object_type: str, objects: list, auto_pick: bool = False):
    '''pick() -  Function to present a menu to pick an object from a list of objects
    auto_pick means if the list has only one item then automatically pick that item'''

    selected_object = None
    choices = len(objects)
    vowels = "AEIOU"
    if object_type[0].upper() in vowels:
        a_or_an = "an"
    else:
        a_or_an = "a"

    # If the list of objects is no good the raise an exception
    if objects is None or choices == 0:
        raise (Exception("No %s to pick from." % object_type))

    # If you selected auto pick and there is only one object in the list then pick it
    if auto_pick is True and choices == 1:
        selected_object = objects[0]

    # While an object has not yet been picked...
    while selected_object == None:

        # Print the menu of available objects to select
        print("Select %s %s:-" % (a_or_an, object_type))

        for i in range(0, choices):
            print("\t%i) %s" % (i + 1, str(objects[i])))

        # Along with an extra option to cancel selection
        print("\t%i) Cancel" % (choices + 1))

        # Get the user's selection and validate it
        choice = input("%s?" % object_type)
        if is_numeric(choice) is not None:
            choice = int(choice)

            if 0 < choice <= choices:
                selected_object = objects[choice - 1]
                logging.info("pick(): You chose %s %s." % (object_type, str(selected_object)))
            elif choice == (choices + 1):
                raise (Exception("You cancelled. No %s selected" % object_type))
            else:
                print("Invalid choice '%i' - try again." % choice)
        else:
            print("You choice '%s' is not a number - try again." % choice)

    return selected_object


def is_numeric(s):
    try:
        x = int(s)
    except:
        try:
            x = float(s)
        except:
            x = None
    return x
