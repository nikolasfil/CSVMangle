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
        df = pandas.read_csv(
            file_path, skipinitialspace=True, encoding="latin-1"
        )  # use 'latin-1' or 'cp1252' if needed

        return df

    def read_max_height(self, file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
        return lines[20].split("Max Broadband Load       : ")[1]

    def list_data_contents(self, folder_path):

        if not folder_path.exists():
            print(f"The folder {folder_path} does not exist.")
            return

        for item in folder_path.iterdir():
            if item.is_dir():
                print(f"Directory: {item.name}")
                for sub_item in item.iterdir():
                    if sub_item.is_file():
                        print(f"File: {sub_item.name}")
                        self.split_file(sub_item)

            elif item.is_file():
                # print(f"File: {item.name}")
                if "properties-" in item.name:
                    # print(f"File: {item.name}")
                    max_height = self.read_max_height(item)
                    print(f"Max height: {max_height}")

                elif "csv-" in item.name:
                    # print(f"File: {item.name}")
                    df = self.read_csv(item)
                    df["Brd Reslt"] = pandas.to_numeric(
                        df["Brd Reslt"], errors="coerce"
                    )
                    # Calculate and print the mean (μέση τιμή)
                    mean_value = df["Brd Reslt"].mean()
                    print(f"Μέση τιμή (mean) της στήλης 'Brd Reslt': {mean_value:.2f}")

    def main(self):
        # self.list_data_contents(self.folder_data)
        self.list_data_contents(self.folder_out)


if __name__ == "__main__":
    # Entry point for the script
    mangler = Mangler()
    mangler.main()
