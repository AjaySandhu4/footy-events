import psycopg
from pprint import pprint

def load_shot(db_conn, event_id, shot_event, match_id, season_name):
    with db_conn.cursor() as cursor:
        # cursor.execute('''INSERT INTO shot (event_id, match_id, season_name, player_name, xg) VALUES (%s, %s, %s, %s, %s);''', (shot_event['id'], match_id, season_name, shot_event['player']['name'], shot_event['shot']['statsbomb_xg']))
        cursor.execute('''
            INSERT INTO shot (
            event_id, 
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
            shot_type, 
            outcome
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            event_id, 
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
            shot_event.get('type', {}).get('name'), 
            shot_event.get('outcome', {}).get('name')
        ))

def load_pass(db_conn, event_id, pass_event, match_id, season_name):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO pass (
            event_id, 
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
            outcome,
            body_part,
            pass_type,
            technique 
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            event_id, 
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
            pass_event.get('outcome', {}).get('name'), 
            pass_event.get('body_part', {}).get('name'), 
            pass_event.get('type', {}).get('name'), 
            pass_event.get('technique', {}).get('name')
        ))

def load_dribble(db_conn, event_id, pass_event, match_id, season_name):
    with db_conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO dribble (
            event_id, 
            outcome, 
            overrun, 
            no_touch,
            nutmeg
            ) VALUES (%s, %s, %s, %s, %s)
        ''', (
            event_id, 
            pass_event.get('outcome', {}).get('name'), 
            pass_event.get('overrun'), 
            pass_event.get('no_touch'), 
            pass_event.get('nutmeg'), 
        ))