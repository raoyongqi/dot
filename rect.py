import pandas as pd

# Read Excel files
location_df = pd.read_excel('data/1_Alldata.xlsx', sheet_name='Lacation')
site_data = pd.read_excel("data/1_Alldata.xlsx", sheet_name="Plotdata")

# Drop 'site' column if it exists
if 'site' in site_data.columns:
    site_data = site_data.drop(columns=['site'])

# Rename 'Site' column to 'site' if it exists
if 'Site' in site_data.columns:
    site_data = site_data.rename(columns={'Site': 'site'})

# Lowercase all columns in location_df
location_df.columns = [col.lower() for col in location_df.columns]

# Merge data
merged_df = pd.merge(site_data, location_df, left_on="site", right_on="site")

merged_df = merged_df[['site','Plot','PL','lat',
    'lon']]

grouped_df =merged_df.groupby(['site', 'lat', 'lon'])['PL'].apply(lambda x: list(x)).reset_index()

# 为每个 'site' 和 'Plot' 创建新的列名
grouped_df['PL'] = grouped_df['PL'].apply(lambda pl_list: {f'PL_{i+1}': pl for i, pl in enumerate(pl_list)})

# 将 'PL' 列展开为多个列
pl_expanded_df = pd.json_normalize(grouped_df['PL'])
result_df = pd.concat([grouped_df.drop(columns=['PL']), pl_expanded_df], axis=1)

# 重新排列列顺序，确保列名按 'site' 和 'Plot' 排序
sorted_columns = sorted(result_df.columns)
result_df = result_df[sorted_columns]
def to_js_format(grouped_df):
    capitals = []
    for _, row in grouped_df.iterrows():
        site = row['site']
        pl_values = row['PL']
        center = [row['lon'], row['lat']]
        capitals.append({
            "site": str(site),
            "PL": pl_values,
            "center": center
        })
    return capitals

capitals = to_js_format(grouped_df)
import json
formatted_capitals = json.dumps(capitals, indent=4)

# 输出为 JavaScript 文件
js_content = f"export const capitals = {formatted_capitals};"
with open('site.js', 'w') as file:
    file.write(js_content)