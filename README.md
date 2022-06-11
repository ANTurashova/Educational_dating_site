# Dating_site

**Общая идея:** 

Пишем бекэнд для сайта (приложения) знакомств.

**Задачи:**
1. Создать модель участников. У участника должна быть аватарка, пол, имя и фамилия, почта.
2. Создать эндпоинт регистрации нового участника: /api/clients/create (не забываем о пароле и совместимости с авторизацией модели участника).
3. При регистрации нового участника необходимо обработать его аватарку: наложить на него водяной знак (в качестве водяного знака можете взять любую картинку).
4. Создать эндпоинт оценивания участником другого участника: /api/clients/{id}/match. В случае, если возникает взаимная симпатия, то ответом выдаем почту клиенту и отправляем на почты участников: «Вы понравились <имя>! Почта участника: <почта>».
5. Создать эндпоинт списка участников: /api/list. Должна быть возможность фильтрации списка по полу, имени, фамилии. Советую использовать библиотеку Django-filters.
6. Реализовать определение дистанции между участниками. Добавить поля долготы и широты. В api списка добавить дополнительный фильтр, который показывает участников в пределах заданной дистанции относительно авторизованного пользователя. Не забывайте об оптимизации запросов к базе данных
https://en.wikipedia.org/wiki/Great-circle_distance
7. Задеплоить проект на любом удобном для вас хостинге, сервисах PaaS (Heroku) и т.п. Должна быть возможность просмотреть реализацию всех задач. Если есть какие-то особенности по тестированию, написать в Readme. Там же оставить ссылку/ссылки на АПИ проекта

-------------------------------------------------

# Инструкция:

Регистрируемся http://127.0.0.1:8000/api/clients/create 
![alt tag](https://sun9-20.userapi.com/impf/k_ER5hWzMl-8ZIWSTaVEtjMPA321NeyaYBOQ1g/Z5oi7MbcjyA.jpg?size=1297x655&quality=95&sign=28c8854dc6175915909dbfd3dd659345 "Описание будет тут")
![alt tag](https://sun9-60.userapi.com/impf/-F5kXcTd62GnFJkZVOd00864V_GP40_PU5GTlQ/cIw612VKzIE.jpg?size=1295x281&quality=95&sign=a57966f30473fe266b5489d38ebde7d5 "Описание будет тут")

Вы можете прикрепить изображение, на которое добавится вотермарка
![alt tag](https://sun9-56.userapi.com/impf/NiaeyW0VTp57tfY5OmjJ_yMKkXLY30aF4OSOAg/-r9ElETAlYk.jpg?size=989x613&quality=95&sign=4be1682ab07e063b26f28a04c80c1e53 "Описание будет тут")

Входим в аккаунт http://127.0.0.1:8000/api-authlogin/ 
![alt tag](https://sun7-14.userapi.com/impf/aNGcWryDVakmJGPA5p3ur5MaaPIBvGuiEn0bgg/3ieQgk8qkfg.jpg?size=1308x343&quality=95&sign=c9b2caf67a76a571fe24b7a1d39ee860 "Описание будет тут")

Просматриваем пользователей http://127.0.0.1:8000/api/clients/list 
![alt tag](https://sun9-2.userapi.com/impf/G4dULtwBWBHGuSyMujA4KOpR8zJ6S6O1hV5_oA/0Dcp_4fy5EU.jpg?size=1296x674&quality=95&sign=35d2b922a6a901b5f702f487f5cc8f93 "Описание будет тут")
![alt tag](https://sun9-77.userapi.com/impf/9BXXJLNUOGKH3B31Mf9ivYGMMcOO-KdfYpK9MA/zrjMQ_lcTm0.jpg?size=1294x206&quality=95&sign=d51383569d7956a63451d33067c4c5c4 "Описание будет тут")

Пользователей можно отфильтровать по имени, фамилии, полу и дистанции.
Например, поищем пользователя под именем "Anna" и фамилией "Tur"
http://127.0.0.1:8000/api/clients/list?first_name=Anna&last_name=Tur
![alt tag](https://sun9-15.userapi.com/impf/c9jNYO3B4nLg2VDnmdyJUt17hLAmcpbjYXrzvw/-lhGL4eqAa4.jpg?size=1309x574&quality=95&sign=2452d1187ff4139378b19dcebb689386 "Описание будет тут")

При регистрации пользователю присваивается рандомное местоположение. 
В фильтре вы можете указать радиус поиска других пользователей (в километрах).
Например, поищем девушек в радиусе трех километров http://127.0.0.1:8000/api/clients/list?sex=F&distance=3000 
![alt tag](https://sun9-58.userapi.com/impf/7AzVkfIJoejmSEbXIa1oSFf-QBtZabPRU7OvZA/zJQgtVk2eBI.jpg?size=1302x576&quality=95&sign=82ec6c3586db0b1f16779a413949eee2 "Описание будет тут")

Давайте выразим свою симпатию к какому-нибудь пользователю. 
Для этого в адресе http://127.0.0.1:8000/api/clients/{id}/match/ необходимо
заменить {id} на номер пользователя и отправить PUT запрос.
Например http://127.0.0.1:8000/api/clients/13/match/ 
![alt tag](https://sun9-43.userapi.com/impf/NCw_AbYSsNwKmEL7jttmnaoVvXDOWSSibNLaSA/7zxGMc00qJU.jpg?size=1296x651&quality=95&sign=f65be64acab8a01e8c4496f34b310a84 "Описание будет тут")

Мы получили ответ "Это взаимная симпатия! Его/её электронная почта: rf1junafarm@gmail.com"!
Такой ответ приходит только в том случае, если оба пользователя поставили симпатии друг другу!
![alt tag](https://sun9-53.userapi.com/impf/-2xMuwxJjlYPuSE5Lpfhir_K8-Je1XvgN2t39A/EtDB-voalCo.jpg?size=1296x651&quality=95&sign=704ef2dc078251c31be4a0e337828588 "Описание будет тут")

Теперь и вам, и выбранному вами пользователю на почту придут вот такие сообщения:
![alt tag](https://sun9-39.userapi.com/impf/d3PXJ3i9eRbbIUSU52VxIIuN6zGefW2i5ZVeyg/AikG4O-LDqY.jpg?size=1180x311&quality=95&sign=50e44d5b15527d1fa843bf9a11513b94 "Описание будет тут")
![alt tag](https://sun9-78.userapi.com/impf/sp0y52Llf3ge1JP2bwFipKovLPzEi7AMAPRUiw/gnzdy17VQbU.jpg?size=1008x293&quality=95&sign=1190456d15c07cb10f75bab7d30effd3 "Описание будет тут")
