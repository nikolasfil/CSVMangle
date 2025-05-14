from pathlib import Path
import pandas


class Mangler:
    def __init__(self):
        self.parent = Path(__file__).parent.parent

        self.folder_src = Path(self.parent, "src")
        self.folder_data = Path(self.parent, "data")
        self.folder_out = Path(self.parent, "out")

        self.dictionary = {}

    def split_file(self, file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            # pass
        # print(lines)

        new_path_properties = Path(self.folder_out, f"properties-{file_path.name}")
        with open(new_path_properties, "w") as file:
            for i in range(33):
                file.write(lines[i])

        new_path_csv = Path(self.folder_out, f"csv-{file_path.name}")
        with open(new_path_csv, "w") as file:
            for i in range(33, len(lines)):
                file.write(lines[i])

    def read_csv(self, file_path):
        # Read a CSV file into a pandas DataFrame
        df = pandas.read_csv(file_path)
        return df

    def list_data_contents(self):

        if not self.folder_data.exists():
            print(f"The folder {self.folder_data} does not exist.")
            return

        # print(f"Contents of {self.folder_data}:")

        for item in self.folder_data.iterdir():
            if item.is_dir():
                # print(f"Directory: {item.name}")
                for sub_item in item.iterdir():
                    if sub_item.is_file():
                        print(f"File: {sub_item.name}")
                        self.split_file(sub_item)
                    else:
                        # print(f"Directory: {sub_item.name}")
                        pass

    def main(self):
        self.list_data_contents()


if __name__ == "__main__":
    # Entry point for the script
    mangler = Mangler()
    mangler.main()
