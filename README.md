# About [@fleppa_trade_bot](https://t.me/floppa_trade_bot?start=8a47115d-399b-4f20-8064-2f40497c4537)
---
В этом репозитории хранится исходный код проекта: код бота, автотесты, ci/cd pipelin'ы, базовая документация и всё остальное, что непосредственно связано с проектом. Помимо этого есть [доска в Miro](https://miro.com/app/board/uXjVP2tpPRg=/?share_link_id=930676536983), в которой много мыслей вслух про бота, его архитектуру и задачи.

## О боте
__:white_check_mark: - Это уже сделано;__ 

__:white_square_button: - Это нужно сделать;__

__:hand: - Не разрабатываем на текущей стадии, но держим в голове.__

### Текстовые команды бота:
* :white_check_mark: /menu — меню бота [сообщение не сохраняется в чате]
* :white_check_mark: /help — список всех команд
* :white_check_mark: /start — вывести приветственное сообщение [сообщение не сохраняется в чате]
* :white_square_button: /price — цена актива
  * :white_check_mark: /currency — вывести курсы валют и динамику их изменения - ожидает ввод (текстом или командой) тикера (или нескольких)
  * :white_square_button: цена акции [TBD: After MVP]
* :white_check_mark: /currency_graph — вывести график курсов валют - ожидает ввод (текстом или командой) тикера (или нескольких) или может быть запущена с параметрами из финального сообщения /currency
* :white_check_mark: /totem — узнать свой тотем на бирже - TODO: описать возможные
* :white_check_mark: /diploma — получить персональный диплом, на который фотошопится имя человека и его тотем, а так же ставится печать
* :white_check_mark: /feedback — оставить отзыв о работе бота или предложить функциональность
* /schedule — [В РАЗРАБОТКЕ] подписаться на изменения
  * :white_square_button: изучить документацию
  * :hand: реализовать
    * подписаться на тикер?
    * подписаться на информацию про день?
* :white_square_button: /stocks — [В РАЗРАБОТКЕ] информация об акциях
  * описать необходимые данные
  * выбрать подходящие запросы из API и собрать их композицию
  * придумать что рисовать?
* :white_square_button: /about_date [В РАЗРАБОТКЕ]
  * описать необходимые данные
  * выбрать подходящие запросы из API и собрать их композицию
  * написать обработчик для текущей даты
  * придумать что рисовать?
* :hand: /pulse — [В РАЗРАБОТКЕ] подключить аккаунт пульса
* :white_square_button: /candle — [В РАЗРАБОТКЕ] свечные графики торгов
* :white_check_mark: /crash — [ADMIN] крашнуться
* :white_check_mark: /reply — [ADMIN] ответить на фидбэк
* :white_check_mark: /env — [ADMIN] вывести тип окружения
* :white_check_mark: /sql — [ADMIN] взаимодействие с базой данных
* :white_check_mark: /set_admin — [ADMIN] сделать пользователя админом
* :white_check_mark: /make_link — [ADMIN] создать ссылку на бота
* :white_check_mark: /request — [ADMIN] отправить запрос
* :white_check_mark: /send — [ADMIN] сделать расслыку
* :white_check_mark: /stats — [ADMIN] статистика по пользователям, сообщениям и фидбэку

***

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

### CI/CD

В настоящий момент релизный процесс разделен на ветки develop и master, существует тестовый бот в продакшен окружении (@fleppa_fourth_bot), который собирается в докер контейнере из ветки develop и загружается на VM в Yandex Cloud. Вся работа с окружением в этом боте работает так же, как и в продакшен боте. Процесс развертывания занимает не более 5 минут, из них аптайм будет падать не более чем на 30 секунд (бот отключается только при выключении контейнера, сразу после чего будет запущен новый контейнер).

Помимо пайплайна со сборкой докер контейнера существует [DEPRECATED] скрипт для развертывания в вебхук (Yandex Cloud Functions). От этого формата мы отказались т. к. бот становится высоконагруженным и по различным функциональным требованиям вебхук не подходит для реализации.

На каждый коммит, за исключением прилетающих в мастер, срабатывает проверка линтера.

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
