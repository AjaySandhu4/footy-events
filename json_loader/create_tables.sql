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
    country_name TEXT NOT NULL
);

DROP TABLE IF EXISTS team;
CREATE TABLE team (
    team_id INTEGER PRIMARY KEY,
    team_name CHAR(24) NOT NULL,
    team_country CHAR(24) NOT NULL
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
    FOREIGN KEY (away_team_id) REFERENCES team (team_id)
    -- FOREIGN KEY (home_manager_id) REFERENCES manager (manager_id),
    -- FOREIGN KEY (away_manager_id) REFERENCES manager (manager_id)
    -- FOREIGN KEY (referee_id) REFERENCES referee (referee_id)
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
    -- possession_team CHAR(24) NOT NULL,
    play_pattern CHAR(24) NOT NULL,
    -- team_name CHAR(24) NOT NULL,
    team_id INTEGER NOT NULL,
    -- player_name TEXT NOT NULL,
    player_id INTEGER,
    position TEXT,
    location_x DECIMAL,
    location_y DECIMAL,
    duration DECIMAL,
    under_pressure BOOLEAN,
    off_camera BOOLEAN,
    ball_out BOOLEAN,
    -- related_events CHAR(36),

    FOREIGN KEY (match_id) REFERENCES matches (match_id),
    FOREIGN KEY (player_id) REFERENCES player (player_id)
    -- FOREIGN KEY (related_events) REFERENCES events (event_id)
);


DROP TABLE IF EXISTS shot;
CREATE TABLE shot (
    event_id CHAR(36) PRIMARY KEY,
    -- season_name CHAR(24) NOT NULL,
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
    outcome CHAR(20),

    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (key_pass_id) REFERENCES events (event_id)
);

-- DROP TABLE IF EXISTS pass;
-- CREATE TABLE pass (
--     event_id CHAR(36) PRIMARY KEY,
--     match_id INTEGER NOT NULL,
--     season_name CHAR(24) NOT NULL,
--     -- player_name TEXT NOT NULL,
--     recipient_name TEXT NOT NULL,
--     pass_length DECIMAL NOT NULL,
--     angle DECIMAL NOT NULL,
--     height CHAR(24) NOT NULL,
--     end_location_x DECIMAL NOT NULL,
--     end_location_y DECIMAL NOT NULL,
--     is_cross BOOLEAN,
--     switch BOOLEAN,
--     shot_assist BOOLEAN,
--     cutback BOOLEAN,
--     backheel BOOLEAN,
--     deflected BOOLEAN,
--     miscommunication BOOLEAN,
--     outcome CHAR(10),
--     body_part CHAR(24),
--     pass_type CHAR(24),
--     technique CHAR(24),

--     FOREIGN KEY (event_id) REFERENCES events (event_id)
-- );

-- DROP TABLE IF EXISTS dribble;
-- CREATE TABLE dribble (
--     event_id CHAR(36) PRIMARY KEY,
--     match_id INTEGER NOT NULL,
--     outcome CHAR(24) NOT NULL,
--     overrun BOOLEAN,
--     no_touch BOOLEAN
-- );

-- DROP TABLE IF EXISTS dribbled_past;
-- CREATE TABLE dribbled_past (
--     event_id CHAR(36) PRIMARY KEY,
--     match_id INTEGER NOT NULL,
--     counterpress BOOLEAN
-- );

-- CREATE TABLE ball_receipt;
-- CREATE TABLE ball_recovery;
-- CREATE TABLE dispossessed;
-- CREATE TABLE duel;
-- CREATE TABLE camera_on;
-- CREATE TABLE block;
-- CREATE TABLE offside;
-- CREATE TABLE clearance;
-- CREATE TABLE interception;
-- CREATE TABLE pressure;
-- CREATE TABLE half_start;
-- CREATE TABLE substitution;
-- CREATE TABLE own_goal_against;
-- CREATE TABLE foul_won;
-- CREATE TABLE foul_committed;
-- CREATE TABLE goalkeeper;
-- CREATE TABLE bad_behaviour;
-- CREATE TABLE own_goal_for;
-- CREATE TABLE player_on;
-- CREATE TABLE player_off;
-- CREATE TABLE shield;
-- CREATE TABLE fifty_fifty;
-- CREATE TABLE half_end;
-- CREATE TABLE starting_xi;
-- CREATE TABLE tactical_shift;
-- CREATE TABLE error;
-- CREATE TABLE miscontrol;
-- CREATE TABLE injury_stoppage;
-- CREATE TABLE referee_ball_drop;
-- CREATE TABLE carry;

                    