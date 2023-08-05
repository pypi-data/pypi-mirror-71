from database_generator import DataBaseRandomGenerator
from table import Table
from attribute import Attribute
from attribute_type import FirstNameAttr, LastNameAttr, DigitIDAttr, DateAttr, CityAttr

BookTable = Table(
    {
        "id": Attribute(DigitIDAttr),
        "title": Attribute(CityAttr),
        "author_name": Attribute(FirstNameAttr),
    }
)

Reader = Table(
    {
        "id": Attribute(DigitIDAttr),
        "book_id": Attribute(DigitIDAttr),
        "return_date": Attribute(DateAttr),
    }
)

Person = Table(
    {
        "id": Attribute(DigitIDAttr),
        "Name": Attribute(FirstNameAttr),
        "Surname": Attribute(LastNameAttr),
        "Birthdate": Attribute(DateAttr),
    }
)


BookTable.add_relation("id", "Reader", "book_id", (0, 2))
Reader.add_relation("book_id", "BookTable", "id", (1, 1))

Reader.add_relation("id", "Person", "id", (1, 1))
Person.add_relation("id", "Reader", "id", (0, 1))


db_gen = DataBaseRandomGenerator()

db_gen.add_table("BookTable", BookTable)
db_gen.add_table("Reader", Reader)
db_gen.add_table("Person", Person)

db_gen.random_generation(min_rows=100)

db_gen.tables["BookTable"].to_csv("book_table.csv")
db_gen.tables["Reader"].to_csvdb_gen("reader.csv")
db_gen.tables["Person"].to_csv("person.csv")
