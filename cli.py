import cmd
import model

class WCCLI(cmd.Cmd):

    intro = "Welcome to the World Cup Predictor.\nType 'start' to get going!\nType 'help' for a list of commands."
    prompt = "What next?"

    def __init__(self):

        super(WCCLI, self).__init__()

        self.model = None

    def do_start(self, args):
        """Load all of the fixtures and predictions"""
        try:
            self.model = model.FixtureFactory()
            self.model.load()
        except Exception as err:
            print(str(err))

    def do_print(self, args):
        """Print all of the loaded details"""
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
            player_name = model.pick("Player", sorted(list(self.model.predictions.keys())))
            predos = list(self.model.predictions[player_name])
            predos.sort(reverse=False)
            for predo in predos:
                print(predo)

        except Exception as err:
            print(str(err))

    def do_groups(self, args):
        """Print Group details"""
        try:
            self.model.print_groups()
        except Exception as err:
            print(str(err))

    def do_teams(self, args):
        """Print ALL Teams"""
        try:
            self.model.print_teams()
        except Exception as err:
            print(str(err))

    def do_quit(self, args):
        '''End the session'''
        print("bye bye")
        exit(0)
