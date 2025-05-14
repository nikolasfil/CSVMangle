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

        new_path_properties = Path(
            self.folder_out, f"{file_path.name.strip('.csv')}-properties.csv"
        )
        with open(new_path_properties, "w") as file:
            for i in range(33):
                file.write(lines[i])

        new_path_csv = Path(self.folder_out, f"{file_path.name.strip('.csv')}-csv.csv")
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

    def list_data_contents(self, folder_path, save=False):

        output = []

        if not folder_path.exists():
            print(f"The folder {folder_path} does not exist.")
            return

        for item in sorted(folder_path.iterdir()):
            if item.is_dir():
                print(f"Directory: {item.name}")
                for sub_item in item.iterdir():
                    if sub_item.is_file():
                        print(f"File: {sub_item.name}")
                        self.split_file(sub_item)

            elif item.is_file():
                print(f"Item: {item.name}")
                if save:
                    output.append(f"Item: {item.name}")
                if "-properties" in item.name:
                    max_height = self.read_max_height(item)
                    print(f"Max height: {max_height}")
                    if save:
                        output.append(f"Max height: {max_height}")

                elif "-csv" in item.name:

                    # print(f"File: {item.name}")
                    df = self.read_csv(item)
                    df["Brd Reslt"] = pandas.to_numeric(
                        df["Brd Reslt"], errors="coerce"
                    )
                    # Calculate and print the mean (μέση τιμή)
                    mean_value = df["Brd Reslt"].mean()
                    print(f"Μέση τιμή (mean) της στήλης 'Brd Reslt': {mean_value:.2f}")
                    if save:
                        output.append(
                            f"Μέση τιμή (mean) της στήλης 'Brd Reslt': {mean_value:.2f}"
                        )

        if save:
            # Save the output to a text file
            output_file = Path(self.parent, "output.txt")
            with open(output_file, "w") as f:
                for line in output:
                    f.write(line + "\n")
            print(f"Output saved to {output_file}")

    def main(self):
        print("Formatting files")
        self.list_data_contents(self.folder_data)
        print("\n\n\nSplitting files\n\n\n")
        self.list_data_contents(self.folder_out, save=True)


if __name__ == "__main__":
    # Entry point for the script
    mangler = Mangler()
    mangler.main()
