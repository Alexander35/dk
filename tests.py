import unittest
from http_server import Validator

class TestService(unittest.TestCase):

    def test_basic_structure(self):
        input_structure = {"username":"xyz",
            "phone":"8 (950) 288-56-23",
            "age": 28,
            "dub": 2.28,
            "phone1":"89146149360",
            "phone2":"+7(914)6149360",
            "skills": ["abc", "def", "ghi"],
            "skills1": ["abc", 3, "ghi"],
            "skills_named": {"python": 34, "django": 45 },
            "salary": "2.5", "passport": "1232424"}
        V = Validator(input_structure)
        report = V.validate()
        etalon_report = {'unknown_key error >> username xyz': 'UNKNOWN_KEY username',
            'rus_fed_pnone >> phone 8 (950) 288-56-23': 'IS_VALID 8 950 2885623',
            'int >> age 28': 'IS_VALID',
            'unknown_key error >> dub 2.28': 'UNKNOWN_KEY dub',
            'rus_fed_pnone >> phone1 89146149360': 'IS_VALID 89146149360',
            'rus_fed_pnone >> phone2 +7(914)6149360': 'IS_VALID +79146149360',
            "array_str >> skills ['abc', 'def', 'ghi']": 'IS_VALID',
            "array_str >> skills1 ['abc', 3, 'ghi']": 'NOT_VALID. type must be array of string, but 3!= "str" found',
            "skills_named_struct >> skills_named {'python': 34, 'django': 45}": 'IS_VALID',
            'float >> salary 2.5': "NOT_VALID. type must be float, but <class 'str'> given",
            'str >> passport 1232424': 'IS_VALID'}
        self.assertEqual(report, etalon_report)

if __name__ == '__main__':
    unittest.main()
