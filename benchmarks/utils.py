from typing import Dict

import os
import csv
import json

import subprocess

from .common import logger

class Utils:
    """Utils for Benchmarking"""

    @staticmethod
    def read_json(path_to_file:str) -> Dict:
        """ reads json -> returns dict 

        Args:
            path_to_file (str): _description_

        Returns:
            Dict: _description_
        """
        try:
            with open(path_to_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            logger.error(f"can not load {path_to_file} -> FileNotFound")
            return None
        except json.JSONDecodeError:
            logger.error(f"can not load {path_to_file} -> JSONDecodeError")
            return None

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

    @staticmethod
    def get_git_head() -> str:
        """ Gets the git head to use a marker in Benchmarks"""
        try:
            process = subprocess.Popen(['git', 'rev-parse', 'HEAD'],\
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                print(f"Error getting Git HEAD: {stderr.decode()}")
                return None

            commit_hash = stdout.decode().strip()
            return commit_hash
        except FileNotFoundError:
            print("Git command not found. Make sure Git is installed and in your PATH.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    path:str = "benchmarks/configs/config.json"
    print(Utils.read_json(path))
