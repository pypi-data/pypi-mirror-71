import pandas as pd
from sqlalchemy import create_engine
import datetime
from random import randint
from pysin import prescription_generator, cr_generator
from tqdm import tqdm
import os

from pysin.mimic.database_generator import DataBaseRandomGenerator
from pysin.mimic.table import Table
from pysin.mimic.attribute import Attribute
from pysin.mimic.attribute_type import AttributeType, bool_random_generator
from pysin.mimic.attribute_type import (
    FirstNameAttr,
    LastNameAttr,
    CityAttr,
    PostalCodeAttr,
    StreetAddressAttr,
    IntegerAttr,
    FloatAttr,
    RelativeFloatAttr,
    BoolAttr,
    DigitIDAttr,
    DoubleDigitIDAttr,
    ComposedDigitIDAttr,
    EVDigitIDAttr,
    PhoneNumberAttr,
    DateAttr,
    PathAttr,
    TextAttr,
    FieldAttr,
)
from pysin.mimic.mimic_preprocessing import MimicPreprocessing, MIMIC_FILES_DEFAULT_URL

import argparse


def scrap():
    parser = argparse.ArgumentParser(description="Scrap MIMIC-III data from alpha.physionet.org")
    parser.add_argument(
        "--dest", required=True, type=str, help="the destination path of the scrapped files",
    )
    parser.add_argument(
        "--url",
        type=str,
        help="the url from where the files are scrapped",
        default=MIMIC_FILES_DEFAULT_URL,
    )
    args = parser.parse_args()

    mimic = MimicPreprocessing(args.dest)
    mimic.scraper(
        url=args.url,
        unused_tables=[
            "callout",
            "cptevents",
            "datetimeevents",
            "d_cpt",
            "inputevents_cv",
            "inputevents_mv",
            "noteevents",
            "outputevents",
            "procedureevents_mv",
        ],
    )


def preprocess():
    parser = argparse.ArgumentParser(
        description="Preprocess MIMIC-III CSV files to compute unique values"
    )
    parser.add_argument(
        "--data", required=True, type=str, help="the destination path of the computed files",
    )
    args = parser.parse_args()

    mimic = MimicPreprocessing(args.data)
    mimic.compute_unique_values()


def generate_database():
    parser = argparse.ArgumentParser(
        description="Populate a postgres database with synthetic medical data based on MIMIC-III"
    )
    parser.add_argument(
        "--data",
        required=True,
        type=str,
        help="the location of the scrapped files and unique values of MIMIC tables",
    )
    parser.add_argument(
        "--db",
        required=True,
        type=str,
        help="the database connexion string (eg: postgresql://user:passsword@host/database)",
    )
    parser.add_argument(
        "--translate",
        action="store_true",
        help="should the mimic database be translated into french",
    )
    parser.add_argument(
        "--rows", required=True, type=int, help="The number of rows to generate",
    )
    parser.add_argument(
        "--locale",
        default="fr_FR",
        type=str,
        help="The locale to use when generating data",
        # see available locales here (https://faker.readthedocs.io/en/master/locales.html)
    )

    args = parser.parse_args()

    mimic = MimicPreprocessing(args.data)

    print("Connecting to postgres...")
    engine = create_engine(args.db)
    connection = engine.connect()
    print("OK")

    attributes_dict, possible_values = mimic.infer_attributes()

    unused_attributes = [  # (table_name, attribute_name)
        ("d_items", "dbsource"),
        ("icustays", "dbsource"),
        ("icustays", "first_wardid"),
        ("icustays", "last_wardid"),
        ("transfers", "dbsource"),
        ("transfers", "prev_wardid"),
        ("transfers", "curr_wardid"),
        ("admissions", "admittime"),
        ("admissions", "dischtime"),
        ("admissions", "deathtime"),
        ("patients", "dob"),
        ("patients", "dod"),
    ]

    tables_to_add = [
        "hospit_services",
        "documents",
    ]

    attributes_to_add = {  # (table_name, Attribute)
        "patients": [
            ("first_name", Attribute(FirstNameAttr)),
            ("last_name", Attribute(LastNameAttr)),
            ("weight", Attribute(IntegerAttr, min_val=40, max_val=110)),
            ("height", Attribute(IntegerAttr, min_val=130, max_val=210)),
            ("street_address", Attribute(StreetAddressAttr)),
            ("postal_code", Attribute(PostalCodeAttr)),
            ("city", Attribute(CityAttr)),
            ("phone", Attribute(PhoneNumberAttr)),
            ("dob", Attribute(DateAttr, start_date="-90y")),
            ("dod", Attribute(DateAttr)),
        ],
        "documents": [
            ("date", Attribute(DateAttr)),
            ("type", Attribute(FieldAttr, possible_values=["prescription", "report"])),
            ("description", Attribute(FieldAttr, possible_values=["discharge prescription and report", "entry prescription and report", "hospitalization report", "surgery report"])),  # TODO
            (
                "patient_id",
                Attribute(FieldAttr, possible_values=possible_values["patients"]["subject_id"]),
            ),
            ("statut", Attribute(BoolAttr, proba_true=0.9),),
            ("document", Attribute(PathAttr, file_type="pdf"),),
            ("doc_id", Attribute(DigitIDAttr)),
            (
                "hadm_id",
                Attribute(FieldAttr, possible_values=possible_values["admissions"]["hadm_id"]),
            ),
            ("cgid", Attribute(FieldAttr, possible_values=possible_values["caregivers"]["cgid"]),),
            ("nda", Attribute(BoolAttr, proba_true=0.5)),
        ],
        "hospit_services": [
            ("row_id", Attribute(DigitIDAttr)),
            (
                "careunit",
                Attribute(FieldAttr, possible_values=possible_values["services"]["curr_service"],),
            ),
        ],
        "caregivers": [
            ("first_name", Attribute(FirstNameAttr)),
            ("last_name", Attribute(LastNameAttr)),
        ],
        "admissions": [
            ("admittime", Attribute(DateAttr, start_date="-20y")),
            ("dischtime", Attribute(DateAttr)),
            ("deathtime", Attribute(DateAttr)),
        ],
        "diagnoses_icd": [
            ("date", Attribute(DateAttr, start_date="-20y")),
        ]

    }

    attributes_to_translate = [  # (table_name, attr_name)
        ("admissions", "diagnosis"),
        ("drgcodes", "description"),
        ("d_icd_diagnoses", "short_title"),
        ("d_icd_diagnoses", "long_title"),
        ("d_icd_procedures", "short_title"),
        ("d_icd_procedures", "long_title"),
    ]

    tables = {}

    for table in tables_to_add:
        attributes_dict[table] = {}
    for curr_table in attributes_dict:
        curr_attributes = {}
        for attr, attr_class in attributes_dict[curr_table].items():
            if not (curr_table, attr) in unused_attributes:
                try:
                    attr_type, attr_params = attr_class.split("-", 1)
                except:
                    raise Exception(f"Wrong attribute class format : {attr_class}.")
                if attr_type == "digit_id":
                    curr_attributes[attr] = Attribute(DigitIDAttr, length=int(attr_params))
                elif attr_type == "date":
                    curr_attributes[attr] = Attribute(DateAttr)
                elif attr_type == "float":
                    min_val, max_val = attr_params.split("-")
                    curr_attributes[attr] = Attribute(
                        FloatAttr, min_val=float(min_val), max_val=float(max_val)
                    )
                elif attr_type == "relative_float":
                    min_val, max_val = attr_params.split("-")
                    curr_attributes[attr] = Attribute(
                        RelativeFloatAttr, min_val=float(min_val), max_val=float(max_val),
                    )
                elif attr_type == "bool":
                    curr_attributes[attr] = Attribute(BoolAttr, proba_true=float(attr_params),)
                elif attr_type == "double_digit_id":
                    curr_attributes[attr] = Attribute(DoubleDigitIDAttr, length=int(attr_params))
                elif attr_type == "composed_digit_id-":
                    curr_attributes[attr] = Attribute(ComposedDigitIDAttr)
                elif attr_type == "first_name":
                    curr_attributes[attr] = Attribute(FirstNameAttr)
                elif attr_type == "last_name":
                    curr_attributes[attr] = Attribute(LastNameAttr)
                elif attr_type == "city_name":
                    curr_attributes[attr] = Attribute(CityAttr)
                elif attr_type == "postal_code":
                    curr_attributes[attr] = Attribute(PostalCodeAttr)
                elif attr_type == "phone_number":
                    curr_attributes[attr] = Attribute(PhoneNumberAttr)
                elif attr_type == "ev_digit_id":
                    curr_attributes[attr] = Attribute(EVDigitIDAttr, digit_length=attr_params)
                elif attr_type == "field":
                    curr_attributes[attr] = Attribute(
                        FieldAttr, possible_values=possible_values[curr_table][attr_params],
                    )
                else:
                    raise Exception(f"Unknow attribute type : {attr_type}.")
                tables[curr_table.split(".")[0]] = Table(curr_attributes)
                try:
                    attr_type, attr_params = attr_class.split("-", 1)
                except:
                    raise Exception(f"Wrong attribute class format : {attr_class}.")
        if curr_table in attributes_to_add.keys():
            for attr_name, attr in attributes_to_add[curr_table]:
                curr_attributes[attr_name] = attr
        tables[curr_table.split(".")[0]] = Table(curr_attributes)

    print(f"Translation is {'enabled' if args.translate else 'disabled'}")
    for table_name, attr_name in attributes_to_translate:
        tables[table_name].attributes[attr_name].translation_required = args.translate

    relations = {
        "hadm_id": {
            "parents": [("admissions", "hadm_id"),],
            "children": [
                ("chartevents", "hadm_id", (1, 2)),
                # ('datetimeevents', 'hadm_id', (1, 2)),
                ("diagnoses_icd", "hadm_id", (1, 2)),
                ("drgcodes", "hadm_id", (1, 2)),
                ("icustays", "hadm_id", (1, 2)),
                ("procedures_icd", "hadm_id", (1, 2)),
                ("services", "hadm_id", (1, 1)),
                ("documents", "hadm_id", (1, 2)),
                ("transfers", "hadm_id", (1, 2)),
                ("prescriptions", "hadm_id", (1, 2)),
                ("labevents", "hadm_id", (1, 2)),
                ("microbiologyevents", "hadm_id", (1, 2)),
            ],
        },
        "subject_id": {
            "parents": [("patients", "subject_id"),],
            "children": [
                ("admissions", "subject_id", (1, 2)),
                ("chartevents", "subject_id", (1, 2)),
                # ('datetimeevents', 'subject_id', (1, 2)),
                ("diagnoses_icd", "subject_id", (1, 2)),
                ("drgcodes", "subject_id", (1, 2)),
                ("icustays", "subject_id", (1, 2)),
                ("procedures_icd", "subject_id", (1, 2)),
                ("services", "subject_id", (1, 1)),
                ("transfers", "subject_id", (1, 2)),
                ("prescriptions", "subject_id", (1, 2)),
                ("labevents", "subject_id", (1, 2)),
                ("microbiologyevents", "subject_id", (1, 2)),
                ("documents", "patient_id", (1, 2)),
            ],
        },
        "cgid": {
            "parents": [("caregivers", "cgid"),],
            "children": [
                ("chartevents", "cgid", (1, 2)),
                # ('datetimeevents', 'cgid', (1, 2)),
                ("documents", "cgid", (1, 2)),
            ],
        },
        "icustay_id": {
            "parents": [("icustays", "icustay_id"),],
            "children": [
                ("chartevents", "icustay_id", (0, 2)),
                # ('datetimeevents', 'icustay_id', (1, 2)),
                ("transfers", "icustay_id", (1, 2)),
                ("prescriptions", "icustay_id", (1, 2)),
            ],
        },
        "itemid": {
            "parents": [("d_items", "itemid"),],
            "children": [
                ("chartevents", "itemid", (1, 2)),
                # ('datetimeevents', 'itemid', (1, 2)),
                ("microbiologyevents", "spec_itemid", (1, 2)),
                ("microbiologyevents", "org_itemid", (1, 2)),
                ("microbiologyevents", "ab_itemid", (1, 2)),
            ],
        },
        "icd9_code_diagnoses": {
            "parents": [("d_icd_diagnoses", "icd9_code"),],
            "children": [("diagnoses_icd", "icd9_code", (1, 2)),],
        },
        "icd9_code_procedures": {
            "parents": [("d_icd_procedures", "icd9_code"),],
            "children": [("procedures_icd", "icd9_code", (1, 2)),],
        },
        "itemid_lab": {
            "parents": [("d_labitems", "itemid"),],
            "children": [("labevents", "itemid", (1, 2)), ],
        },
        "service": {
            "parents": [("hospit_services", "careunit")],
            "children": [
                ("icustays", "first_careunit", (1, 2)),
                ("icustays", "last_careunit", (1, 2)),
                ("services", "prev_service", (1, 2)),
                ("services", "curr_service", (1, 2)),
                ("transfers", "prev_careunit", (1, 2)),
                ("transfers", "curr_careunit", (1, 2)),
            ],
        },
    }

    db_gen = DataBaseRandomGenerator(locale=args.locale, translation_enabled=args.translate)

    for table_name, table in tables.items():
        db_gen.add_table(table_name, table)

    for relation_name, relation_dict in relations.items():
        db_gen.add_relation(relation_name, relation_dict)

    db_gen.random_generation(min_rows=args.rows, max_card=5)

    for table_name, table in tqdm(tables.items(), desc="Uploading to postgres"):
        db_gen.tables[table_name].to_sql(table_name, engine)


def generate_pdf():
    parser = argparse.ArgumentParser(
        description="Generates prescriptions PDF based on a postgres MIMIC database"
    )
    parser.add_argument(
        "--db",
        required=True,
        type=str,
        help="the database connexion string (eg: postgresql://user:passsword@host/database)",
    )
    parser.add_argument(
        "--dest",
        required=True,
        type=str,
        help="Folder to use to write pdf"
    )
    parser.add_argument(
        "--locale",
        default="fr_FR",
        type=str,
        help="The locale to use when generating data",
        # see available locales here (https://faker.readthedocs.io/en/master/locales.html)
    )

    args = parser.parse_args()

    dest_dir = args.dest
    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)

    print("Connecting to postgres...")
    engine = create_engine(args.db)
    connection = engine.connect()
    print("OK")

    result = connection.execute(
        """SELECT
            caregivers.first_name AS doctor_first_name,
            caregivers.last_name AS doctor_last_name,
            patients.first_name AS patient_first_name,
            patients.last_name AS patient_last_name,
            patients.dob AS patient_birth_date,
            patients.weight AS patient_weight,
            d_icd_diagnoses.short_title AS diagnoses_st,
            d_icd_diagnoses.long_title AS diagnoses_lt,
            documents.document as path,
            documents.type as type,
            documents.hadm_id as hadm_id
        FROM documents
        JOIN caregivers ON documents.cgid = caregivers.cgid
        JOIN patients ON documents.patient_id = patients.subject_id
        JOIN diagnoses_icd ON documents.patient_id = diagnoses_icd.subject_id JOIN d_icd_diagnoses ON diagnoses_icd.icd9_code = d_icd_diagnoses.icd9_code"""
    )

    for row in tqdm(result, desc="Generating PDF prescriptions from database"):
        doc_date_result = connection.execute(
            f"""SELECT startdate as doc_date FROM prescriptions WHERE hadm_id LIKE '{row['hadm_id']}'"""
        )
        for date in doc_date_result:
            doc_date = datetime.datetime.strptime(date["doc_date"], "%Y-%m-%d %H:%M:%S")
            patient_birth_date = datetime.datetime.strptime(
                row["patient_birth_date"], "%Y-%m-%d %H:%M:%S"
            )
            patient_age = (
                doc_date.year
                - patient_birth_date.year
                - (
                    (doc_date.month, doc_date.day)
                    < (patient_birth_date.month, patient_birth_date.day)
                )
            )
            medication_result = connection.execute(
                f"""SELECT
                        drug as name,
                        prod_strength as dose,
                        dose_val_rx as poso_qty,
                        dose_unit_rx as poso_type
                    FROM
                        prescriptions
                    WHERE
                        hadm_id LIKE '{row['hadm_id']}' AND startdate LIKE '{doc_date}'
                """
            )
            medication = []
            for medic in medication_result:
                medication.append(
                    {
                        "name": medic["name"],
                        "dose": medic["dose"],
                        "poso_qty": medic["poso_qty"],
                        "poso_type": medic["poso_type"],
                    }
                )
        if row["type"] == "prescription":
            prescription_generator(
                os.path.join(dest_dir, row["path"]),
                locale=args.locale,
                doc_attributes={"date": doc_date.strftime("%d/%m/%Y")},
                doctor={
                    "first_name": row["doctor_first_name"],
                    "last_name": row["doctor_last_name"],
                },
                patient={
                    "first_name": row["patient_first_name"],
                    "last_name": row["patient_last_name"],
                    "age": patient_age,
                    "weight": row["patient_weight"],
                },
                medication=medication,
            )
        elif row["type"] == "report":
            cr_generator(
                os.path.join(dest_dir, row["path"]),
                locale=args.locale,
                doctor={
                    "first_name": row["doctor_first_name"],
                    "last_name": row["doctor_last_name"],
                },
                patient={
                    "first_name": row["patient_first_name"],
                    "last_name": row["patient_last_name"],
                    "age": patient_age,
                    "weight": row["patient_weight"],
                },
                hospitalization={
                    "reason": row["diagnoses_st"],
                    "hospitalization": row["diagnoses_lt"],
                },
                date={
                    "last_date": doc_date.strftime("%d/%m/%Y"),
                    "first_date": (doc_date - datetime.timedelta(days=randint(0, 16))).strftime(
                        "%d/%m/%Y"
                    ),
                    "birth_date": patient_birth_date,
                },
                medication=medication,
            )
