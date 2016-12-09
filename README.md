Документация в Wiki

русский текст в MYSQL: 

Выполнить: 
ALTER TABLE database.table MODIFY COLUMN col VARCHAR(255)
CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;
   
Добавить: 
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        ...
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}    