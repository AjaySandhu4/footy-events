CREATE INDEX events_type_index ON events(event_type, competition_id);
CREATE INDEX events_competition_index ON events(competition_id,season_id);