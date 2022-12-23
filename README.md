# fleppa_trade_bot

В этом репозитории хранится исходный код проекта: код бота, автотесты, ci/cd pipelin'ы, базовая документация и всё остальное, что непосредственно связано с проектом

## Техническая документация и всякая всячина

Для работы команд бота необходима реализация следущих базовых сущностей:
* акция (тикер, индекс, думаю можно объеденить)
* историческое поведение акции (является композицией акции с одним тикером, но за разное время) с вычисляемыми значениями min/max/avg/0.25/0.5/0.75 по основным параметрам

Помимо этого, необходимы функции по работе с изображениями:
* создать график и записать его в base64 (нужно сделать варианты с разным качеством)
* добавить на изображение другое изображение (прифотошопить вотермарку, сделать арт и т.д.)


### О функциональностях
__:white_check_mark: - Это уже сделано;__ 

__:white_square_button: - Это нужно сделать;__

__:hand: - Не разрабатываем на текущей стадии, но держим в голове.__

#### Комманды для бота (/setcommands):

* :white_square_button: /about - информация о боте
  * выводить информацию о создателях
  * выводить информацию о сборке
  * выводить ссылку на гит
* :hand: /art - сделать персональный арт
  * прифотошопить к аватарке человека (хомячка/пульс-лого)
  * прифотошопить к фото из диалога (хомячка/пульс-лого)
* /subscribe - подписаться на рассылку
  * :white_square_button: изучить документацию
  * :hand: реализовать
    * подписаться на тикер?
    * подписаться на информацию про день?
* :white_square_button: /about_ticker
  * описать необходимые данные
  * выбрать подходящие запросы из API и собрать их композицию
  * придумать что рисовать?
* :white_square_button: /about_date
  * описать необходимые данные
  * выбрать подходящие запросы из API и собрать их композицию
  * написать обработчик для текущей даты
  * придумать что рисовать?
* :white_square_button: /help - информация о коммандах бота


#### Описание для бота при запуске (/setdescription): ***Мир инвестиций не так уж и легок, не правда ли? Шлёппа многое повидал и готов поделиться своей мудростью***
#### Имя для бота (/setname): ***Fleppa trade bot***
#### Описание в профиле бота (/mybots -> About): ***Бот для ржакича про инвестиции***

## Полезные ресурсы:

<a href=https://cloud.yandex.ru/docs/iam/concepts/authorization/oauth-token>Get OAuth token</a> for YC CLI

<a href=https://www.moex.com/a2193>Документация ИСС Мосбиржи</a> 

<a href=http://iss.moex.com/iss/reference/>Спецификация API</a>

<a href=https://cloud.yandex.ru/docs/functions/tutorials/connect-to-ydb>Работа с YDB</a>

<a href=https://github.com/ydb-platform/ydb-python-sdk/blob/main/examples/access-token-credentials/main.py>Use access token to YDB</a>