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

        # Split the properties into one file
        new_path_properties = Path(
            self.folder_out, f"{file_path.name.strip('.csv')}-properties.csv"
        )
        with open(new_path_properties, "w") as file:
            for i in range(33):
                file.write(lines[i])

        # Split the CSV into another file
        new_path_csv = Path(self.folder_out, f"{file_path.name.strip('.csv')}-csv.csv")
        with open(new_path_csv, "w") as file:
            for i in range(33, len(lines)):
                file.write(lines[i])

    def read_csv(self, file_path):
        # Read a CSV file into a pandas DataFrame
        df = pandas.read_csv(file_path, skipinitialspace=True, encoding="latin-1")

        column_mean = "Brd Reslt"

        df[column_mean] = pandas.to_numeric(df[column_mean], errors="coerce")
        mean_value = df[column_mean].mean()

        column_max = "Brd Load"
        df[column_max] = pandas.to_numeric(df[column_max], errors="coerce")
        max_value = df[column_max].max()

        return mean_value, max_value

    def read_max_height(self, file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
        return lines[19].split("Max Broadband Resultant  : ")[1]

    def iterate_directory(self, folder_path):
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

    def list_data_contents(self, folder_path, save=False):
        output_list = []
        column_mean = "Brd Reslt"
        column_max = "Brd Load"

        if not folder_path.exists():
            print(f"The folder {folder_path} does not exist.")
            return

        for item in sorted(folder_path.iterdir()):

            if item.is_file():
                # Used for creating the output

                if "-properties" in item.name:

                    max_height = self.read_max_height(item)

                    self.print_save(
                        f"Max Broadband Resultant  : {max_height}",
                        lst=output_list,
                        save=save,
                    )

                elif "-csv" in item.name:

                    item_name = (
                        item.name.strip("-properties").strip("-csv").strip(".csv")
                    )

                    self.print_save(
                        f"Item: {item_name}",
                        lst=output_list,
                        save=save,
                    )

                    mean_value, max_value = self.read_csv(item)

                    self.print_save(
                        f"Μέση τιμή (mean) της στήλης {column_mean}: {mean_value}",
                        lst=output_list,
                        save=save,
                    )

                    self.print_save(
                        f"Peak της στήλης {column_max}: {max_value:.2f}",
                        lst=output_list,
                        save=save,
                    )

        if save:
            self.save_output_to_file(output_list)

    def print_save(self, result, lst=None, save=False):
        if save:
            lst.append(result)
        print(result)

    def save_output_to_file(self, output_list):
        # Save the output to a text file
        output_file = Path(self.parent, "output.txt")
        with open(output_file, "w") as f:
            for line in output_list:
                f.write(line + "\n")
        print(f"Output saved to {output_file}")

    def main(self):
        print("Formatting files")
        self.iterate_directory(self.folder_data)
        print("\n\n\nSplitting files\n\n\n")
        self.list_data_contents(self.folder_out, save=True)


if __name__ == "__main__":
    # Entry point for the script
    mangler = Mangler()
    mangler.main()
