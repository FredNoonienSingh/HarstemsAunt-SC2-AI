import os
import csv


class Utils:
    """Utils for Benchmarking"""

    @staticmethod
    def write_dict_to_csv(data_dict:dict, csv_filename:str) ->None:
        """
        Appends a dictionary to a CSV file if it exists, otherwise creates a new CSV file.

        Args:
            data_dict (dict): The dictionary to write to the CSV file.
            csv_filename (str): The name of the CSV file.
        """
        fieldnames = list(data_dict.keys())

        file_exists = os.path.isfile(csv_filename)

        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()
            writer.writerow(data_dict)
