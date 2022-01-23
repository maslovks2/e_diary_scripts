# Хаки от Ивана
Задолбала домашка, но хочется получать пятерки? Выход есть, можно воспользоваться скриптами из этого репозитория
Скрипты позволяют:
- удалять замечания
- добавлять похвалу от учителя
- исправлять двойки и тройки на пятерки

# Как установить
- развернуть сайт (следовать [инструкции](https://github.com/devmanorg/e-diary/tree/master)) 
- переместить файл script.py из текущего репозитория в корневой каталог сайта, на один уровень с manage.py

# Как пользоваться
- из корневого каталога сайта (где расположен файл manage.py) вызвать django консоль 

```bash
python manage.py shell
```

- в консоли импортировать скрипты
```python
from scripts import *
```

- для исправления оценок (поправить 2 и 3 на 5) вызвать fix_marks(schoolkid_name), где schoolkid_name это имя ученика 
```python
fix_marks('Сидоров Иван')
fix_marks('Иванов Василий Петрович')
```

- для удаления замечаний
```python
remove_chastisements('Сидоров Иван')
remove_chastisements('Сидоров Иван Васильевич')
``` 

- для добавления похвалы по заданному предмету (наименование предмета доллжно быть как в дневнике). Похвала добавляется в последний урок по предмету, на дату по которой еще не было похвалы.
```python
create_commendation('Сидоров Иван', 'География')
create_commendation('Иванов Василий Петрович', 'Алгебра')
```


