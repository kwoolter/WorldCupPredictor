import matplotlib.pyplot as plt
import model
import numpy as np


class ScoresChart:

    def __init__(self, model : model.FixtureFactory):

        self.model = model

    def draw(self):

        fig = plt.figure(1, figsize=(6,8))

        # Player Score History
        plt.subplot(2,1, 1)

        plt.ylabel('Score')
        plt.xlabel('Date')
        plt.title("Score History")

        player_scores = self.model.player_score_history()
        player_colours = ('c', 'b', 'r', 'violet')

        count = 0
        for player in sorted(player_scores.keys()):
            cum_sum = np.cumsum( list(player_scores[player].values()))
            plt.plot(list(player_scores[player].keys()),cum_sum, player_colours[count])
            count +=1

        plt.legend(sorted(list(player_scores.keys())),loc='lower right')
        plt.grid(True)
        plt.ylim(bottom=0)

        # Total Player Scores
        plt.subplot(2,1, 2)

        plt.ylabel('Score')
        plt.xlabel('Player')
        plt.title("Scores")

        ax = plt.gca()
        ax.yaxis.grid(True)

        x = list(self.model.scores.keys())
        x_pos = np.arange(len(x))
        y = list(self.model.scores.values())
        min_score = np.min(y)
        max_score = np.max(y)

        plt.ylim(bottom=(max(0,min_score - 10)))
        plt.ylim(top=(max_score + 10))
        plt.bar(x_pos,y, align="center")
        plt.xticks(x_pos,x)

        ax = plt.gca()

        add_value_labels(ax, spacing=2)

        fig.tight_layout()

        plt.savefig('scores.png')
        plt.show()




def add_value_labels(ax, spacing=5):
    """Add labels to the end of each bar in a bar chart.

    Arguments:
        ax (matplotlib.axes.Axes): The matplotlib object containing the axes
            of the plot to annotate.
        spacing (int): The distance between the labels and the bars.
    """

    # For each bar: Place a label
    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Use Y value as label and format number with one decimal place
        label = "{:.0f}".format(y_value)

        # Create annotation
        ax.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(0, space),          # Vertically shift label by `space`
            textcoords="offset points", # Interpret `xytext` as offset in points
            ha='center',                # Horizontally center label
            va=va)                      # Vertically align label differently for
                                        # positive and negative values.
