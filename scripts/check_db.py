import psycopg2
import pickle

conn = psycopg2.connect('postgresql://catanatron:victorypoint@localhost:5432/catanatron_db')
cur = conn.cursor()
uuid = '5bbfd4b4-83ca-4dd6-b3d8-f0db44f1c032'

cur.execute(f"SELECT state_index, pickle_data FROM game_states WHERE uuid='{uuid}' ORDER BY state_index")
rows = cur.fetchall()

print(f"Length of actions at middle:")
for index, pickle_data in rows[230:245]:
    game = pickle.loads(pickle_data)
    last_act = game.state.action_records[-1].action if len(game.state.action_records) > 0 else "None"
    vps = game.state.player_state
    blue_vps = vps.get('P1_ACTUAL_VICTORY_POINTS', 0)
    red_vps = vps.get('P0_ACTUAL_VICTORY_POINTS', 0)
    print(f"Index {index}: (Blue VPs: {blue_vps}, Red VPs: {red_vps}) last_action={last_act}")

# find EXACT index it won using json payload
cur.execute(f"SELECT state_index, state FROM game_states WHERE uuid='{uuid}' ORDER BY state_index")
json_rows = cur.fetchall()

for idx, state_json in json_rows[230:245]:
    import json
    data = json.loads(state_json)
    if data.get('winning_color') is not None:
        print(f"JSON says winner at {idx}: {data['winning_color']}")
