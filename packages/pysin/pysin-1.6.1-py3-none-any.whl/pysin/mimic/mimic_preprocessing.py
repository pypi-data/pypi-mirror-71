import csv
import os
import re
import multiprocessing as mp
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from warnings import simplefilter

simplefilter("ignore")

MIMIC_FILES_DEFAULT_URL = "https://alpha.physionet.org/files/mimiciii-demo/1.4/"


class MimicPreprocessing:
    def __init__(self, dest_folder="data"):
        self.dest_folder = dest_folder
        if not os.path.isdir(dest_folder):
            os.mkdir(dest_folder)
            os.mkdir(f"{dest_folder}/csv")
            os.mkdir(f"{dest_folder}/csv_unique_values")

    def scraper(self, url=MIMIC_FILES_DEFAULT_URL, unused_tables=[]):

        print("Starts scraping mimic...")

        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, "html.parser")
        filename_list = [x.get("href") for x in soup.find_all("a")]
        print(filename_list)
        i = 0
        progress_files = tqdm(filename_list)
        for filename in progress_files:
            progress_files.set_description(f"Fetching {filename}...")
            if not filename.split(".csv")[0].lower() in unused_tables:

                if filename.endswith(".csv"):

                    resp = requests.get(url + filename)
                    with open(f"{self.dest_folder}/csv/{filename.lower()}", "w+") as f:
                        f.write(resp.text)

                i += 1

        print("\nScrapping terminated !\n")

    def infer_attributes(self):
        print("Starts inferring attributes from mimic...")

        attribute_types_all_tables = {}
        possible_values_all_tables = {}
        progress_files = tqdm(os.listdir(f"{self.dest_folder}/csv_unique_values"))
        for filename in progress_files:
            progress_files.set_description(f"Infering attributes from {filename}...")
            if filename.endswith(".csv"):

                attribute_types = {}
                possible_values = {}
                df = pd.read_csv(f"{self.dest_folder}/csv_unique_values/{filename}")
                df.columns = df.columns.str.lower()
                for attr in df.columns:
                    if (
                        False
                    ):  ############################################ TO FIX WHEN ATTRIBUTE TYPE DETECTION HAS BEEN SUFFICIENTLY IMPROVED (bad guessed type may lead to troubles with relations)
                        if re.match(r"^\d+$", attr_values[i]):
                            float_type = False
                            ev_digit_id_type = False
                            relative_float_type = False
                            length = len(attr_values[i])
                            is_field = False
                            for j in range(i + 1, len(attr_values)):
                                if attr_values[j] != "":
                                    if not re.match(r"^\d+$", attr_values[j]):
                                        if re.match(r"^\d+\.\d+$", attr_values[j]):
                                            float_type = True
                                        elif re.match(r"^-\d+\.?\d*$", attr_values[j]):
                                            relative_float_type = True
                                        elif re.match(r"^[EV]?\d+$", attr_values[j]):
                                            ev_digit_id_type = True
                                        else:
                                            attribute_types[attr] = f"field-{attr}"
                                            possible_values[f"{attr}"] = attr_values
                                            is_field = True
                                            break
                                    else:
                                        length = max(length, len(attr_values[j]))
                            if not is_field:
                                if ev_digit_id_type:
                                    attribute_types[attr] = f"ev_digit_id-"
                                elif relative_float_type:
                                    min_value = min([float(x) for x in attr_values if float(x) > 0])
                                    max_value = max([float(x) for x in attr_values if float(x) > 0])
                                    attribute_types[
                                        attr
                                    ] = f"relative_float-{min_value}-{max_value}"
                                elif float_type:
                                    min_value = min([float(x) for x in attr_values])
                                    max_value = max([float(x) for x in attr_values])
                                    attribute_types[attr] = f"float-{min_value}-{max_value}"
                                else:
                                    attribute_types[attr] = f"digit_id-{length}"
                        elif (
                            re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", attr_values[i],)
                            or attr_values[i] == "nan"
                        ):
                            is_field = False
                            for j in range(i + 1, len(attr_values)):
                                if attr_values[j] != "":
                                    if (
                                        not re.match(
                                            r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$",
                                            attr_values[j],
                                        )
                                        or attr_values[i] == "nan"
                                    ):
                                        attribute_types[attr] = f"field-{attr}"
                                        possible_values[f"{attr}"] = attr_values
                                        is_field = True
                                        break
                            if not is_field:
                                attribute_types[attr] = f"date-"
                        elif re.match(r"^\d+\.\d+$", attr_values[i]) or attr_values[i] == "nan":
                            relative_float_type = False
                            is_field = False
                            for j in range(i + 1, len(attr_values)):
                                if attr_values[j] != "":
                                    if (
                                        not re.match(r"^\d+\.?\d*$", attr_values[j])
                                        or attr_values[j] == "nan"
                                    ):
                                        if re.match(r"^-\d+\.?\d*$", attr_values[j]):
                                            relative_float_type = True
                                        else:
                                            attribute_types[attr] = f"field-{attr}"
                                            possible_values[f"{attr}"] = attr_values
                                            is_field = True
                                            break
                            if not is_field:
                                if relative_float_type:
                                    min_value = min([float(x) for x in attr_values if float(x) > 0])
                                    max_value = max([float(x) for x in attr_values if float(x) > 0])
                                    attribute_types[
                                        attr
                                    ] = f"relative_float-{min_value}-{max_value}"
                                else:
                                    min_value = min([float(x) for x in attr_values])
                                    max_value = max([float(x) for x in attr_values])
                                    attribute_types[attr] = f"float-{min_value}-{max_value}"
                        elif re.match(r"^-\d+\.?\d*$", attr_values[i]) or attr_values[i] == "nan":
                            is_field = False
                            for j in range(i + 1, len(attr_values)):
                                if attr_values[j] != "":
                                    if (
                                        not re.match(r"^-\d+\.?\d*$", attr_values[j])
                                        or attr_values[j] == "nan"
                                    ):
                                        attribute_types[attr] = f"field-{attr}"
                                        possible_values[
                                            f"{filename.split('.')[0]}-{attr}"
                                        ] = attr_values
                                        is_field = True
                                        break
                            if not is_field:
                                min_value = min(
                                    [abs(float(x)) for x in attr_values if float(x) > 0]
                                )
                                max_value = max([float(x) for x in attr_values if float(x) > 0])
                                attribute_types[attr] = f"relative_float-{min_value}-{max_value}"
                        elif re.match(r"^\d{5}-\d{5}$", attr_values[i]):
                            is_field = False
                            for j in range(i + 1, len(attr_values)):
                                if attr_values[j] != "":
                                    if not re.match(r"^\d{5}-\d{5}$", attr_values[j]):
                                        attribute_types[attr] = f"field-{attr}"
                                        possible_values[f"{attr}"] = attr_values
                                        is_field = True
                                        break
                            if not is_field:
                                attribute_types[attr] = f"double_digit_id-5"
                        elif re.match(r"^\d+-\d$", attr_values[i]) or attr_values[i] == "nan":
                            is_field = False
                            for j in range(i + 1, len(attr_values)):
                                if attr_values[j] != "":
                                    if (
                                        not re.match(r"^\d+-\d$", attr_values[j])
                                        or attr_values[j] == "nan"
                                    ):
                                        attribute_types[attr] = f"field-{attr}"
                                        possible_values[f"{attr}"] = attr_values
                                        is_field = True
                                        break
                            if not is_field:
                                attribute_types[attr] = f"composed_digit_id-"
                        elif re.match(r"^[EV]?\d+$", attr_values[i]):
                            is_field = False
                            for j in range(i + 1, len(attr_values)):
                                if attr_values[j] != "":
                                    if not re.match(r"^[EV]?\d+$", attr_values[j]):
                                        attribute_types[attr] = f"field-{attr}"
                                        possible_values[f"{attr}"] = attr_values
                                        is_field = True
                                        break
                            if not is_field:
                                attribute_types[attr] = f"ev_digit_id-"
                    else:
                        attribute_types[attr] = f"field-{attr}"
                        possible_values[f"{attr}"] = (
                            df[attr].dropna().reset_index(drop=True).map(str)
                        )

                attribute_types_all_tables[filename.split(".")[0].lower()] = attribute_types
                possible_values_all_tables[filename.split(".")[0].lower()] = possible_values

        print("\nInferring terminated !\n")
        return attribute_types_all_tables, possible_values_all_tables

    def compute_unique_values(self):
        print("Computing unique attribute values from mimic...")

        with mp.Pool(
            processes=mp.cpu_count()
        ) as pool:  # start as many worker processes as there are CPUs
            workers = pool.starmap_async(
                compute_csv_unique_values,
                [
                    (self.dest_folder, filename)
                    for filename in os.listdir(f"{self.dest_folder}/csv")
                ],
                callback=lambda result: print(f"computed unique values from {result}..."),
            )
            workers.wait()


def compute_csv_unique_values(dest_folder, filename, max_rows=10000000):
    print("processing", filename)
    if filename.endswith(".csv"):

        df = pd.read_csv(f"{dest_folder}/csv/{filename}", nrows=max_rows).applymap(str)
        unique_values = dict()
        for attr in df.columns:
            unique_values[attr] = df[attr].drop_duplicates().reset_index(drop=True)

        with open(f"{dest_folder}/csv_unique_values/{filename}", "w+") as f:
            writer = csv.writer(f)
            writer.writerow(unique_values.keys())
            max_len = max(len(unique_values[x]) for x in df.columns)
            i = 0
            while i < max_len:
                row = []
                for attr in df.columns:
                    values = unique_values[attr]
                    if i < len(values):
                        row.append(values[i])
                    else:
                        row.append("")
                writer.writerow(row)
                i += 1
    return filename
