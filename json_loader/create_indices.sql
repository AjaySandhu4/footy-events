CREATE INDEX events_type_index ON events(competition_id, event_type, outcome);
CREATE INDEX events_competition_index ON events(competition_id,season_id);
CREATE INDEX events_competition_index2 ON events(competition_id);
CREATE INDEX pass_recipient_index ON pass(recipient_id);
CREATE INDEX shots_first_time ON shot(first_time);
CREATE INDEX outcome_index ON events(outcome);