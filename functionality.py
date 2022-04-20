import pandas
import random


class TypeTest:
    def __init__(self):
        self.word_count = 0
        self.spelling = 0
        self.words_to_type = ""
        self.words_to_type_list = []
        self.inputted_words_list = []
        self.get_new_words()

    def get_new_words(self):
        """ Select 100 words randomly from the .csv file. Makes a list and a string with those 100 words. """
        word_data = pandas.read_csv("data.csv")
        all_words = word_data["word"].to_list()
        for w in range(1, 101):
            random_w = f"{random.choice(all_words)} "
            self.words_to_type += random_w
        self.words_to_type_list = self.words_to_type.split()

    def start_again(self):
        """ Re-set values and word lists. """
        self.word_count = 0
        self.spelling = 0
        self.words_to_type = ""
        self.words_to_type_list = []
        self.inputted_words_list = []
        self.get_new_words()

    def word_per_minute(self, typed_words):
        """ Returns the amount of correct spelled words. Note words are compared according to their index. """
        self.inputted_words_list = typed_words.split()
        for n in range(len(self.inputted_words_list)):
            if self.inputted_words_list[n] == self.words_to_type_list[n]:
                self.word_count += 1
        return self.word_count

    def spell_check(self, w_count, input_w_list):
        """ Checks if there are misspelled words and how many. """
        self.spelling = len(input_w_list) - w_count
        if self.spelling == 0:
            return f"You spelled all words correct"
        elif self.spelling > 0:
            return f"You misspelled: {self.spelling} words\nThey were not counted in your WPM score."
