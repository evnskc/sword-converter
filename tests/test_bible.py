import json
import sqlite3

from jsonschema import validate


class TestBible:
    def test_to_json(self, tmp_path, bible):
        output_file = bible.to_json()

        assert output_file == f"{tmp_path / '_'.join(bible._name.split())}.json"

        data = json.load(open(output_file))

        book_schema = {
            "type": "object",
            "required": ["number", "name", "abbreviation", "chapters"],
            "properties": {
                "number": {"type": "integer", "minimum": 1},
                "name": {"type": "string", "minLength": 1},
                "abbreviation": {"type": "string", "minLength": 1},
                "chapters": {
                    "type": "array",
                    "uniqueItems": True,
                    "items": {
                        "type": "object",
                        "required": ["number", "verses"],
                        "properties": {
                            "number": {"type": "integer", "minimum": 1},
                            "verses": {
                                "type": "array",
                                "uniqueItems": True,
                                "items": {
                                    "type": "object",
                                    "required": ["number", "text"],
                                    "properties": {
                                        "number": {"type": "integer", "minimum": 1},
                                        "text": {"type": "string", "minLength": 1}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        validate(data, {
            "type": "object",
            "required": ["name", "abbreviation", "books"],
            "properties": {
                "name": {"type": "string", "minLength": 1},
                "abbreviation": {"type": "string", "minLength": 1},
                "books": {
                    "type": "object",
                    "required": ["ot", "nt"],
                    "properties": {
                        "ot": {
                            "type": "array",
                            "uniqueItems": True,
                            "maxItems": 39,
                            "minItems": 39,
                            "items": book_schema
                        },
                        "nt": {
                            "type": "array",
                            "uniqueItems": True,
                            "maxItems": 27,
                            "minItems": 27,
                            "items": book_schema
                        }
                    }
                }
            }
        })

    def test_to_sqlite(self, tmp_path, bible):
        database = bible.to_sqlite()

        assert database == f"{tmp_path / '_'.join(bible._name.split())}.db"

        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        translations = cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='translations'")
        assert translations.fetchone()[0] == 1

        translations_count = cursor.execute("SELECT COUNT(*) FROM translations")
        assert translations_count.fetchone()[0] == 1

        books = cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='books'")
        assert books.fetchone()[0] == 1

        books_count = cursor.execute("SELECT COUNT(*) FROM books")
        assert books_count.fetchone()[0] == 66

        books_count_ot = cursor.execute("SELECT COUNT(*) FROM books WHERE testament = 'ot'")
        assert books_count_ot.fetchone()[0] == 39

        books_count_nt = cursor.execute("SELECT COUNT(*) FROM books WHERE testament = 'nt'")
        assert books_count_nt.fetchone()[0] == 27

        chapters = cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='chapters'")
        assert chapters.fetchone()[0] == 1

        verses = cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='verses'")
        assert verses.fetchone()[0] == 1

        cursor.close()
        connection.close()
