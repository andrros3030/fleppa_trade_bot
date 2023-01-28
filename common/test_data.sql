-- DO NOT EXECUTE IN PRODUCTION DATABASE
insert into t_involve(pk_id, v_desc, v_override_start_message)
values ('some_involve_link', 'Описание ссылки для админов', 'Эта строка станет ответом на /start');

insert into t_users(pk_id) values('test1');
insert into t_users(pk_id, ts_reg) values('old_user', timestamp('2020-01-01'));
insert into t_users(pk_id, fk_involve) values('test_with_involve_link', 'some_involve_link');

insert into t_feedback (pk_id, fk_user, v_message_id, v_forwarded_id)
values ('uuid1', 'test1', 'origin_message_id', 'forward_id');
insert into t_feedback (pk_id, fk_user, v_message_id, v_forwarded_id, ts_requested)
values ('old_feedback', 'old_user', 'origin_message_id', 'forward_id', timestamp('2020-01-02'));

insert into t_messages(pk_id, fk_user, v_message_id, v_message_text, v_message_content_type)
values ('uuid_m1', 'test1', 'origin_message_id', 'message text', 'text');
insert into t_messages(pk_id, fk_user, v_message_id, v_message_text, v_message_content_type, ts_saved)
values ('uuid_m2', 'test1', 'origin_message_id', 'message text', 'text', timestamp('2023-01-25'));
insert into t_messages(pk_id, fk_user, v_message_id, v_message_text, v_message_content_type, ts_saved)
values ('uuid_m3', 'old_user', 'origin_message_id', 'message text', 'text', timestamp('2020-01-02'));
insert into t_messages(pk_id, fk_user, v_message_id, v_message_text, v_message_content_type, ts_saved)
values ('uuid_m4', 'old_user', 'origin_message_id', 'message text', 'text', timestamp('2020-01-02'));