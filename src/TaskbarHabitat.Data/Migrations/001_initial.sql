CREATE TABLE species (
    id              INTEGER PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    display_name    TEXT NOT NULL,
    region          TEXT NOT NULL DEFAULT 'kanto',
    type1           TEXT NOT NULL,
    type2           TEXT,
    evolution_stage INTEGER NOT NULL DEFAULT 1,
    evolves_from    INTEGER REFERENCES species(id),
    is_legendary    INTEGER NOT NULL DEFAULT 0,
    is_mythical     INTEGER NOT NULL DEFAULT 0,
    rarity_tier     TEXT NOT NULL DEFAULT 'common'
);

CREATE TABLE evolutions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    from_species_id INTEGER NOT NULL REFERENCES species(id),
    to_species_id   INTEGER NOT NULL REFERENCES species(id),
    trigger         TEXT NOT NULL DEFAULT 'level-up',
    min_level       INTEGER,
    condition_note  TEXT,
    UNIQUE(from_species_id, to_species_id)
);

CREATE TABLE habitats (
    id              TEXT PRIMARY KEY,
    display_name    TEXT NOT NULL,
    region          TEXT NOT NULL DEFAULT 'kanto',
    description     TEXT
);

CREATE TABLE encounters (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    habitat_id      TEXT NOT NULL REFERENCES habitats(id),
    species_id      INTEGER NOT NULL REFERENCES species(id),
    method          TEXT NOT NULL DEFAULT 'walk',
    chance          INTEGER NOT NULL CHECK (chance BETWEEN 0 AND 100),
    time_window     TEXT,
    weather         TEXT,
    UNIQUE(habitat_id, species_id, method)
);

CREATE TABLE save_state (
    id              INTEGER PRIMARY KEY CHECK (id = 1),
    starter_id      INTEGER NOT NULL REFERENCES species(id),
    xp              INTEGER NOT NULL DEFAULT 0,
    level           INTEGER NOT NULL DEFAULT 1,
    last_seen_utc   TEXT NOT NULL,
    game_epoch_utc  TEXT NOT NULL,
    total_ticks     INTEGER NOT NULL DEFAULT 0,
    save_id         TEXT NOT NULL,
    created_at_utc  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE creature_state (
    save_id         INTEGER PRIMARY KEY REFERENCES save_state(id),
    hunger          REAL NOT NULL DEFAULT 0.0,
    energy          REAL NOT NULL DEFAULT 100.0,
    happiness       REAL NOT NULL DEFAULT 50.0,
    last_updated_utc TEXT NOT NULL
);
INSERT INTO species (id, name, display_name, type1, type2, evolution_stage, evolves_from, rarity_tier) VALUES
(1, 'bulbasaur', 'Bulbasaur', 'grass', 'poison', 1, NULL, 'common'),
(2, 'ivysaur', 'Ivysaur', 'grass', 'poison', 2, 1, 'common'),
(3, 'venusaur', 'Venusaur', 'grass', 'poison', 3, 2, 'common'),
(4, 'charmander', 'Charmander', 'fire', NULL, 1, NULL, 'common'),
(5, 'charmeleon', 'Charmeleon', 'fire', NULL, 2, 4, 'common'),
(6, 'charizard', 'Charizard', 'fire', 'flying', 3, 5, 'common'),
(7, 'squirtle', 'Squirtle', 'water', NULL, 1, NULL, 'common'),
(8, 'wartortle', 'Wartortle', 'water', NULL, 2, 7, 'common'),
(9, 'blastoise', 'Blastoise', 'water', NULL, 3, 8, 'common');

INSERT INTO evolutions (from_species_id, to_species_id, trigger, min_level) VALUES
(1, 2, 'level-up', 16), (2, 3, 'level-up', 32),
(4, 5, 'level-up', 16), (5, 6, 'level-up', 36),
(7, 8, 'level-up', 16), (8, 9, 'level-up', 36);

INSERT INTO habitats (id, display_name, region, description) VALUES
('viridian-forest', 'Floresta de Viridian', 'kanto', 'Uma floresta densa e úmida ao oeste de Viridian City.');

INSERT INTO encounters (habitat_id, species_id, method, chance) VALUES
('viridian-forest', 1, 'walk', 15),
('viridian-forest', 4, 'walk', 15),
('viridian-forest', 7, 'walk', 15);
