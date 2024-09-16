DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;
DROP TYPE IF EXISTS task_status;

CREATE TYPE task_status AS ENUM ('open', 'in_progress', 'done');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name TEXT,
    creator_id INTEGER REFERENCES users
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title TEXT,
    status task_status,
    creator_id INTEGER REFERENCES users
);
