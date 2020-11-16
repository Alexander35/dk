import unittest
from validator import Validator

class TestService(unittest.TestCase):

    def test_basic_structure(self):
        input_structure = {"username":"xyz",
            "passport": "some passport number",
            "phone": "8 (950) 888-56-23",
            "age": 28,
            "dub": "2.28",
            "s": {"a":"a", "b":2, "c": 3.54, "d": "8 (950) 888-56-2"},
            "skills12": ["abc", "def", "ghi"],
            "skills": [234, 546, 3.33],
            "skills1": ["8 (950) 222-56-23", 3.2, "89146149360", "+7(914)6149360"],
            "skills_named": {"python": 34, "django": 4.5, "rabbitmq": "8 (950) 888-56-23" },
            "salary": 2.5}

        V = Validator(input_structure)

        key_struct = {"a":V.validate_str, "b":V.validate_int, "c": V.validate_float, "d": V.validate_rus_fed_pnone}

        V.add_specification('dub', V.validate_float)
        V.add_specification('skills12', V.validate_array)
        V.add_specification('s', V.validate_struct)
        V.add_key_specification('s', key_struct)
        report = V.validate()


        etalon_report = {'result': {'passport': 'some passport number',
            'phone': '89508885623',
            'age': 28,
            'skills12': ['abc', 'def', 'ghi'],
            'skills_named': {'python': 34, 'django': 4.5, 'rabbitmq': '89508885623'},
            'salary': 2.5},
            'errors': {'username': 'WARNING: validator for `username` does not exist',
                'dub': 'ERROR: `2.28` is not float',
                's': 'ERROR: `8 (950) 888-56-2`, phone format must be +7 (777) 777 77-77',
                'skills': 'The items of the list has different types',
                'skills1': 'The items of the list has different types'}}
        self.assertEqual(report, etalon_report)

    def test_first_structure(self):
        input_structure = {
            "foo": 123,
            "bar": "asd",
            "baz": "8 (950) 288-56-25"
        }

        V = Validator(input_structure)
        V.add_specification('foo', V.validate_int)
        V.add_specification('bar', V.validate_str)
        V.add_specification('baz', V.validate_rus_fed_pnone)
        report = V.validate()

        etalon_report = {'result': {'foo': 123, 'bar': 'asd', 'baz': '89502885625'},
        'errors': {}}
        self.assertEqual(report, etalon_report)

if __name__ == '__main__':
    unittest.main()
