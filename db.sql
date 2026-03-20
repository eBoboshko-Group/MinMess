BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "user" (
    "id_user" SERIAL PRIMARY KEY,
    "name" TEXT NOT NULL,
    "pass_hash" TEXT NOT NULL,
    "id_chats" INTEGER[]
);

CREATE TABLE IF NOT EXISTS "chat" (
    "id_chat" SERIAL PRIMARY KEY,
    "name" TEXT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS "message" (
    "id_mess" SERIAL PRIMARY KEY,
    "id_sender" INTEGER NOT NULL,
    "id_chat" INTEGER NOT NULL,
    "text" TEXT NOT NULL,
    "date" TIMESTAMP
);

COMMIT;
