/*
 Сущность ССЫЛКА-ПРИВЛЕЧЕНИЯ
 содержит уникальный идентификатор (его используем при старте бота)
 содержит описание, для внутренней идентификации ссылки
 является:
 (1) статистическим инструментом для внутренней аналитики и оценки качества рекламных каналов
 [2] заделом для создания партнёрской программы (создания рекомендаций)
*/
create table t_involve(
    pk_id                       varchar(40) primary key not null,
    v_desc                      varchar(200) not null,
    v_override_start_message    varchar(4000) null
);
/*
 Сущность ПОЛЬЗОВАТЕЛЬ:
 имеет уникальный id в Телеграмме
 может являться админом, но по умолчанию не является им
 несет флаг о бане пользовательского фидбэка
 имеет поле о текущей позиции пользователя
 имеет timestamp регистрации
 имеет ссылку на путь, в котором сейчас находится
*/
create table t_users(
    pk_id       varchar(40) primary key not null,
    l_admin     bool not null default false,
    l_banned    bool not null default false,
    v_position  varchar(4000) not null default '/',
    ts_reg      timestamp not null default current_timestamp,
    fk_involve  varchar(40) null references t_involve(pk_id) on delete set null
);
/*
 Сущность ФИДБЭК
 уникальный генерируемый id
 ссылка на пользователя
 id сообщения в пользовательском чате
 id пересланого сообщения
 есть ли ответ на фидбэк
 когда был написан фидбэк
 когда был дан ответ на фидбэк
*/
create table t_feedback(
    pk_id           varchar(40) primary key not null,
    fk_user         varchar(40) not null references t_users(pk_id) on delete cascade,
    v_message_id    varchar(40) not null,
    v_forwarded_id  varchar(40) not null,
    l_answered      bool not null default false,
    ts_requested    timestamp not null default current_timestamp,
    ts_answered     timestamp null
);
/*
 Таблица СООБЩЕНИЯ
 уникальный id (uuid)
 ссылка на пользователя
 id сообщения в диалоге
 текст сообщения
 тип контента сообщения
 дата получения сообщения
*/
create table t_messages(
    pk_id                   varchar(40) primary key not null,
    fk_user                 varchar(40) not null references t_users(pk_id) on delete cascade,
    v_message_id            varchar(40) not null,
    v_message_text          varchar(4000) not null,
    v_message_content_type  varchar(20) not null,
    ts_saved                timestamp not null default current_timestamp
);
/*
 Таблица КОЛБЕКИ
 уникальный id (uuid)
 ссылка на пользователя
 id сообщения с кнопкой в диалоге (по идее может быть ссылкой на t_messages)
 текст кнопки
 данные, которые несла кнопка
 дата получения сообщения
*/
create table t_callbacks(
    pk_id                   varchar(40) primary key not null,
    fk_user                 varchar(40) not null references t_users(pk_id) on delete cascade,
    v_message_id            varchar(40) not null,
    v_button_text           varchar(40) not null,
    v_callback_data         varchar(4000) not null,
    ts_saved                timestamp not null default current_timestamp
)