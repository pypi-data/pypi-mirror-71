from .attribute import Attribute
import pandas as pd


class Table:
    def __init__(self, attributes_dict):
        self.attributes = attributes_dict
        self.data = pd.DataFrame(columns=self.attributes.keys())

    def add_row(self, row_values):
        self.data = self.data.append(row_values, ignore_index=True)

    def get_random_row(self, fake_factory, translator, locale, fixed_values={}):
        row_values = {}
        for name, value in fixed_values.items():
            row_values[name] = value
        for name, attr in self.attributes.items():
            if not name in row_values.keys():
                row_values[name] = attr.get_random_value(fake_factory, translator, locale)
        return row_values

    def add_random_row(self, fake_factory, translator, locale, fixed_values={}):
        self.add_row(
            self.get_random_row(fake_factory, translator, locale, fixed_values=fixed_values)
        )

    def to_csv(self, output_path):
        self.data.to_csv(output_path, index=False)

    def to_sql(self, table_name, engine):
        self.data.to_sql(table_name, engine, index=False)

    def length(self):

        return len(self.data)
