import csv
from os.path import exists


class Reader:
    def __init__(self, CSV_file_name):
        self.csv_file_data = []
        # self.validate_csv_file(CSV_file_name)
        self.read_file(CSV_file_name)

    def validate_csv_file(self, CSV_file_name):
        while not exists(CSV_file_name) or not CSV_file_name.lower().endswith(".csv"):
            input("should be csv file : ")

    def read_file(self, CSV_file_name):
        with open(CSV_file_name, encoding='utf-8') as file:
            reader = csv.reader(file)
            for line in reader:
                self.csv_file_data.append(line)

    def get_data_as_list(self):
        return self.csv_file_data

    def get_number_of_columns(self):
        return len(self.csv_file_data[0])


class Model:
    def __init__(self, data_list, col_count):
        """get data as list"""
        self.data_counter = len(data_list)
        self.data = {}
        self.list_of_sets_of_col_options = [set({}) for num in range(col_count)]
        self.dependent_probability = {}
        self.save_data(data_list)
        self.processed_data = {key: {col: {} for col in range(len(self.list_of_sets_of_col_options) - 1)} for key in
                               self.data.keys()}
        self.get_dependent_probability()
        self.create_model()

    def save_data(self, data_list):
        """insearting data in list data and get sets of all col options"""
        for row in data_list:
            if not row[-1] in self.data.keys():
                self.data[row[-1]] = []
            self.data[row[-1]].append(tuple(row))
            counter = 0
            for col in row:
                self.list_of_sets_of_col_options[counter].add(col)
                counter += 1

    def get_colum_conditional_probability(self, col):
        """return list of the probability for differnt uses"""
        for key in self.data.keys():
            for col_options in self.list_of_sets_of_col_options[col]:
                self.processed_data[key][col].update({col_options: 0})
            for row in self.data[key]:
                self.processed_data[key][col][row[col]] += 1 / len(self.data[key])
            for row in self.processed_data[key][col]:
                if self.processed_data[key][col][row] == 0:
                    self.processed_data[key][col][row] = 1 / (len(self.data[key]) + 1)

    def create_model(self):
        for col in range(len(self.list_of_sets_of_col_options) - 1):
            self.get_colum_conditional_probability(col)
        print("The model built successfully")
        return True

    def get_dependent_probability(self):
        for key in self.data.keys():
            self.dependent_probability.update({key: len(self.data[key]) / self.data_counter})
        # print(self.dependent_probability)

    def get_expected_answer(self, row):
        probability_list = {key: 1 for key in self.processed_data}
        for key in self.processed_data:
            col = 0
            for data in row:
                probability_list[key] *= self.processed_data[key][col][data]
                col += 1
            probability_list[key] *= self.dependent_probability[key]

        # print(probability_list)
        return max(probability_list, key=probability_list.get)

    def get_correctness(self, csvfile):
        rows_counter = 0
        correct_counter = 0
        with open(csvfile, encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                rows_counter += 1
                if self.get_expected_answer(row[0:-1]) == row[-1]:
                    correct_counter += 1
        return correct_counter / rows_counter


if __name__ == '__main__':
    csv_data_reader = Reader("mashroom.csv")
    dat_list = csv_data_reader.get_data_as_list()
    # columns_count = csv_data_reader.get_number_of_columns()
    # mod1 = Model(dat_list, columns_count)
    # print(mod1.processed_data)
    # a = "senior,medium,yes,fair"
    # a.split(",")
    # print(mod1.get_correctness("mashroom.csv"))
