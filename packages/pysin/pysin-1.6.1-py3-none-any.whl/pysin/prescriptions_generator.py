import os
from fpdf import FPDF
from faker import Factory
from random import randint, choice
import pandas as pd
from unidecode import unidecode
from path import Path
from warnings import simplefilter
from datetime import datetime, timedelta

simplefilter("ignore")

MEDIC = [
    "DOLIPRANE",
    "DAFALGAN",
    "IMODIUM",
    "SPASFON",
    "TAHOR",
    "SPEDIFEN",
    "VOLTARENE",
    "ELUDRIL",
    "IXPRIM",
    "PARACETAMOL BIOGARAN",
    "FORLAX",
    "MAGNE B6",
    "HELICIDINE",
    "CLAMOXYL",
    "PIASCLEDINE",
    "LAMALINE",
    "GAVISCON",
    "DAFLON",
    "ANTARENE",
    "RHINOFLUIMUCIL",
    "PLAVIX",
    "MOPRAL",
    "SUBUTEX",
    "AERIUS",
    "ORELOX",
    "INEXIUM",
    "METEOSPASMYL",
    "AUGMENTIN",
    "TOPLEXIL",
    "PIVALONE",
    "VASTAREL",
    "ADVIL",
    "EUPANTOL",
    "DEXERYL",
    "RENUTRYL 500",
    "XANAX",
    "EMLAPATCH",
    "LASILIX",
    "ENDOTELON",
    "DEROXAT",
    "TEMESTA",
    "EFFEXOR",
    "PARACETAMOL SANDOZ",
    "VENTOLINE",
    "SOLUPRED",
    "DEXTROPROPOXYPHENE PARAC BIOG",
    "PNEUMOREL",
    "INIPOMP",
    "PREVISCAN",
    "ASPEGIC",
    "GINKOR",
    "CRESTOR",
    "MEDIATOR",
    "SERESTA",
    "MOTILIUM",
    "PARACETAMOL MERCK",
    "CELESTENE",
    "AMLOR",
    "DIAMICRON",
    "TANAKAN",
    "ATARAX",
    "DERINOX",
    "XYZALL",
    "DEXTROPROPOXYPHENE PARAC SAND",
    "SERETIDE",
    "COVERSYL",
    "PROPOFAN",
    "HEXAQUINE",
    "APROVEL",
    "PARIET",
    "ZALDIAR",
    "DIPROSONE",
    "PARACETAMOL TEVA",
    "BETADINE",
    "LYSANXIA",
    "ALODONT",
    "LEXOMIL",
    "DACRYOSERUM",
    "FUCIDINE",
    "STILNOX",
    "KETUM",
    "STABLON",
    "ART",
    "BIOCALYPTOL",
    "THIOVALONE",
    "DEBRIDAT",
    "PYOSTACINE",
    "TIORFAN",
    "SPECIAFOLDINE",
    "OGAST",
    "RIVOTRIL",
    "TOPALGIC",
    "NASONEX",
]

POSO_TYPE = ["cp", "injections", "comprimés"]

POSO_FREQ = [
    "le matin",
    "le soir",
    "matin, midi et soir",
    "avant les repas",
    "après les repas",
    "par jour",
]

POSO_DURATION = [f"pendant {n} jours" for n in {3, 5, 7, 10, 15, 30}] + ["si douleur"]

MONTHS = [
    "janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre",
]

HOSP = [["ischémie de main droite","L intervention a consisté en une ligature de l artère radiale distale" ],
             ["urétéroscopie","Simples, Ablation de la sonde vésicale à J1. Reprise mictionnelle satisfaisante autorisant la sortie"],
             ["superficialisation","L intervention a consisté en une superficialisation de veine radiale droite."],
             ["création d un abord vasculaire","L intervention a consisté en la création d une fistule radio céphalique gauche"],
             ["PUC GENOU GAUCHE", "PUC Genou Gauche sous AG. Suites simples"],
             ["fermeture exérèse d un abord vasculaire", "L intervention a consisté en une fermeture exérèse de l abord vasculaire"],
             ["Hydrocèle scrotale gauche", "Augmentation du volume de la bourse gauche ,  confirmé en échographie"],
             ["coronarographie de contrôle","La coronarographie réalisée par voie radiale droite retrouve une bonne perméabilité des stents IVA et circonflexe"],
             ["coronarographie diagnostique", "La coronarographie retrouve une atteinte coronaire tri tronculaire"],
             ["tentative de désobstruction IVA","La procédure a consisté en une tentative de recanalisation de l IVA avec échec"],
             ["pontage aorto coronaire", "L intervention consiste en un double pontage IVA"],
             ["artériographie des membres inférieurs", "L artériographie retrouve une arthrite distale sévère"],
             ["faux anévrisme de l aorte ascendante", "Le suivi scanographique a montré l apparition d un aspect d un double faux anévrisme de l aorte initiale"]]

ANT = ["fumeur",
       "hypertension artérielle",
       "hypercholestérolémie",
       "diabète",
       "diabète de type 2",
       "obésité",
       "Tabac/PA",
        "Insuffisance rénale chronique",
        "Surpoids",
        "Pas d’allergie"]

FONTS_FOLDER_PATH = Path(os.path.dirname(__file__)) / "utils/fonts/"

SIGNATURE_FONTS = [
    FONTS_FOLDER_PATH / name
    for name in os.listdir(FONTS_FOLDER_PATH)
    if name.endswith(".ttf")
]

MAIN_FONTS = ["Arial", "Courier", "Helvetica", "Times"]


def add_block(pdf, txt, align="L"):
    """Adds paragraph to the pdf object

    Arguments:
        pdf {fpdf.fpdf.FPDF} -- current pdf object
        txt {str} -- paragraph to add

    Keyword Arguments:
        align {str} -- text alignment : the possible values are "L", "C" and "R" (default: {"L"})
    """
    txt = unidecode(txt)
    for row in txt.split("\n"):
        pdf.cell(200, 5, txt=row, ln=1, align=align)


def signature(name):
    """Creates a fake signature

    Arguments:
        name {str} -- person name

    Returns:
        str -- signature
    """

    name_list = name.split(" ")
    sign = ""
    for w in name_list[:-1]:
        if randint(0, 1):
            if randint(0, 1):
                sign += w[0]
            else:
                sign += w
            if randint(0, 1):
                sign += " "
    sign += name_list[-1]
    return sign


def prescription_generator(output_path, locale="fr_FR", **kwargs):
    """Generates a fake medical prescription

    Arguments:
        output_path {Path} -- path the ouput pdf file
        patient_name {str} -- patient name to use
        year {int} -- year of the prescription
    """

    fake = Factory.create(locale)
    pdf = FPDF(format="A4")
    pdf.add_page()
    font = choice(MAIN_FONTS)
    pdf.set_font(font, size=11)

    # Arguments processing

    try:
        nb_medics = len(kwargs["medication"])
    except KeyError:
        nb_medics = randint(1, 5)

    field_group_values = {
        "doc_attributes": {"city": fake.city(), "date": fake.date(pattern="%d/%m/%Y"),},
        "medical_centre": {
            "city": fake.city(),
            "street_address": fake.street_address(),
            "postal_code": randint(1000, 10000) * 10,
            "phone_number": fake.phone_number(),
        },
        "doctor": {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "street_address": fake.street_address(),
            "postal_code": randint(1000, 10000) * 10,
            "city": fake.city(),
            "phone_number": fake.phone_number(),
        },
        "patient": {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "age": randint(10, 100),
            "weight": randint(30, 110),
        },
        "medication": [],
    }

    for _ in range(nb_medics):
        field_group_values["medication"].append(
            {
                "name": choice(MEDIC),
                "dose": 5 * randint(1, 10),
                "poso_qty": randint(1, 3),
                "poso_type": choice(POSO_TYPE),
                "poso_freq": choice(POSO_FREQ),
                "poso_duration": choice(POSO_DURATION),
            }
        )

    for group_name in {"doc_attributes", "medical_centre", "doctor", "patient"}:
        for field_name in field_group_values[group_name]:
            try:
                field_group_values[group_name][field_name] = kwargs[group_name][
                    field_name
                ]
            except KeyError:
                pass

    if "medication" in kwargs.keys():
        for i in range(nb_medics):
            for field_name in field_group_values["medication"][i]:
                try:
                    field_group_values["medication"][i][field_name] = kwargs[
                        "medication"
                    ][i][field_name]
                except KeyError:
                    pass

    for group_name, group_values in kwargs.items():
        if not group_name in field_group_values:
            print(f"Attributes group '{group_name}' is not recognized.")
        elif group_name in {"doc_attributes", "medical_centre", "doctor", "patient"}:
            for field_name in group_values.keys():
                if not field_name in field_group_values[group_name]:
                    print(
                        f"Attribute '{field_name}' from group '{group_name}' is not recognized."
                    )
        else:
            assert group_name == "medication", f"Unexpected argument."
            assert (
                type(kwargs["medication"]) == list
            ), f"Wrong argument type : 'medication' argument must be a list of dictionnaries."
            for i in range(nb_medics):
                for field_name in kwargs["medication"][i].keys():
                    if not field_name in field_group_values["medication"][i].keys():
                        print(
                            f"Attribute '{field_name}' from medication #{i} is not recognized."
                        )

    # En-tête

    txt = f"""À {field_group_values["doc_attributes"]["city"]}, le {field_group_values["doc_attributes"]["date"]}     
    
    
    
    """
    add_block(pdf, txt, align="R")

    # Centre médical

    txt = f"""
Centre Médical de {field_group_values["medical_centre"]["city"]}
{field_group_values["medical_centre"]["street_address"]}
{field_group_values["medical_centre"]["postal_code"]} {field_group_values["medical_centre"]["city"]}
{field_group_values["medical_centre"]["phone_number"]}


"""
    pdf.set_font(font, "B", size=11)
    add_block(pdf, txt, align="C")
    pdf.set_font(font, size=11)

    # Docteur

    txt = f"""
        Docteur {field_group_values["doctor"]["last_name"]}
        {field_group_values["doctor"]["street_address"]}
        {field_group_values["doctor"]["postal_code"]} {field_group_values["doctor"]["city"]}
        Tél. : {field_group_values["doctor"]["phone_number"]}

"""
    add_block(pdf, txt)

    # Patient

    txt = f"""
        {field_group_values["patient"]["first_name"]} {field_group_values["patient"]["last_name"]}
        {field_group_values["patient"]["age"]} ans, {field_group_values["patient"]["weight"]} kg

    """

    add_block(pdf, txt)

    # Prescription

    for i in range(nb_medics):

        txt = f"""
        {field_group_values["medication"][i]["name"]} {field_group_values["medication"][i]["dose"]}"""

        pdf.set_font(font, "B", size=11)
        add_block(pdf, txt)

        txt = f"""          {field_group_values["medication"][i]["poso_qty"]} {field_group_values["medication"][i]["poso_type"]} {field_group_values["medication"][i]["poso_freq"]} {field_group_values["medication"][i]["poso_duration"]}
"""

        pdf.set_font(font, size=11)
        add_block(pdf, txt)

    # Signature

    font_size = randint(20, 40)
    pdf.set_font(font, "I", size=font_size)
    # pdf.add_font("Signature", "", choice(SIGNATURE_FONTS), uni=True)
    # pdf.set_font("Signature", size=font_size)

    txt = f"""


{signature(field_group_values["doctor"]['last_name'])}          {int((40 - font_size)/20) * randint(0, 20) * ' '}
"""
    add_block(pdf, txt, align="R")

    pdf.output(output_path)

def cr_generator(output_path, locale="fr_FR", **kwargs):
    """Generates a fake medical report

    Arguments:
        output_path {Path} -- path the ouput pdf file
        patient_name {str} -- patient name to use
        year {int} -- year of the prescription
    """
    fake = Factory.create(locale)
    pdf = FPDF(format="A4")
    pdf.add_page()
    font = choice(MAIN_FONTS)
    pdf.set_font(font, size=10)

    #Arguments processing

    try:
        nb_medics = len(kwargs["medication"])
    except KeyError:
        nb_medics = randint(1, 5)

    try:
        nb_ant = len(kwargs["antecedent"])
    except KeyError:
        nb_ant = randint(1, 3)

    choice_hospitalization = randint(0, len(HOSP)-1)
    last_date = fake.date_between()
    duration = randint(0,16)
    first_date = last_date - timedelta(days=duration)

    field_group_values = {
        "doc_attributes": {"city": fake.city(), "date": fake.date(pattern="%d/%m/%Y"),},
        "medical_centre": {
            "city": fake.city(),
            "street_address": fake.street_address(),
            "postal_code": randint(1000, 10000) * 10,
            "phone_number": fake.phone_number(),
        },
        "doctor": {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "street_address": fake.street_address(),
            "postal_code": randint(1000, 10000) * 10,
            "city": fake.city(),
            "phone_number": fake.phone_number(),
        },
        "patient": {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "age": randint(10, 100),
            "weight": randint(30, 110),
        },
        "hospitalization": {
            "reason": HOSP[choice_hospitalization][0],
            "hospitalization": HOSP[choice_hospitalization][1]
        },
        "date": {
            "last_date": last_date.strftime("%d/%m/%Y"),
            "first_date": first_date.strftime("%d/%m/%Y"),
            "birth_date": fake.date_between(start_date='-80y', end_date=first_date).strftime("%d/%m/%Y")
        },
        "medication": [],
        "antecedent": []
    }

    for _ in range(nb_medics):
        field_group_values["medication"].append(
            {
                "name": choice(MEDIC),
                "dose": 5 * randint(1, 10),
                "poso_qty": randint(1, 3),
                "poso_type": choice(POSO_TYPE),
                "poso_freq": choice(POSO_FREQ),
                "poso_duration": choice(POSO_DURATION),
            }
        )

    for _ in range(nb_ant):
        field_group_values["antecedent"].append(choice(ANT))

    for group_name in {'doc_attributes', 'medical_centre', 'doctor', 'patient', "hospitalization", "date"}:
        for field_name in field_group_values[group_name]:
            try:
                field_group_values[group_name][field_name] = kwargs[group_name][
                    field_name
                ]

            except KeyError:
                pass

    if "medication" in kwargs.keys():
        for i in range(nb_medics):
            for field_name in field_group_values["medication"][i]:
                try:
                    field_group_values["medication"][i][field_name] = kwargs[
                        "medication"
                    ][i][field_name]
                except KeyError:
                    pass
    if "antecedent" in kwargs.keys():
        for i in range(nb_ant):
            try:
                field_group_values["antecedent"][i] = kwargs["antecedent"][i]
            except:
                pass

    for group_name, group_values in kwargs.items():
        if not group_name in field_group_values:
            print(f"Attributes group '{group_name}' is not recognized.")
        elif group_name in {'doc_attributes', 'medical_centre', 'doctor', 'patient', 'date', 'hospitalization'}:
            for field_name in group_values.keys():
                if not field_name in field_group_values[group_name]:
                    print(
                        f"Attribute '{field_name}'' from group '{group_name}' is not recognized."
                    )
        elif group_name == 'antecedent':
            pass
        else:
            assert group_name == 'medication', f"Unexpected argument."
            assert type(kwargs[
                            "medication"]) == list, f"Wrong argument type : 'medication' argument must be a list of dictionnaries."
            for i in range(nb_medics):
                for field_name in kwargs["medication"][i].keys():
                    if not field_name in field_group_values['medication'][i].keys():
                        print(
                            f"Attribute '{field_name}' from medication #{i} is not recognized."
                        )

    # Centre médical

    txt = f"""
Centre Médical de {field_group_values["medical_centre"]["city"]}
{field_group_values["medical_centre"]["street_address"]}
{field_group_values["medical_centre"]["postal_code"]} {field_group_values["medical_centre"]["city"]}
{field_group_values["medical_centre"]["phone_number"]}


"""
    pdf.set_font(font, "B", size=11)
    add_block(pdf, txt, align="L")
    pdf.set_font(font, size=10)

    # Docteur

    doctor_name = fake.name()
    postal_code = randint(1000, 10000) * 10

    txt = f"""
Docteur {field_group_values["doctor"]["last_name"]}
{field_group_values["doctor"]["street_address"]}
{field_group_values["doctor"]["postal_code"]} {field_group_values["doctor"]["city"]}
Tél. : {field_group_values["doctor"]["phone_number"]}

"""
    add_block(pdf, txt)

    # Date
    txt = f"""À {field_group_values["medical_centre"]["city"]}, le {field_group_values["date"]["last_date"]}     

        """
    add_block(pdf, txt, align="R")

    #Objet
    txt = f"""Objet : Compte-rendu d'hospitalisation de {field_group_values["patient"]["first_name"]} {field_group_values["patient"]["last_name"]} du {field_group_values["date"]["first_date"]} au {field_group_values["date"]["last_date"]}

{field_group_values["patient"]["first_name"]} {field_group_values["patient"]["last_name"]} né le {field_group_values["date"]["birth_date"]} a été hospitalisé le {field_group_values["date"]["first_date"]} pour {field_group_values["hospitalization"]["reason"]}

"""
    add_block(pdf, txt, align="L")

    #Antécédents
    pdf.set_font(font, "B", size=10)
    txt = """
Antécédents
    """
    add_block(pdf, txt, align="L")
    pdf.set_font(font, size=10)
    for i in range(nb_ant):
        txt = f"""      {field_group_values["antecedent"][i]} """
        add_block(pdf, txt)

    #Hospitalisation
    pdf.set_font(font, "B", size=10)
    txt = """
Hospitalisation
    """
    add_block(pdf, txt, align="L")
    pdf.set_font(font, size=10)
    txt = f"""      {field_group_values["hospitalization"]["hospitalization"]}"""
    add_block(pdf, txt, align="L")

    #Traitement de sortie
    pdf.set_font(font, "B", size=10)
    txt = """
Traitement de sortie
    """
    add_block(pdf, txt, align="L")
    pdf.set_font(font, size=10)
    for i in range(nb_medics):
        txt = f"""
        {field_group_values["medication"][i]["name"]} {field_group_values["medication"][i]["dose"]} mg, {field_group_values["medication"][i]["poso_qty"]} {field_group_values["medication"][i]["poso_type"]} {field_group_values["medication"][i]["poso_freq"]} {field_group_values["medication"][i]["poso_duration"]}"""
    add_block(pdf, txt, align="L")
    # Signature
    font_size = randint(20, 40)
    pdf.set_font(font, "I", size=font_size)
    # pdf.add_font("Signature", "", choice(SIGNATURE_FONTS), uni=True)
    # pdf.set_font("Signature", size=font_size)

    txt = f"""
    {signature(field_group_values["doctor"]['last_name'])}          {int((40 - font_size) / 20) * randint(0, 20) * ' '}
    """
    add_block(pdf, txt, align="R")

    pdf.output(output_path)


def get_id():
    """Generates a random 6-digit id

    Returns:
        str -- random 6-digit id
    """

    return str(randint(1000, 100000)).zfill(6)


def generate(nb, output_path, locale="fr_FR"):
    """Generate several fake medical prescriptions

    Arguments:
        nb {int} -- number or fake medical prescriptions to generate
        output_path {str} -- folder to store the fake medical prescriptions in
    """
    fake = Factory.create(locale)
    output_path = Path(output_path)

    link = pd.DataFrame(
        columns=[
            "patient_id",
            "patient_surname",
            "patient_name",
            "date_folder",
            "prescription_id",
            "cr_id",
        ]
    )

    print("Generating data...")

    for i in range(nb):

        print(f"Loading : {int(100 * i / nb)} %", end="\r")

        patient_id = get_id()
        while not link[lambda row: row["patient_id"] == patient_id].empty:
            patient_id = get_id()

        prescription_id = get_id()
        while not link[lambda row: row["prescription_id"] == prescription_id].empty:
            prescription_id = get_id()

        cr_id = get_id()
        while not link[lambda row: row["prescription_id"] == prescription_id].empty:
            cr_id = get_id()

        patient_name = fake.first_name()
        patient_surname = fake.last_name()
        year = str(randint(2010, 2019))

        link = link.append(
            {
                "patient_id": patient_id,
                "patient_surname": patient_surname,
                "patient_name": patient_name,
                "date_folder": year,
                "prescription_id": prescription_id,
                "cr_id": cr_id,
            },
            ignore_index=True,
        )

        if not os.path.isdir(output_path / year):
            os.mkdir(output_path / year)

        prescription_generator(
            f"{output_path}/{year}/prescription_{prescription_id}.pdf",
            patient={"first_name": patient_name, "last_name": patient_surname},
            doc_attributes={"date": f"01/01/{year}"},
        )
        cr_generator(
            f"{output_path}/{year}/CR_{cr_id}.pdf",
            patient = {"first_name":patient_name, "last_name": patient_surname},
            doc_attributes={'date': f'01/01/{year}'},
        )

    link.to_csv(output_path / "index.csv")

    print("Generation terminated !")