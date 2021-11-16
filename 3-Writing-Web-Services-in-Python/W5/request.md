```pycon
Python 3.10.0 (v3.10.0:b494f5935c, Oct  4 2021, 14:59:20) [Clang 12.0.5 (clang-1205.0.22.11)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import requests
>>> import json
>>> headers = {'Authorization': 'Basic YWxsYWRpbjpvcGVuc2VzYW1l'}
>>> response = requests.post('https://datasend.webpython.graders.eldf.ru/submissions/1/', headers=headers)
>>> json.loads(response.content.decode('utf-8'))
{'login': 'alibaba', 'password': '40razboinikov', 'path': 'submissions/secretlocation/', 'instructions': 'Сделайте PUT запрос на тот же хост, но на path указанный в этом документе c логином и паролем из этого документа. Логин и пароль также передайте в заголовке Authorization.'}
>>> import base64
>>> base64.b64encode(b'alibaba:40razboinikov')
b'YWxpYmFiYTo0MHJhemJvaW5pa292'
>>> headers = {'Authorization': 'Basic YWxpYmFiYTo0MHJhemJvaW5pa292'}
>>> response = requests.put('https://datasend.webpython.graders.eldf.ru/submissions/secretlocation/', headers=headers)
>>> json.loads(response.content.decode('utf-8'))
{'answer': 'w3lc0m370ch4p73r4.2'}
>>>
```