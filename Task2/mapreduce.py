from collections import defaultdict

class MapReduce:
    def __init__(self, text):
        self.text = text
        self.mapper = self.map_function()
        self.shuffle = self.shuffle_function()
        self.mpreduce = self.reduce_function()

    def map_function(self):
        words = self.text.split()
        return [(word, 1) for word in words]

    def shuffle_function(self):
        shuffled = defaultdict(list)
        for key, value in self.mapper:
            shuffled[key].append(value)
        return shuffled.items()

    def reduce_function(self):
        reduced = {}
        for key, values in self.shuffle:
            reduced[key] = sum(values)
        return reduced
    


if __name__ == "__main__":
    pass
