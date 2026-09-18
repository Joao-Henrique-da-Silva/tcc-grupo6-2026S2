-- TCC Grupo 6 - 2026S2
-- Schema do banco de dados

CREATE TABLE IF NOT EXISTS usuarios (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    nome       TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    perfil     TEXT NOT NULL DEFAULT 'luthier',
    criado_em  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS madeiras (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_qr       TEXT NOT NULL UNIQUE,
    especie         TEXT NOT NULL,
    descricao       TEXT,
    fornecedor      TEXT,
    procedencia     TEXT,
    certificacao    TEXT,
    data_extracao   DATE,
    data_entrada    DATE NOT NULL,
    massa_inicial_g REAL,
    massa_atual_g   REAL,
    status          TEXT NOT NULL DEFAULT 'em_estoque',
    criado_em       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS leituras (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    madeira_id    INTEGER,
    temperatura_c REAL NOT NULL,
    umidade_pct   REAL NOT NULL,
    origem        TEXT NOT NULL DEFAULT 'esp32',
    lida_em       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sincronizada  INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (madeira_id) REFERENCES madeiras(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_leituras_madeira ON leituras(madeira_id);
CREATE INDEX IF NOT EXISTS idx_leituras_data ON leituras(lida_em);

CREATE TABLE IF NOT EXISTS alertas (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    leitura_id   INTEGER NOT NULL,
    tipo         TEXT NOT NULL,
    severidade   TEXT NOT NULL DEFAULT 'aviso',
    mensagem     TEXT NOT NULL,
    resolvido    INTEGER NOT NULL DEFAULT 0,
    criado_em    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolvido_em DATETIME,
    FOREIGN KEY (leitura_id) REFERENCES leituras(id) ON DELETE CASCADE
);
