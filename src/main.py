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
        """
        Splits a file into two separate files: one containing the first 33 lines
        (assumed to be properties) and the other containing the remaining lines
        (assumed to be CSV data).
        Args:
            file_path (str or Path): The path to the input file to be split.
        Creates:
            - A file named "<original_filename>-properties.csv" in the output folder,
              containing the first 33 lines of the input file.
            - A file named "<original_filename>-csv.csv" in the output folder,
              containing the remaining lines of the input file.
        Raises:
            FileNotFoundError: If the input file does not exist.
            IOError: If there is an issue reading from or writing to the files.
        """

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
        """
        Reads a CSV file into a pandas DataFrame, processes specific columns, and computes statistical values.
        Args:
            file_path (str): The path to the CSV file to be read.
        Returns:
            tuple: A tuple containing:
                - mean_value (float): The mean value of the "Brd Reslt" column after converting it to numeric.
                - max_value (float): The maximum value of the "Brd Load" column after converting it to numeric.
        Notes:
            - The CSV file is read with `skipinitialspace=True` and `encoding="latin-1"`.
            - Non-numeric values in the specified columns are coerced to NaN during conversion.
        """

        # Read a CSV file into a pandas DataFrame
        df = pandas.read_csv(file_path, skipinitialspace=True, encoding="latin-1")

        column_1 = "Brd Reslt"

        df[column_1] = pandas.to_numeric(df[column_1], errors="coerce")
        column_1_mean = df[column_1].mean()
        column_1_max = df[column_1].max()

        column_2 = "Brd Load"
        df[column_2] = pandas.to_numeric(df[column_2], errors="coerce")
        column_2_max = df[column_2].max()
        column_2_mean = df[column_2].mean()

        return (
            column_1,
            column_1_mean,
            column_1_max,
            column_2,
            column_2_mean,
            column_2_max,
        )

    def read_max_property(self, file_path, property="Max Broadband Resultant  : "):
        """
        Reads a specific property value from a text file.
        This method searches for a line in the file that contains the specified
        property string and extracts the value following the property string.
        Args:
            file_path (str): The path to the text file to be read.
            property (str, optional): The property string to search for in the file.
            Defaults to "Max Broadband Resultant  : ".
        Returns:
            str: The value associated with the specified property in the file,
            or None if the property is not found.
        """

        with open(file_path, "r") as file:
            lines = file.readlines()

        for line in lines:
            if property in line:
                return line.split(property)[1]
        # return lines[line].split(property)[1]

    def iterate_directory(self, folder_path):
        """
        Iterates through the contents of a given directory and processes files.
        Args:
            folder_path (Path): The path to the folder to iterate through.
        Behavior:
            - Checks if the specified folder exists. If not, prints an error message and exits the function.
            - Iterates through the items in the folder in sorted order.
            - For each item:
                - If it is a directory, prints its name.
                - If it is a file within a directory, prints its name and processes it using the `split_file` method.
        Note:
            This method assumes that `folder_path` is a `Path` object from the `pathlib` module.
        """

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
        """
        Lists and processes the contents of a specified folder, extracting and displaying
        relevant information from files with specific naming patterns. Optionally, the output
        can be saved to a file.
        Args:
            folder_path (Path): The path to the folder containing the files to process.
            save (bool, optional): If True, the output will be saved to a file. Defaults to False.
        Returns:
            None
        Behavior:
            - Checks if the specified folder exists. If not, prints an error message and exits.
            - Iterates through the files in the folder, sorted by name.
            - For files containing "-properties" in their name:
            - Reads the maximum property value using the `read_max_property` method.
            - Prints and optionally saves the property value.
            - For files containing "-csv" in their name:
            - Extracts the item name by stripping specific substrings from the file name.
            - Prints and optionally saves the item name.
            - Reads the mean and maximum values of specific columns using the `read_csv` method.
            - Prints and optionally saves the mean and maximum values.
            - If `save` is True, saves the output to a file using the `save_output_to_file` method.
        Notes:
            - The column names and property string are hardcoded as "Brd Reslt", "Brd Load",
              and "Max Broadband Resultant  : ", respectively.
            - The method assumes the presence of helper methods `read_max_property`,
              `read_csv`, `print_save`, and `save_output_to_file` within the same class.
        """

        output_list = []
        column_mean = "Brd Reslt"
        column_max = "Brd Load"
        property = "Max Broadband Resultant  : "

        if not folder_path.exists():
            print(f"The folder {folder_path} does not exist.")
            return

        for item in sorted(folder_path.iterdir()):

            if item.is_file():
                # Used for creating the output

                if "-properties" in item.name:

                    max_height = self.read_max_property(item, property=property)

                    self.print_save(
                        f"{property} {max_height}",
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

                    # mean_value, max_value
                    (
                        column_1,
                        column_1_mean,
                        column_1_max,
                        column_2,
                        column_2_mean,
                        column_2_max,
                    ) = self.read_csv(item)

                    self.print_save(
                        f"Μέση τιμή (mean) της στήλης {column_1}: {column_1_mean}",
                        lst=output_list,
                        save=save,
                    )

                    self.print_save(
                        f"Μαξ τιμή (max) της στήλης {column_1}: {column_1_max}",
                        lst=output_list,
                        save=save,
                    )

                    self.print_save(
                        f"Μέση τιμή (mean) της στήλης {column_2}: {column_2_mean}",
                        lst=output_list,
                        save=save,
                    )

                    self.print_save(
                        f"Μαξ τιμή (max) της στήλης {column_2}: {column_2_max}",
                        lst=output_list,
                        save=save,
                    )

        if save:
            self.save_output_to_file(output_list)

    def print_save(self, result, lst=None, save=False):
        """
        Prints a result and optionally saves it to a list.
        Args:
            result (Any): The result to be printed and optionally saved.
            lst (list, optional): The list to which the result will be appended if `save` is True. Defaults to None.
            save (bool, optional): If True, appends the result to the provided list. Defaults to False.
        Raises:
            AttributeError: If `save` is True and `lst` is not provided or is not a list.
        """

        if save:
            lst.append(result)
        print(result)

    def save_output_to_file(self, output_list):
        """
        Saves the provided list of output strings to a text file named 'output.txt'
        in the parent directory.
        Args:
            output_list (list of str): A list of strings to be written to the file.
        Returns:
            None
        Side Effects:
            - Writes the contents of `output_list` to a file named 'output.txt'.
            - Prints a message indicating the file's location.
        """

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
    mangler = Mangler()
    mangler.main()
