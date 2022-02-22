import csv
from sys import argv, exit
from os import listdir, path, system, name
import json
import pickle


class CommonReader:
    data = []

    def __init__(self):
        self.load_file_path = str
        self.save_file_path = str
        self.changes = []
        self.change_flag = True

    def cls(self):
        system("cls" if name == "nt" else "clear")

    def testing_parameters(self):
        try:
            self.load_file_path = argv[1]
            self.save_file_path = argv[2]
            if path.exists(self.load_file_path):
                if path.isfile(self.load_file_path):
                    pass
                else:
                    quit(
                        f"\nścieżka odczytu nie jest plikiem!\n"
                        "Poniżej lista plików z katalogu"
                        f" [{path.abspath(self.load_file_path)}]:"
                        f"\n{listdir(self.load_file_path)}\n"
                    )
            else:
                quit("ścieżka odczytu nie istnieje")
        except IndexError:
            exit("nie podano ścieżki")
        try:
            self.changes = [x.split(",") for x in argv[3:]]
        except IndexError:
            print("nie podano argumentów - plik zapisany bez zmian")
            self.change_flag = False

    def kind_of_file(self):
        self.load_ext = self.load_file_path.split(".")[-1]
        print(self.load_ext)
        self.save_ext = self.save_file_path.split(".")[-1]
        print(self.save_ext)

    def make_change(self):
        for change in self.changes:
            if self.change_flag:
                if len(self.data) <= int(change[0]) or len(self.data[0]) <= int(
                    change[1]
                ):
                    print(
                        f"\nwspółrzedne [{change[0]},{change[1]}]"
                        " poza zakresem pliku"
                    )
                else:
                    self.data[int(change[0])][int(change[1])] = change[2]

    def printer(self):
        system("cls" if name == "nt" else "clear")
        print("\n")
        for line in self.data:
            print(line)
        print("\n")


class SpecificReader(CommonReader):
    def read_csv(self):
        with open(self.load_file_path, "r", newline="") as self.file:
            self.reader = csv.reader(
                self.file, skipinitialspace=True, delimiter=","
                )
            CommonReader.data = list(self.reader)
            return CommonReader.data

    def save_csv(self):
        with open(self.save_file_path, "w", newline="") as self.file:
            self.writer = csv.writer(self.file)
            self.writer.writerows(self.data)

    def read_json(self):
        with open(self.load_file_path, "r") as self.file:
            CommonReader.data = json.load(self.file)
            return CommonReader.data

    def save_json(self):
        with open(self.save_file_path, "w") as self.file:
            json.dump(
                CommonReader.data, self.file, indent=4, ensure_ascii=False
                )

    def read_pickle(self):
        with open(self.load_file_path, "rb") as self.file:
            CommonReader.data = pickle.load(self.file)
            return CommonReader.data

    def save_pickle(self):
        with open(self.save_file_path, "wb") as self.file:
            pickle.dump(CommonReader.data, self.file, pickle.HIGHEST_PROTOCOL)

def main():
    plik = SpecificReader()
    plik.testing_parameters()
    plik.kind_of_file()

    if plik.load_ext == "csv":
        plik.read_csv()
    elif plik.load_ext == "json":
        plik.read_json()
    elif plik.load_ext == "pickle":
        plik.read_pickle()

    # dispatcher2 = {
    # "load":{
    #       "csv":plik.read_csv, "json":SpecificReader.read_json,
    #       "pickle":SpecificReader.read_json},
    # "save":{"csv":SpecificReader.save_csv, "json":SpecificReader.save_json,
    #        "pickle":SpecificReader.save_json}
    # }
    #dispatcher2["load"]["csv"]()
 
    plik.make_change()
    plik.printer()

    if plik.save_ext == "csv":
        plik.save_csv()
    elif plik.save_ext == "json":
        plik.save_json()
    else:
        plik.save_pickle()


if __name__ == "__main__":
    main()
