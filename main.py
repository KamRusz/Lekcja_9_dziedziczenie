import csv
from sys import argv
from os import listdir, path, system, name
from pathlib import Path
import json
import pickle


class Reader:
    flag = "r"

    def __init__(self):
        self.load_file_path = argv[1]

    def read(self):
        try:
            with open(self.load_file_path, self.flag) as file:
                return self.read_inner(file)
        except FileNotFoundError:
            quit(
                "\nścieżka odczytu nie istnieje!\n"
                "Poniżej lista plików z katalogu"
                f" [{path.abspath(Path(argv[1]).parent)}]:"
                f"\n{listdir(path.abspath(Path(argv[1]).parent))}\n"
            )


class JsonReader(Reader):
    def read_inner(self, file):
        return json.load(file)


class CsvReader(Reader):
    def read_inner(self, file):
        return list(csv.reader(file, skipinitialspace=True, delimiter=","))


class PickleReader(Reader):
    flag = "rb"

    def read_inner(self, file):
        return pickle.load(file)


class Writer:
    flag = "w"
    nl = None

    def __init__(self):
        self.save_file_path = argv[2]

    def write(self, data):
        with open(self.save_file_path, self.flag) as file:
            return self.write_inner(file, data)


class JsonWriter(Writer):
    def write_inner(self, file, data):
        json.dump(data, file, indent=4, ensure_ascii=False)


class CsvWriter(Writer):
    nl = ""

    def write_inner(self, file, data):
        csv.writer(file).writerows(data)


class PickleWriter(Writer):
    flag = "wb"

    def write_inner(self, file, data):
        pickle.dump(data, file)


class Manager:
    read_dict = {
                ".json": JsonReader,
                ".csv": CsvReader,
                ".pickle": PickleReader
                }
    write_dict = {
                ".json": JsonWriter,
                ".csv": CsvWriter,
                ".pickle": PickleWriter
                }

    def __init__(self):
        try:
            load_ext = Path(argv[1])
            if not path.exists(load_ext):
                quit(
                    "\nścieżka odczytu nie istnieje!\n"
                    "Poniżej lista plików z katalogu"
                    f" [{path.abspath(load_ext.parent)}]:"
                    f"\n{listdir(path.abspath(load_ext.parent))}\n"
                )
            if not path.isfile(load_ext):
                quit(
                    "\nścieżka odczytu nie jest plikiem!\n"
                    "Poniżej lista plików z katalogu"
                    f" [{path.abspath(load_ext.parent)}]:"
                    f"\n{listdir(load_ext.parent)}\n"
                )
        except IndexError:
            quit("nie podano scieżki odczytu")

        try:
            save_ext = Path(argv[2])
            if not save_ext.suffix:
                quit("\nścieżka zapisu nie jest plikiem!\n")
        except IndexError:
            quit("\nnie podano scieżki zapisu")

        self.reader = self.read_dict[load_ext.suffix]()
        self.writer = self.write_dict[save_ext.suffix]()

    def execute(self):
        self.data = self.reader.read()
        self.make_change()
        self.printer()
        self.writer.write(self.data)

    def make_change(self):
        try:
            self.changes = [x.split(",") for x in argv[3:]]
            print(self.data)
            for change in self.changes:
                if len(self.data) <= int(change[0]) or len(
                    self.data[0]) <= int(change[1]
                    ):
                    print(
                        f"\nwspółrzedne [{change[0]},{change[1]}]"
                        " poza zakresem pliku"
                    )
                else:
                    self.data[
                            int(change[0])][int(change[1])
                             ] = ",".join(change[2:])
        except IndexError:
            print("nie podano argumentów - plik zapisany bez zmian")

    def printer(self):
        system("cls" if name == "nt" else "clear")
        print("\n")
        for line in self.data:
            print(line)
        print("\n")


if __name__ == "__main__":
    obj = Manager()
    obj.execute()
