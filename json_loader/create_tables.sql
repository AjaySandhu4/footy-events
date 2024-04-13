DROP TABLE IF EXISTS competition;
CREATE TABLE competition (
    competition_id INTEGER NOT NULL,
    season_id INTEGER NOT NULL,
    competition_name CHAR(14) NOT NULL,
    season_name CHAR(9) NOT NULL,
    competition_country CHAR(24) NOT NULL,
    competition_gender CHAR(6) NOT NULL,
    competition_youth BOOLEAN NOT NULL,
    competition_international BOOLEAN NOT NULL,

    PRIMARY KEY (competition_id, season_id)
);

DROP TABLE IF EXISTS player;
CREATE TABLE player (
    player_id INTEGER PRIMARY KEY,
    player_name TEXT NOT NULL, 
    player_nickname TEXT,
    player_country TEXT NOT NULL
);

DROP TABLE IF EXISTS team;
CREATE TABLE team (
    team_id INTEGER PRIMARY KEY,
    team_name CHAR(24) NOT NULL,
    team_country CHAR(24) NOT NULL
);

DROP TABLE IF EXISTS manager;
CREATE TABLE manager (
    manager_id INTEGER PRIMARY KEY,
    manager_name TEXT NOT NULL,
    manager_nickname TEXT,
    manager_dob DATE NOT NULL,
    manager_country TEXT NOT NULL
);

DROP TABLE IF EXISTS referee;
CREATE TABLE referee (
    referee_id INTEGER PRIMARY KEY,
    referee_name TEXT NOT NULL,
    referee_country TEXT NOT NULL
);

DROP TABLE IF EXISTS matches;
CREATE TABLE matches (
    match_id INTEGER PRIMARY KEY,
    competition_id INTEGER NOT NULL,
    season_id INTEGER NOT NULL,
    match_date DATE NOT NULL,
    kick_off TIME NOT NULL,
    stadium_name CHAR(32),
    stadium_country CHAR(24),
    referee_id INTEGER,
    home_team_id INTEGER NOT NULL,
    home_manager_id INTEGER,
    home_score INTEGER NOT NULL,
    away_team_id INTEGER NOT NULL,
    away_manager_id INTEGER,
    away_score INTEGER NOT NULL,
    match_week INTEGER NOT NULL,
    competition_stage CHAR(14) NOT NULL,

    FOREIGN KEY (competition_id, season_id) REFERENCES competition (competition_id, season_id),
    FOREIGN KEY (home_team_id) REFERENCES team (team_id),
    FOREIGN KEY (away_team_id) REFERENCES team (team_id),
    FOREIGN KEY (home_manager_id) REFERENCES manager (manager_id),
    FOREIGN KEY (away_manager_id) REFERENCES manager (manager_id),
    FOREIGN KEY (referee_id) REFERENCES referee (referee_id)
);

DROP TABLE IF EXISTS lineup;
CREATE TABLE lineup (
    match_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    jersey_number INTEGER NOT NULL,

    PRIMARY KEY (match_id, player_id, team_id),
    FOREIGN KEY (match_id) REFERENCES matches (match_id),
    FOREIGN KEY (player_id) REFERENCES player (player_id),
    FOREIGN KEY (team_id) REFERENCES team (team_id)
);

DROP TABLE IF EXISTS position;
CREATE TABLE position (
    match_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    position_name TEXT NOT NULL,
    position_from CHAR(5) NOT NULL,
    position_to CHAR(5),
    from_period INTEGER NOT NULL,
    to_period INTEGER,
    start_reason TEXT NOT NULL,
    end_reason TEXT NOT NULL,

    PRIMARY KEY (player_id, match_id, team_id, position_name, position_from),
    FOREIGN KEY (player_id) REFERENCES player (player_id),
    FOREIGN KEY (match_id) REFERENCES matches (match_id)
);

DROP TABLE IF EXISTS cards;
CREATE TABLE cards (
    player_id INTEGER NOT NULL,
    match_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    card_time CHAR(5) NOT NULL,
    card_type CHAR(24) NOT NULL,
    card_reason TEXT,
    card_period INTEGER NOT NULL,

    PRIMARY KEY (player_id, match_id, team_id, card_time, card_type),
    FOREIGN KEY (player_id) REFERENCES player (player_id),
    FOREIGN KEY (match_id) REFERENCES matches (match_id)
);

DROP TABLE IF EXISTS events;
CREATE TABLE events (
    event_id CHAR(36) PRIMARY KEY,
    match_id INTEGER NOT NULL,
    event_index INTEGER NOT NULL,
    event_timestamp TIME NOT NULL,
    event_period INTEGER NOT NULL,
    event_minute INTEGER NOT NULL,
    event_second INTEGER NOT NULL,
    event_type CHAR(24) NOT NULL,
    possession INTEGER NOT NULL,
    possession_team_id INTEGER NOT NULL,
    play_pattern CHAR(24) NOT NULL,
    team_id INTEGER NOT NULL,
    player_id INTEGER,
    position TEXT,
    location_x DECIMAL,
    location_y DECIMAL,
    duration DECIMAL,
    under_pressure BOOLEAN,
    off_camera BOOLEAN,
    ball_out BOOLEAN,
    counterpress BOOLEAN,
    tactics_formation INTEGER,
    outcome CHAR(24),

    FOREIGN KEY (match_id) REFERENCES matches (match_id),
    FOREIGN KEY (player_id) REFERENCES player (player_id),
    FOREIGN KEY (team_id) REFERENCES team (team_id)
);

DROP TABLE IF EXISTS related_event;
CREATE TABLE related_event (
    event_id CHAR(36),
    related_event_id CHAR(36),

    PRIMARY KEY (event_id, related_event_id),
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (related_event_id) REFERENCES events (event_id)
);

DROP TABLE IF EXISTS pass;
CREATE TABLE pass (
    event_id CHAR(36) PRIMARY KEY,
    competition_id INTEGER NOT NULL,
    season_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    recipient_id INTEGER,
    pass_length DECIMAL NOT NULL,
    angle DECIMAL NOT NULL,
    height CHAR(24) NOT NULL,
    end_location_x DECIMAL NOT NULL,
    end_location_y DECIMAL NOT NULL,
    is_cross BOOLEAN,
    switch BOOLEAN,
    shot_assist BOOLEAN,
    goal_assist BOOLEAN,
    cutback BOOLEAN,
    backheel BOOLEAN,
    deflected BOOLEAN,
    miscommunication BOOLEAN,
    body_part CHAR(24),
    pass_type CHAR(24),
    technique CHAR(24),

    FOREIGN KEY (competition_id, season_id) REFERENCES competition (competition_id, season_id),
    FOREIGN KEY (player_id) REFERENCES player (player_id),
    FOREIGN KEY (team_id) REFERENCES team (team_id),
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (recipient_id) REFERENCES player (player_id)
);

DROP TABLE IF EXISTS shot;
CREATE TABLE shot (
    event_id CHAR(36) PRIMARY KEY,
    competition_id INTEGER NOT NULL,
    season_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    key_pass_id CHAR(36),
    end_location_x DECIMAL NOT NULL,
    end_location_y DECIMAL NOT NULL,
    end_location_z DECIMAL,
    aerial_won BOOLEAN,
    follows_dribble BOOLEAN,
    first_time BOOLEAN,
    open_goal BOOLEAN,
    statsbomb_xg DECIMAL NOT NULL,
    deflected BOOLEAN,
    technique CHAR(13),
    body_part CHAR(10),
    shot_type CHAR(10),

    FOREIGN KEY (competition_id, season_id) REFERENCES competition (competition_id, season_id),
    FOREIGN KEY (player_id) REFERENCES player (player_id),
    FOREIGN KEY (team_id) REFERENCES team (team_id),
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (key_pass_id) REFERENCES pass (event_id)
);

DROP TABLE IF EXISTS dribble;
CREATE TABLE dribble (
    event_id CHAR(36) PRIMARY KEY,
    competition_id INTEGER NOT NULL,
    season_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    overrun BOOLEAN,
    nutmeg BOOLEAN,
    no_touch BOOLEAN,
    outcome CHAR(10),

    FOREIGN KEY (competition_id, season_id) REFERENCES competition (competition_id, season_id),
    FOREIGN KEY (player_id) REFERENCES player (player_id),
    FOREIGN KEY (event_id) REFERENCES events (event_id)
);

DROP TABLE IF EXISTS dribbled_past;
CREATE TABLE dribbled_past (
    event_id CHAR(36) PRIMARY KEY,
    competition_id INTEGER NOT NULL,
    season_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    outcome CHAR(10),

    FOREIGN KEY (competition_id, season_id) REFERENCES competition (competition_id, season_id),
    FOREIGN KEY (player_id) REFERENCES player (player_id),
    FOREIGN KEY (event_id) REFERENCES events (event_id)
);

DROP TABLE IF EXISTS bad_behaviour;
CREATE TABLE bad_behaviour (
    event_id CHAR(36) PRIMARY KEY,
    card_name TEXT,

    FOREIGN KEY (event_id) REFERENCES events (event_id)
);

DROP TABLE IF EXISTS ball_recovery;
CREATE TABLE ball_recovery (
    event_id CHAR(36) PRIMARY KEY,
    offensive BOOLEAN,
    recovery_failure BOOLEAN,

    FOREIGN KEY (event_id) REFERENCES events (event_id)
);

DROP TABLE IF EXISTS blocks;
CREATE TABLE blocks (
    event_id CHAR(36) PRIMARY KEY,
    deflection BOOLEAN,
    offensive BOOLEAN,
    save_block BOOLEAN,

    FOREIGN KEY (event_id) REFERENCES events (event_id)
);

DROP TABLE IF EXISTS carry;
CREATE TABLE carry (
    event_id CHAR(36) PRIMARY KEY,
    end_location_x DECIMAL,
    end_location_y DECIMAL,

    FOREIGN KEY (event_id) REFERENCES events (event_id)
);

DROP TABLE IF EXISTS clearance;
CREATE TABLE clearance (
    event_id CHAR(36) PRIMARY KEY,
    aerial_won BOOLEAN,
    body_part TEXT,

    FOREIGN KEY (event_id) REFERENCES events (event_id)
);

DROP TABLE IF EXISTS duel;
CREATE TABLE duel (
    event_id CHAR(36) PRIMARY KEY,
    duel_type TEXT,

    FOREIGN KEY (event_id) REFERENCES events (event_id)
);

DROP TABLE IF EXISTS foul_committed;
CREATE TABLE foul_committed (
    event_id CHAR(36) PRIMARY KEY,
    offensive BOOLEAN,
    foul_type TEXT,
    advantage BOOLEAN,
    penalty BOOLEAN,
    card_name TEXT,

    FOREIGN KEY (event_id) REFERENCES events (event_id)
);

DROP TABLE IF EXISTS foul_won;
CREATE TABLE foul_won (
    event_id CHAR(36) PRIMARY KEY,
    defensive BOOLEAN,
    advantage BOOLEAN,
    penalty BOOLEAN,

    FOREIGN KEY (event_id) REFERENCES events (event_id)
);

DROP TABLE IF EXISTS goalkeeper;
CREATE TABLE goalkeeper (
    event_id CHAR(36) PRIMARY KEY,
    position TEXT,
    technique TEXT,
    body_part TEXT,
    goalkeeper_type TEXT,

    FOREIGN KEY (event_id) REFERENCES events (event_id)
);

DROP TABLE IF EXISTS half_end;
CREATE TABLE half_end (
    event_id CHAR(36) PRIMARY KEY,
    early_video_end BOOLEAN,
    match_suspended BOOLEAN,

    FOREIGN KEY (event_id) REFERENCES events (event_id)
);

DROP TABLE IF EXISTS half_start;
CREATE TABLE half_start (
    event_id CHAR(36) PRIMARY KEY,
    late_video_start BOOLEAN,

    FOREIGN KEY (event_id) REFERENCES events (event_id)
);

DROP TABLE IF EXISTS injury_stoppage;
CREATE TABLE injury_stoppage (
    event_id CHAR(36) PRIMARY KEY,
    in_chain BOOLEAN,

    FOREIGN KEY (event_id) REFERENCES events (event_id)
);

DROP TABLE IF EXISTS miscontrol;
CREATE TABLE miscontrol (
    event_id CHAR(36) PRIMARY KEY,
    aerial_won BOOLEAN,

    FOREIGN KEY (event_id) REFERENCES events (event_id)
);

DROP TABLE IF EXISTS player_off;
CREATE TABLE player_off (
    event_id CHAR(36) PRIMARY KEY,
    permanent BOOLEAN,

    FOREIGN KEY (event_id) REFERENCES events (event_id)
);

DROP TABLE IF EXISTS substitution;
CREATE TABLE substitution (
    event_id CHAR(36) PRIMARY KEY,
    replacement_id INTEGER,

    FOREIGN KEY (event_id) REFERENCES events (event_id)
);

                    