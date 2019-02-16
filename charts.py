import matplotlib.pyplot as plt
import model
import numpy as np

class ScoresChart:

    def __init__(self, model : model.FixtureFactory):
        self.model = model


    def draw(self):


        plt.figure(1, figsize=(12, 5))

        # Player Score History
        plt.subplot(1, 2, 1)

        plt.ylabel('Score')
        plt.xlabel('Time')
        plt.title("Score History")

        player_scores = self.model.player_score_history()

        for player in player_scores.keys():
            cum_sum = np.cumsum( list(player_scores[player].values()))
            plt.plot(list(player_scores[player].keys()),cum_sum)

        plt.legend(list(player_scores.keys()),loc='lower right')
        plt.grid(True)
        plt.ylim(bottom=0)

        # Total Player Scores
        plt.subplot(1, 2, 2)

        plt.ylabel('Score')
        plt.xlabel('Player')
        plt.title("Scores")

        ax = plt.gca()
        ax.yaxis.grid(True)

        x = list(self.model.scores.keys())
        y = list(self.model.scores.values())

        plt.bar(x,y)

        plt.show()


