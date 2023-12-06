import json

from jsonschema import validate

from sword_converter.converters.bible import Bible


class TestBible:

    def test_to_json(self, tmp_path, source, module):
        bible = Bible(source, module)
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
