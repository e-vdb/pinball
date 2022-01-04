import pandas as pd


class Score:
    def __init__(self):
        self.filepath = 'scores.csv'

    def create_csv(self):
        # initialize list of lists
        data = {'Player': ['Player_' + str(i) for i in range(1, 6)], 'Time': [0 for i in range(1, 6)]}
        # Create the pandas DataFrame
        self.df = pd.DataFrame(data, columns=['Player', 'Time'])
        self.df.to_csv(self.filepath, index=False)

    def load_score(self):
        try:
            self.df = pd.read_csv(self.filepath)
        except OSError:
            self.create_csv()

    def erase_score(self):
        self.create_csv()

    def sort_by_score(self):
        self.df.sort_values(by='Time', ascending=False, inplace=True)

    def add_score(self, name, time_game):
        data = {'Player': name, 'Time': time_game}
        self.df = self.df.append(data, ignore_index=True)
        self.sort_by_score()
        self.df.to_csv(self.filepath, index=False)
