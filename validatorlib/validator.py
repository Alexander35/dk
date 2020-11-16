import re

class Validator():
    def __init__(self, structure):
        self.structure = structure
        self.result_structure = {}
        self.errors = {}

        self.specification = {
            'phone': self.validate_rus_fed_pnone,
            'passport': self.validate_str,
            'age': self.validate_int,
            'salary': self.validate_float,
            'skills': self.validate_array,
            'skills1': self.validate_array,
            'skills_named': self.validate_struct
        }

        self.keys_specification = {
            'skills_named': {'python':  self.validate_int,
                'django': self.validate_float,
                'rabbitmq': self.validate_rus_fed_pnone}
        }

    def add_error(self, item, error_text):
        self.errors[item] = error_text

    def add_result(self, item, val):
        self.result_structure[item] = val

    def add_specification(self, name, validator_method):
        self.specification[name] = validator_method

    def add_key_specification(self, name, specification):
        self.keys_specification[name] = specification

    def validate_str(self, value):
        type_of_val = type(value)

        if type_of_val == str:
            return (True, value)
        else:
            return (False, 'ERROR: `{}` is not string'.format(value)) 

    def validate_rus_fed_pnone(self, value):
        try:
            p = re.search('^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', value)

            if p is not None:
                phone = p.group(0).replace('(', '').replace('-','').replace(')','').replace(' ','')
                return (True, phone)
            else:
                return (False, 'ERROR: `{}`, phone format must be +7 (777) 777 77-77'.format(value))
        except TypeError as te:
            return (False, 'ERROR: `{}`, phone format must be +7 (777) 777 77-77'.format(value))

    def validate_int(self, value):
        type_of_val = type(value)

        if type_of_val == int:
            return (True, value)
        else:
            return (False, 'ERROR: `{}` is not integer'.format(value))

    def validate_float(self, value):
        type_of_val = type(value)

        if type_of_val == float:
            return (True, value)
        else:
            return (False, 'ERROR: `{}` is not float'.format(value))

    def validate_array(self, value):
        result = []
        result_len = 0
        error = ''
        len_value = len(value)

        for type_name, type_validator in self.specification.items():
            if ((str(type_validator) != str(self.validate_array)) and
                (str(type_validator) != str(self.validate_struct))):
                for v in value:
                    (is_ok, res) = type_validator(v)
                    if is_ok:
                        result.append(res)
                        error = ''
                        result_len = result_len + 1
                        if(result_len == len_value):
                            return (True, result)
                    else:
                        result = []
                        error = 'The items of the list has different types'
                        result_len = 0
                        break

        return (False, error)

    def validate_struct(self, type_of_item, value):
        keys = self.keys_specification.get(type_of_item, None)
        res = {}

        if keys is None:
            return(False, 'key_specification for {} does not exists'.format(type_of_item))

        for k, kv in keys.items():
            key = value.get(k, None)
            if key is None:
                return (False, 'key {} does not exists'.format(key))

            (check_status, result) = kv(key)

            if check_status == False:
                return (False, result)
            else:
                res[k] = result

        return (True, res)

    def validate(self):
        for type_of_item, value in self.structure.items():
            validator_func = self.specification.get(type_of_item, None)

            if validator_func is not None:
                if(str(validator_func) == str(self.validate_struct)):
                    (check_status, result) = self.validate_struct(type_of_item, value)
                else:
                    (check_status, result) = validator_func(value)

                if check_status:
                    self.add_result(type_of_item, result)
                else:
                    self.add_error(type_of_item, result)

            else:
                self.add_error(type_of_item, 'WARNING: validator for `{}` does not exist'.format(type_of_item))

        return {'result': self.result_structure, 'errors': self.errors}

def main():
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

    print(report)

if __name__ == '__main__':
    main()
