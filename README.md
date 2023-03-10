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
---
## Про код

Используем деление по необходимости наследования и самостоятельности функций. 

В base_modules лежат модули, которые не импортируют другие модули проекта и выполняют свою определенную функцию.
Это низший слой проекта, код внутри которого решает какую-то задачу, не связанную с пользовательскими функциями бота.
При этом, базовые модули инкапсулируют бизнес-логику, получая необходимые данные в качестве параметров.

В common_modules расположены модули, импортирующие модули из base_modules, которые могут быть использованы фичами, 
при этом не использующие друг друга и выполняющие какую-то комплексную задачу. В основном, все тестируемые модули
должны находится в этой папке. Это функциональный слой бота, сюда можно поместить функции по обработке изображений,
получению данных из ISS, построению графика. При этом, эти функции не имеют доступа к контексту и не работают с ботом.
Это необходимо для обеспечения возможности тестирования функций в отрыве от бота.

В features лежат модули, которые работают с common_modules, реализуя какую-либо бизнес-логику. Фичи работают с 
контекстом, могут доставать из контекста объекты базового модуля (но не импортируют их), взаимодействуют с ботом и 
реализуют какой-то конечный функционал для взаимодействия пользователя с ботом.

Таким образом код проекта инкапсулируется в основных сущностях и предотвращаются циклические зависимости.
Чтобы соблюсти эти меры - обращайте внимание на комментарии в самом начале файла. При создании нового файла - дублируйте
комментарии для этого слоя, чтобы другие контрибьюторы не забывали об этих простых правилах)

Важно, чтобы фичи не взаимодействовали с какими-либо базовыми модулями напрямую. 
Например, чтобы залогировать поведение своей функции в features -- нужно использовать прокинутый параметр через context.

Исходный код бота, который выливается в продакшен, живёт в каталоге src. Помимо этого, в бота вливается файл requirements.txt, который описывает зависимости проекта.
При редактировании этих файлов в основной ветке гита (master) срабатывает workflow, который раскатывает код на yandex-cloud functions.
Функция редактирования кода в основной ветке напрямую заблокирована, для создания новой версии бота необходимо вливать код через pull request.
При добавлении кода в ветку, отличную от основной, срабатывает workflow с линтером, который должен предотвратить пуш ___грязного___ кода в основную ветку.

---
## Полезные ресурсы:

<a href=https://cloud.yandex.ru/docs/iam/concepts/authorization/oauth-token>Get OAuth token</a> for YC CLI

<a href=https://www.moex.com/a2193>Документация ИСС Мосбиржи</a> 

<a href=http://iss.moex.com/iss/reference/>Спецификация API</a>

<a href=https://cloud.yandex.ru/docs/functions/lang/python/context>Про контекст вызова</a>

<a href=https://cloud.yandex.ru/docs/functions/operations/database-connection>Работа с PGSQL из CF</a>

---

<a href=https://cloud.yandex.ru/docs/functions/tutorials/connect-to-ydb>Работа с YDB</a>

<a href=https://github.com/ydb-platform/ydb-python-sdk/blob/main/examples/access-token-credentials/main.py>Use access token to YDB</a>