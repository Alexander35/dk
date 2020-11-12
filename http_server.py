import http.server
import json
import re

PORT = 8000

dummy_specification = {
    'passport': 'str',
    'phone': 'rus_fed_pnone',
    'phone1': 'rus_fed_pnone',
    'phone2': 'rus_fed_pnone',
    'age': 'int',
    'salary': 'float',
    'skills': 'array_str',
    'skills1': 'array_str',
    'skills_named': 
        {'python': 'int',
        'django': 'int',
        'python_years': 'float'}
}

class Validator():
    def __init__(self, structure):
        self.structure = structure

    def validate_str(self, item):
        type_of_item = type(item)
        if type_of_item == str:
            return 'IS_VALID'
        else:
            return 'NOT_VALID. type must be str, but {} given'.format(type_of_item) 

    def validate_rus_fed_pnone(self, item):
        p = re.search('^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', item)
        phone = 'NOT_VALID. phone format must be +7 (777) 777 77-77, but {} given'.format(item)

        if p is not None:
            phone = p.group(0).replace('(', '').replace('-','').replace(')','')
            return 'IS_VALID {}'.format(phone)

    def validate_int(self, item):
        type_of_item = type(item)
        if type_of_item == int:
            return 'IS_VALID'
        else:
            return 'NOT_VALID. type must be int, but {} given'.format(type_of_item) 

    def validate_float(self, item):
        type_of_item = type(item)
        if type_of_item == float:
            return 'IS_VALID'
        else:
            return 'NOT_VALID. type must be float, but {} given'.format(type_of_item) 

    def validate_array_str(self, item):
        for i in item:
            if self.validate_str(i) != 'IS_VALID':
                return 'NOT_VALID. type must be array of string, but {}!= "str" found'.format(i)

        return 'IS_VALID'

    def validate_array_skills_named_struct(self, item):
        for i, _ in item.items():
            if dummy_specification['skills_named'].get(i, None) is None:
                return 'NOT_VALID. skills_named_struct format must be "python": val, "django": val , "python_years": val, but {} given'.format(item)

        return 'IS_VALID'

    def validate(self):

        validation_report = {}

        for key, val in self.structure.items():
            type_of_item = dummy_specification.get(key, None)
            if type_of_item is not None:
                if type_of_item is 'str':
                    chunk_name = 'str >> {} {}'.format(key, val)
                    validation_report[chunk_name] = self.validate_str(val)

                elif type_of_item is 'rus_fed_pnone':
                    chunk_name = 'rus_fed_pnone >> {} {}'.format(key, val)
                    validation_report[chunk_name] =  self.validate_rus_fed_pnone(val)

                elif type_of_item is 'int':
                    chunk_name = 'int >> {} {}'.format(key, val)
                    validation_report[chunk_name] =  self.validate_int(val)

                elif type_of_item is 'float':
                    chunk_name = 'float >> {} {}'.format(key, val)
                    validation_report[chunk_name] =  self.validate_float(val)

                elif type_of_item is 'array_str':
                    chunk_name = 'array_str >> {} {}'.format(key, val)
                    validation_report[chunk_name] =  self.validate_array_str(val)

                elif (key == 'skills_named') and (type(type_of_item) is dict):
                    chunk_name = 'skills_named_struct >> {} {}'.format(key, val)
                    validation_report[chunk_name] =  self.validate_array_skills_named_struct(val)
            else:
                chunk_name = 'unknown_key error >> {} {}'.format(key, val)
                validation_report[chunk_name] =  "UNKNOWN_KEY {}".format(key)

        return validation_report

class Handler(http.server.BaseHTTPRequestHandler):
    def make_json(self, data):
        data_json = json.loads(data)

        return data_json

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length) 

        self._set_response()
        self.wfile.write("POST {} \n {} \n {} \n ".format(self.path, self.headers, post_data).encode('utf-8'))

        json_data = self.make_json(post_data)
        V = Validator(json_data)
        valid_report = V.validate()

        self.wfile.write("\nPOST processed\n".encode('utf-8'))
        self.wfile.write("\t\t\tValidation report\n\n".encode('utf-8'))

        print('valid_report', valid_report)

        for key, chunk in valid_report.items():
            self.wfile.write('\n\t{} :: {}\n'.format(key, chunk).encode('utf-8'))

if __name__ == '__main__':
    with http.server.HTTPServer(("", PORT), Handler) as httpd:
        print("========= Server start at port : {} =========".format(PORT))
        httpd.serve_forever()