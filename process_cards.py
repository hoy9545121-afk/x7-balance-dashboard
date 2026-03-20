import pandas as pd
import ast

def parse_list(x):
    if pd.isna(x):
        return []
    if isinstance(x, str):
        # Remove brackets and split by comma
        x = x.strip()
        if x.startswith('[') and x.endswith(']'):
            x = x[1:-1]
        if not x:
            return []
        return [c.strip() for c in x.split(',')]
    return [str(int(x))]

# Paths
excel_path = r'C:\AI_simulator\기획서\X7_몬스터_카드_아이템_목록.xlsx'
loot_data_path = r'C:\AI_simulator\게임 데이터 전체_원본.csv\LootData.csv'
loot_dataset_path = r'C:\AI_simulator\게임 데이터 전체_원본.csv\LootDataSet.csv'
loot_group_path = r'C:\AI_simulator\게임 데이터 전체_원본.csv\LootGroup.csv'

# Load Excel
df_excel = pd.read_excel(excel_path, sheet_name='📋 전체 카드 목록', header=1)
df_excel = df_excel.dropna(subset=['Cid'])
df_excel['Cid'] = df_excel['Cid'].astype(int)

# Load CSVs
df_loot = pd.read_csv(loot_data_path)
df_dataset = pd.read_csv(loot_dataset_path)
df_group = pd.read_csv(loot_group_path)

# Prepare lists in CSVs
df_dataset['LootDataCids_list'] = df_dataset['LootDataCids'].apply(parse_list)
df_group['LootDataSetCids_list'] = df_group['LootDataSetCids'].apply(parse_list)

results = []

for _, row in df_excel.iterrows():
    card_name = row['카드명']
    card_cid = int(row['Cid'])
    
    # Find matching LootData entries
    loot_matches = df_loot[df_loot['Value'] == card_cid]
    
    for _, l_row in loot_matches.iterrows():
        loot_cid = int(l_row['Cid'])
        
        # Find matching LootDataSet
        mask = df_dataset['LootDataCids_list'].apply(lambda x: str(loot_cid) in x)
        matching_datasets = df_dataset[mask]
        
        for _, ds_row in matching_datasets.iterrows():
            ds_cid = int(ds_row['Cid'])
            
            # Find matching LootGroup
            group_mask = df_group['LootDataSetCids_list'].apply(lambda x: str(ds_cid) in x)
            matching_groups = df_group[group_mask]
            
            for _, lg_row in matching_groups.iterrows():
                results.append({
                    'Monster/Region/Race': card_name.replace(' 카드', ''),
                    'Card Item Name': card_name,
                    'Item Cid': card_cid,
                    'LootData Cid': loot_cid,
                    'LootDataSet Cid': ds_cid,
                    'LootGroup Cid': int(lg_row['Cid']),
                    'LootGroup Comment': lg_row['Comment']
                })

if results:
    df_results = pd.DataFrame(results)
    # De-duplicate
    df_results = df_results.drop_duplicates()
    print(df_results.to_string(index=False))
else:
    print("No matching LootGroups found.")
