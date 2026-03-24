BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "users" (     -- Таблица со всеми пользователями
    "id_user"   SERIAL     PRIMARY KEY,  -- Уникальный ID
    "name"      TEXT       NOT NULL,     -- Отображаемое имя
    "pass_hash" TEXT       NOT NULL,     -- Пароль от аккаунта (зашифрованный)
    "id_chats"  INTEGER[]                -- ID Чатов, к которым пользователь имеет доступ
);

CREATE TABLE IF NOT EXISTS "chats" (    -- Таблица со всеми чатами (личными и групповыми)
    "id_chat"     SERIAL PRIMARY KEY,   -- Уникальный ID
    "name"        TEXT   DEFAULT NULL,  -- Название чата (только для групповых чатов)
    "description" TEXT   DEFAULT NULL   -- Описание чата (только для групповых чатов)
);

CREATE TABLE IF NOT EXISTS "messages" (  -- Таблица со всеми сообщениями
    "id_mess"   SERIAL     PRIMARY KEY,  -- Уникальный ID
    "id_sender" INTEGER    NOT NULL,     -- ID Отправителями
    "id_chat"   INTEGER    NOT NULL,     -- ID Чата, в который отправлено сообщение
    "text"      TEXT       NOT NULL,     -- Текст сообщения
    "date"      TIMESTAMP,               -- Дата записи в БД в виде unix timestamp
    "date_edit" TIMESTAMP  DEFAULT -1    -- Дата последнего изменения текста сообщения в виде unix timestamp, но где -1 - сообщение не изменялось.
);

--CREATE TABLE IF NOT EXISTS "session" (
--    "key" TEXT PRIMARY KEY,
--    "is_expired" BOOLEAN
--);

COMMIT;
