1. Задание выполнено с использованием стандартной библиотеки python
2. Решение было выполнено самостоятельно без копирования чужого кода (только гугление нужных частей)
3. Осуществлена поддержка следующих типов данных:
- Строка
- Целое число
- Число с плавающей точкой
- Российский федеральный номер телефона
- Массив с элементами одного фиксированного поддерживаемого типа
- Структура (ассоциативный массив с заранее известными ключами)

4. Решение можно расширить другими типами данных


5. Чтобы протестировать можно запустить python tests.py
6. Чтобы запустить приложение нужно запустить python http_server.py
И отправить данные например так

curl --header "Content-Type: application/json"   --request POST   --data '{"username":"xyz","phone":"8 (950) 288-56-23", "age": 28, "dub": 2.28,"phone1":"89146149360", "phone2":"+7(914)6149360", "skills": ["abc", "def", "ghi"], "skills1": ["abc", 3, "ghi"], "skills_named": {"python": 34, "django": 45 }, "salary": "2.5", "passport": "1232424"}'   http://localhost:8000

И получить ответ в виде 

POST / 
 Host: localhost:8000
User-Agent: curl/7.64.0
Accept: */*
Content-Type: application/json
Content-Length: 270

 
 b'{"username":"xyz","phone":"8 (950) 288-56-23", "age": 28, "dub": 2.28,"phone1":"89146149360", "phone2":"+7(914)6149360", "skills": ["abc", "def", "ghi"], "skills1": ["abc", 3, "ghi"], "skills_named": {"python": 34, "django": 45 }, "salary": "2.5", "passport": "1232424"}' 
 
POST processed
			Validation report


	unknown_key error >> username xyz :: UNKNOWN_KEY username

	rus_fed_pnone >> phone 8 (950) 288-56-23 :: IS_VALID 8 950 2885623

	int >> age 28 :: IS_VALID

	unknown_key error >> dub 2.28 :: UNKNOWN_KEY dub

	rus_fed_pnone >> phone1 89146149360 :: IS_VALID 89146149360

	rus_fed_pnone >> phone2 +7(914)6149360 :: IS_VALID +79146149360

	array_str >> skills ['abc', 'def', 'ghi'] :: IS_VALID

	array_str >> skills1 ['abc', 3, 'ghi'] :: NOT_VALID. type must be array of string, but 3!= "str" found

	skills_named_struct >> skills_named {'python': 34, 'django': 45} :: IS_VALID

	float >> salary 2.5 :: NOT_VALID. type must be float, but <class 'str'> given

	str >> passport 1232424 :: IS_VALID


где после слов Validation report можно видеть отчёт по валидации типов данных.