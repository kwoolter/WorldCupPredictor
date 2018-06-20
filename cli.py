import cmd
import model

class WCCLI(cmd.Cmd):

    intro = "Welcome to the World Cup Predictor.\nType 'start' to get going!\nType 'help' for a list of commands."
    prompt = "What next?"

    def __init__(self):

        super(WCCLI, self).__init__()

        self.model = None

    def do_start(self, args):
        """Start the game"""
        try:
            self.model = model.FixtureFactory()
            self.model.load()
        except Exception as err:
            print(str(err))

    def do_print(self, args):
        """Print the game"""
        try:
            self.model.print()
        except Exception as err:
            print(str(err))

    def do_scores(self, args):
        """Print player scores"""
        try:
            self.model.print_player_scores()
        except Exception as err:
            print(str(err))

    def do_predos(self, args):
        """Print specific player's predictions and scores"""
        try:
            player_name = model.pick("Player", list(self.model.predictions.keys()))
            for predo in self.model.predictions[player_name]:
                print(predo)

        except Exception as err:
            print(str(err))

    def do_groups(self, args):
        """Print Groups"""
        try:
            self.model.print_groups()
        except Exception as err:
            print(str(err))

    def do_teams(self, args):
        """Print Teams"""
        try:
            self.model.print_teams()
        except Exception as err:
            print(str(err))
