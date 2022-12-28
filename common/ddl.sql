-- TODO: нужно очень сильно подумать о том, как будет работать навигация
-- в первую очередь функционал должен исходить из потребности
-- закодировать действие комманды в SQL фактически не представляется возможным
-- однако и смысла раздувать код и в SQL и в Python
-- возможно есть способ описать навигацию в одном Python, а в SQL записывать результат навигации?
-- TODO: описать типовые кейсы и данные, которые нужно хранить/изменять
-- до тех пор файл actions.py и архитектура commands.py заблокирована


-- /*
--  Сущность КОММАНДА:
--  имеет уникальный id,
--  имеет некоторый набор псевдонимов для вызова
--  имеет описание, которое можно вывести пользователю, что делает комманда
--  имеет флаг, отвечающий за ограничение доступа к комманде только админам
-- */
-- create table t_commands(
--     pk_id           serial primary key,
--     v_aliases       varchar(255) not null,
--     v_desc          varchar(400) not null,
--     l_admin_only    bool not null default false,
-- );

-- /*
--  Сущность ПУТЬ:
--  должна быть уникальна для каждого пользователя
--  ключевое значение пути - ссылка, отвечающая за шаг, на котором находится пользователь
--  на каждом шаге хранится свой набор аргументов
--  пользователь имеет возможность вернуться на предыдущий шаг и не потерять аргументы пути
-- */
-- create table t_routes(
--     pk_id       serial primary key,
--     fk_prev     integer null references t_routes(pk_id),
--     pv_link     varchar(36) not null,
--     v_args      varchar(255) null
-- );
-- insert into t_routes(pv_link) values ('/');
-- /*
--  Связь ПУТЬ-КОММАНДА
--  одному пути может соответствовать несколько комманд
--  одна и та же комманда может быть доступна из нескольких путей
-- */
-- create table t_path_commands(
--     pk_id           serial primary key,
--     fk_path         integer references t_route(pk_id),
--     fk_command      integer references t_commands(pk_id)
-- );
/*
 Сущность ПОЛЬЗОВАТЕЛЬ:
 имеет уникальный id в Телеграмме
 может являться админом, но по умолчанию не является им
 имеет timestamp регистрации
 имеет ссылку на путь, в котором сейчас находится
*/
create table t_users(
    pk_id       varchar(40) primary key not null,
    l_admin     bool not null default false,
    t_reg       timestamp not null default current_timestamp,
--     fk_route    integer references t_routes(pk_id) default 0,
);
-- alter table t_users add column fk_route integer references t_routes(pk_id) default 1
