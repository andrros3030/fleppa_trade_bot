create table t_users(
    pk_id       varchar(40) primary key not null,
    l_admin     bool not null default false,
    t_reg       timestamp not null default current_timestamp
);