CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    imie          TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL DEFAULT 'klient'   -- 'klient' lub 'serwis'
);

CREATE TABLE IF NOT EXISTS zgloszenia (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL REFERENCES users(id),
    urzadzenie TEXT NOT NULL,
    opis       TEXT NOT NULL,
    status     TEXT NOT NULL DEFAULT 'Przyjęte',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);