CREATE INDEX pass_recipient_index ON pass(competition_id, season_id, recipient_id);
CREATE INDEX pass_technique_index ON pass(competition_id, season_id, technique);
CREATE INDEX shots_first_time ON shot(competition_id, season_id, first_time, player_id);
CREATE INDEX shots_competition_player ON shot(competition_id, season_id, player_id); 
CREATE INDEX shots_competition_team ON shot(competition_id, season_id, team_id); 
CREATE INDEX pass_competition_player ON pass(competition_id, season_id, player_id);
CREATE INDEX pass_competition_team ON pass(competition_id, season_id, team_id);
CREATE INDEX dribble_competition_player ON dribble(competition_id, season_id, outcome, player_id);
CREATE INDEX dribble_past_comp_player ON dribbled_past(competition_id, season_id, player_id);