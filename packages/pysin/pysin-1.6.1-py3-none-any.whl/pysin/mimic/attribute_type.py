from random import choice, randint, random
from unidecode import unidecode
import pandas as pd
import os
import html


class AttributeType:
    def __init__(self, type_name, random_generator):
        self.type_name = type_name
        self.random_generator = random_generator

    def get_random(self, fake_factory, translator, locale, **kwargs_for_random_generator):
        return self.random_generator(
            fake_factory, translator, locale, **kwargs_for_random_generator
        )


### Random generators


def first_name_random_generator(fake_factory, translator, locale, **kwargs):
    return fake_factory.first_name()


def last_name_random_generator(fake_factory, translator, locale, **kwargs):
    return fake_factory.last_name()


def signature_random_generator(*args, name=None, **kwargs):
    name_list = unidecode(name).split(" ")
    sign = ""
    for w in name_list[:-1]:
        if randint(0, 1):
            if randint(0, 1):
                sign += w[0]
            else:
                sign += w
            if randint(0, 1):
                sign += " "
    return sign + name_list[-1]


def city_random_generator(fake_factory, translator, locale, **kwargs):
    return fake_factory.city()


def postal_code_random_generator(*args, **kwargs):
    return randint(1000, 10000) * 10


def street_address_random_generator(fake_factory, translator, locale, **kwargs):
    return fake_factory.street_address()


def integer_random_generator(*args, min_val=0, max_val=1000, **kwargs):
    return randint(min_val, max_val)


def float_random_generator(*args, min_val=0, max_val=100, **kwargs):
    return min_val + random() * (max_val - min_val)


def relative_float_random_generator(*args, min_val=0, max_val=100, **kwargs):
    if randint(0, 1):
        return randint(-99, -1)
    return float_random_generator(*args, min_val=min_val, max_val=max_val, **kwargs)


def bool_random_generator(*args, proba_true=0.6, **kwargs):
    return random() < proba_true


def digitID_random_generator(*args, length=5, **kwargs):
    min_val = int(10 ** (length - 2))
    max_val = int(10 ** length - 1)
    return str(randint(min_val, max_val)).zfill(length)


def double_digitID_random_generator(*args, length=5, **kwargs):
    min_val = int(10 ** (length - 2))
    max_val = int(10 ** length - 1)
    return (
        str(randint(min_val, max_val)).zfill(length)
        + "-"
        + str(randint(min_val, max_val)).zfill(length)
    )


def EV_digitID_random_generator(*args, digit_length=5, **kwargs):
    return (
        str(choice(["E", "V"] + list(range(10))))
        + 3 * str(randint(0, 9))
        + str(choice([""] + list(range(10))))
    )


def composed_digitID_random_generator(*args, **kwargs):
    return str(randint(100, 99999)) + "-" + randint(0, 9)


def phone_number_random_generator(fake_factory, translator, locale, **kwargs):
    return fake_factory.numerify(choice([f"0{d} ## ## ## ##" for d in range(1, 8)]))


def date_random_generator(
    fake_factory,
    translator,
    locale,
    pattern="%Y-%m-%d %H:%M:%S",
    start_date="-10y",
    end_date="today",
    **kwargs,
):
    return fake_factory.date_between(start_date=start_date, end_date=end_date).strftime(pattern)


def path_random_generator(*args, prefix="", file_type="", **kwargs):
    return f"{prefix}{digitID_random_generator(length=15)}.{file_type}"

def text_random_generator(fake_factory, translator, locale, **kwargs):
    return fake_factory.sentence()


def field_random_generator(
    fake_factory, translator, locale, translation_required=False, possible_values=None, **kwargs,
):
    if len(possible_values) == 0:
        return ""

    txt = choice(possible_values)
    language = locale.split("_")[0]
    if language == "en" or translation_required == False:
        return txt
    else:
        if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ.keys():
            try:
                translated_txt = html.unescape(
                    translator.translate(txt, target_language=language)["translatedText"]
                )
                if translated_txt == txt:
                    print(f"A text has not been translated : {txt}")
                    return txt
                return translated_txt
            except:
                print(f"Used initial text because an error occurred while translating : {txt}.")
                return txt
        else:
            raise Exception("Environment variable GOOGLE_APPLICATION_CREDENTIALS not found.")


### Attribute types

FirstNameAttr = AttributeType("first_name", first_name_random_generator)
LastNameAttr = AttributeType("last_name", last_name_random_generator)

CityAttr = AttributeType("city", city_random_generator)
PostalCodeAttr = AttributeType("postal_code", postal_code_random_generator)
StreetAddressAttr = AttributeType("street_address", street_address_random_generator)

IntegerAttr = AttributeType("integer", integer_random_generator)
FloatAttr = AttributeType("float", float_random_generator)
RelativeFloatAttr = AttributeType("relative_float", relative_float_random_generator)
BoolAttr = AttributeType("bool_attr", bool_random_generator)

DigitIDAttr = AttributeType("digit_ID", digitID_random_generator)
DoubleDigitIDAttr = AttributeType("double_digitID", double_digitID_random_generator)
EVDigitIDAttr = AttributeType("EV_digitID", EV_digitID_random_generator)
ComposedDigitIDAttr = AttributeType("composed_digitID", composed_digitID_random_generator)

PhoneNumberAttr = AttributeType("phone_number", phone_number_random_generator)

DateAttr = AttributeType("date", date_random_generator)

PathAttr = AttributeType("path", path_random_generator)

TextAttr = AttributeType("text", text_random_generator)

FieldAttr = AttributeType("field", field_random_generator)
