INSERT INTO "chats" DEFAULT VALUES;
INSERT INTO "chats" DEFAULT VALUES;
UPDATE "users" SET "id_chats" = array_append("id_chats", 1) WHERE "id_user" = 1;
UPDATE "users" SET "id_chats" = array_append("id_chats", 1) WHERE "id_user" = 2;
UPDATE "users" SET "id_chats" = array_append("id_chats", 2) WHERE "id_user" = 2;
UPDATE "users" SET "id_chats" = array_append("id_chats", 2) WHERE "id_user" = 3;