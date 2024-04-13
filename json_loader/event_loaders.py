import psycopg
from pprint import pprint

def load_shot(db_conn, event_id, shot_event, competition_id, season_id, player_id, team_id):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO shot (
            event_id, 
            competition_id,
            season_id,
            player_id,
            team_id,
            key_pass_id, 
            end_location_x, 
            end_location_y, 
            end_location_z, 
            aerial_won, 
            follows_dribble, 
            first_time, 
            open_goal, 
            statsbomb_xg, 
            deflected, 
            technique, 
            body_part, 
            shot_type
            ) 
            VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            event_id, 
            competition_id,
            season_id,
            player_id,
            team_id,
            shot_event.get('key_pass_id'), 
            shot_event.get('end_location')[0] if shot_event.get('end_location') else None, 
            shot_event.get('end_location')[1] if shot_event.get('end_location') else None, 
            shot_event.get('end_location')[2] if shot_event.get('end_location') and len(shot_event.get('end_location')) > 2 else None, 
            shot_event.get('aerial_won'), 
            shot_event.get('follows_dribble'), 
            shot_event.get('first_time'), 
            shot_event.get('open_goal'), 
            shot_event.get('statsbomb_xg'), 
            shot_event.get('deflected'), 
            shot_event.get('technique', {}).get('name'), 
            shot_event.get('body_part', {}).get('name'), 
            shot_event.get('type', {}).get('name')
        ))

def load_pass(db_conn, event_id, pass_event, competition_id, season_id, player_id, team_id):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO pass (
            event_id, 
            competition_id,
            season_id,
            player_id,
            team_id,
            recipient_id, 
            pass_length, 
            angle, 
            height, 
            end_location_x, 
            end_location_y, 
            is_cross, 
            switch, 
            shot_assist,
            goal_assist,
            cutback,
            backheel,
            deflected,
            miscommunication,
            body_part,
            pass_type,
            technique 
            ) VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            event_id, 
            competition_id,
            season_id,
            player_id,
            team_id,
            pass_event.get('recipient', {}).get('id'), 
            pass_event.get('length'), 
            pass_event.get('angle'), 
            pass_event.get('height', {}).get('name'), 
            pass_event.get('end_location')[0] if pass_event.get('end_location') else None, 
            pass_event.get('end_location')[1] if pass_event.get('end_location') else None, 
            pass_event.get('cross'), 
            pass_event.get('switch'), 
            pass_event.get('shot-assist'), 
            pass_event.get('goal-assit'),
            pass_event.get('cut_back'), 
            pass_event.get('backheel'), 
            pass_event.get('deflected'), 
            pass_event.get('miscommunication'), 
            pass_event.get('body_part', {}).get('name'), 
            pass_event.get('type', {}).get('name'), 
            pass_event.get('technique', {}).get('name')
        ))

def load_dribble(db_conn, event_id, dribble_event, competition_id, season_id, player_id, team_id):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO dribble (
            event_id, 
            competition_id,
            season_id,
            player_id,
            outcome,
            overrun, 
            no_touch,
            nutmeg
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            event_id, 
            competition_id,
            season_id,
            player_id,
            dribble_event.get('outcome', {}).get('name'),
            dribble_event.get('overrun'), 
            dribble_event.get('no_touch'), 
            dribble_event.get('nutmeg')
        ))

def load_dribbled_past(db_conn, event_id, dribbled_past_event, competition_id, season_id, player_id, team_id):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO dribbled_past (
            event_id, 
            competition_id,
            season_id,
            player_id
            ) VALUES (%s, %s, %s, %s)
        ''', (
            event_id, 
            competition_id,
            season_id,
            player_id
        ))


def load_bad_behaviour(db_conn, event_id, bad_behaviour_event):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO bad_behaviour (
            event_id, 
            card_name 
            ) VALUES (%s, %s)
        ''', (
            event_id, 
            bad_behaviour_event.get('card', {}).get('name'), 
        ))

def load_ball_recovery(db_conn, event_id, ball_recovery_event):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO ball_recovery (
            event_id, 
            offensive,
            recovery_failure
            ) VALUES (%s, %s, %s)
        ''', (
            event_id, 
            ball_recovery_event.get('offensive'),
            ball_recovery_event.get('recovery_failure')
        ))

def load_blocks(db_conn, event_id, block_event):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO blocks (
            event_id, 
            deflection,
            offensive,
            save_block
            ) VALUES (%s, %s, %s, %s)
        ''', (
            event_id, 
            block_event.get('deflection'),
            block_event.get('offensive'),
            block_event.get('save_block')
        ))

def load_carry(db_conn, event_id, carry_event):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO carry (
            event_id, 
            end_location_x,
            end_location_y
            ) VALUES (%s, %s, %s)
        ''', (
            event_id, 
            carry_event.get('end_location')[0] if carry_event.get('end_location') else None, 
            carry_event.get('end_location')[1] if carry_event.get('end_location') else None, 
        ))

def load_clearance(db_conn, event_id, clearance_event):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO clearance (
            event_id, 
            aerial_won,
            body_part
            ) VALUES (%s, %s, %s)
        ''', (
            event_id, 
            clearance_event.get('aerial_won'),
            clearance_event.get('body_part', {}).get('name'),
        ))

def load_duel(db_conn, event_id, duel_event):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO duel (
            event_id, 
            duel_type
            ) VALUES (%s, %s)
        ''', (
            event_id, 
            duel_event.get('type', {}).get('name'),
        ))

def load_foul_committed(db_conn, event_id, foul_committed_event):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO foul_committed (
            event_id, 
            foul_type,
            card_name,
            advantage,
            penalty,
            offensive        
            ) VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            event_id, 
            foul_committed_event.get('type', {}).get('name'),
            foul_committed_event.get('card', {}).get('name'),
            foul_committed_event.get('advantage'),
            foul_committed_event.get('penalty'),
            foul_committed_event.get('offensive'),
        ))

def load_foul_won(db_conn, event_id, foul_won_event):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO foul_won (
            event_id, 
            defensive,
            penalty,
            advantage
            ) VALUES (%s, %s, %s, %s)
        ''', (
            event_id, 
            foul_won_event.get('defensive'),
            foul_won_event.get('penalty'),
            foul_won_event.get('advantage'),
        ))

def load_goalkeeper(db_conn, event_id, goalkeeper_event):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO goalkeeper (
            event_id, 
            position,
            body_part,
            goalkeeper_type,
            technique
            ) VALUES (%s, %s, %s, %s, %s)
        ''', (
            event_id, 
            goalkeeper_event.get('position', {}).get('name'),
            goalkeeper_event.get('body_part', {}).get('name'),
            goalkeeper_event.get('type', {}).get('name'),
            goalkeeper_event.get('technique', {}).get('name'),
        ))

def load_half_end(db_conn, event_id, half_end_event):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO half_end (
            event_id, 
            early_video_end,
            match_suspended
            ) VALUES (%s, %s, %s)
        ''', (
            event_id, 
            half_end_event.get('early_video_end'),
            half_end_event.get('match_suspended')
        ))

def load_half_start(db_conn, event_id, half_start_event):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO half_start (
            event_id, 
            late_video_start
            ) VALUES (%s, %s)
        ''', (
            event_id, 
            half_start_event.get('late_video_start')
        ))

def load_injury_stoppage(db_conn, event_id, injury_stoppage_event):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO injury_stoppage (
            event_id, 
            in_chain
            ) VALUES (%s, %s)
        ''', (
            event_id, 
            injury_stoppage_event.get('in_chain')
        ))

def load_miscontrol(db_conn, event_id, miscontrol_event):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO miscontrol (
            event_id, 
            aerial_won
            ) VALUES (%s, %s)
        ''', (
            event_id, 
            miscontrol_event.get('aerial_won')
        ))

def load_player_off(db_conn, event_id, player_off_event):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO player_off (
            event_id, 
            permanent
            ) VALUES (%s, %s)
        ''', (
            event_id, 
            player_off_event.get('permanent')
        ))

def load_substitution(db_conn, event_id, substitution_event):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO substitution (
            event_id, 
            replacement_id
            ) VALUES (%s, %s)
        ''', (
            event_id, 
            substitution_event.get('replacement', {}).get('id'),
        ))