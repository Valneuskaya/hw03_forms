[![CI](https://github.com/yandex-praktikum/hw03_forms/actions/workflows/python-app.yml/badge.svg?branch=master)](https://github.com/yandex-praktikum/hw03_forms/actions/workflows/python-app.yml)

Проект Yatube - соцсеть для публикации дневников.

В данном репозитории работа по Django ORM.

1. Настроен эмулятор отправки писем

Отправленные письма сохраняются в виде текстовых файлов в директорию /sent_emails. Настроена отправка письма при восстановлении пароля. 

2. Создано и подключено приложение core. В нём
- размещён и зарегистрирован фильтр addclass, позволяющий добавлять CSS-класс к тегу шаблона.
- создан и зарегистрирован контекст-процессор, добавляющий текущий год на все страницы в переменную {{ year }}

3. Создано и подключено приложение about, в нём
- созданы статические страницы /about/author/ и /about/tech/.
- ссылки на эти страницы добавлены в навигацию сайта.
Для всех путей установлены name и namespace.

4. Подключено приложение django.contrib.auth

Его urls.py подключен к головному urls.py.

5. Создано и подключено приложение users, в нём
- переопределены шаблоны для адресов
    /auth/login/ (авторизация),
    /auth/logout/ (выход из аккаунта).
- создана страница /auth/signup/ с формой для регистрации пользователей.

6. Изменено приложение posts, в нем:
- создана страница пользователя profile/<username>/. На ней отображаются посты пользователя. 
- создана отдельная страница поста posts/<post_id>/. 
- подключен паджинатор, он выводит по десять постов
    на главную страницу,
    на страницу профайла,
    на страницу группы.
- создана навигация по разделам.

7. Создана форма для публикации новых записей.

У зарегистрированных пользователей Yatube теперь есть возможность самостоятельно публиковать посты.
  
8. Создана форма редактирования записи с адресом /posts/<post_id>/edit/. 
