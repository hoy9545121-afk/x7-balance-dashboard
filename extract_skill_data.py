import csv
import pandas as pd

def extract_data():
    skill_list_path = r'C:\AI_simulator\기획 참고용\[X7] 스킬 밸런스 - 스킬 리스트.csv'
    skill_damage_path = r'C:\AI_simulator\스킬 데이터용 csv\skill_damage.csv'
    skill_info_path = r'C:\AI_simulator\스킬 데이터용 csv\skill_info.csv'

    # Read skill list
    skill_list = pd.read_csv(skill_list_path)
    group_ids = skill_list['스킬 GroupId'].astype(str).tolist()

    # Read skill damage
    # We use root_id as the key. 
    # Since there might be multiple nodes for a root_id, we'll take the first one that has root_type == 'skill_root' or just the first one if not found.
    # Actually, skill_damage often has multiple hits. But usually skill_root entry in skill_damage is the primary one.
    damage_df = pd.read_csv(skill_damage_path)
    damage_dict = {}
    for rid in group_ids:
        # Filter by root_id (as string or int)
        match = damage_df[damage_df['root_id'].astype(str) == rid]
        if not match.empty:
            # Prefer skill_root
            skill_root_match = match[match['root_type'] == 'skill_root']
            if not skill_root_match.empty:
                damage_dict[rid] = skill_root_match.iloc[0]['skill_d_m_g_minper']
            else:
                damage_dict[rid] = match.iloc[0]['skill_d_m_g_minper']
        else:
            damage_dict[rid] = "N/A"

    # Read skill info for cooldown
    info_df = pd.read_csv(skill_info_path)
    cooltime_dict = {}
    for rid in group_ids:
        match = info_df[info_df['root_id'].astype(str) == rid]
        if not match.empty:
            # skill_info also has multiple nodes, root_type 'skill_root' usually contains the cooltime
            skill_root_match = match[match['root_type'] == 'skill_root']
            if not skill_root_match.empty:
                cooltime_dict[rid] = skill_root_match.iloc[0]['cooltime']
            else:
                cooltime_dict[rid] = match.iloc[0]['cooltime']
        else:
            cooltime_dict[rid] = "N/A"

    # Combine results
    results = []
    for index, row in skill_list.iterrows():
        rid = str(row['스킬 GroupId'])
        results.append({
            'Category': row['장비 구분'],
            'Command': row['커맨드'],
            'GroupId': rid,
            'Damage': damage_dict.get(rid, "N/A"),
            'Cooldown': cooltime_dict.get(rid, "N/A")
        })

    return results

if __name__ == "__main__":
    data = extract_data()
    # Format as table
    # I'll group by Weapon and Command to show 1T, 2T, 3T together
    # Data structure: Category is "1티어 한손검", etc.
    
    formatted_data = []
    # Extract weapon name
    def get_weapon(cat):
        return cat.split(' ')[1] if ' ' in cat else cat
    
    def get_tier(cat):
        return cat.split(' ')[0] if ' ' in cat else cat

    weapons = ["한손검", "양손검", "지팡이", "단검", "활"]
    commands = ["Q", "W", "E", "R"]
    
    table = []
    for weapon in weapons:
        for cmd in commands:
            row_data = {"Weapon": weapon, "Command": cmd}
            for tier, tier_prefix in [("1티어", "1T"), ("2티어", "2T"), ("3티어", "3T")]:
                match = next((item for item in data if weapon in item['Category'] and tier in item['Category'] and item['Command'] == cmd), None)
                if match:
                    row_data[f"{tier_prefix}_Dmg"] = match['Damage']
                    row_data[f"{tier_prefix}_CD"] = match['Cooldown']
                else:
                    row_data[f"{tier_prefix}_Dmg"] = "-"
                    row_data[f"{tier_prefix}_CD"] = "-"
            table.append(row_data)
            
    # Manually print markdown table
    headers = ["Weapon", "Command", "1T_Dmg", "1T_CD", "2T_Dmg", "2T_CD", "3T_Dmg", "3T_CD"]
    header_str = "| " + " | ".join(headers) + " |"
    sep_str = "| " + " | ".join(["---"] * len(headers)) + " |"
    print(header_str)
    print(sep_str)
    
    for row in table:
        row_str = "| " + " | ".join([str(row.get(h, "-")) for h in headers]) + " |"
        print(row_str)
