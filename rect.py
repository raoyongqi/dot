import pandas as pd
import requests
import json

# 定义函数，从 API 响应中提取省、市、县信息
def get_address_components(location, key):
    url = f"https://restapi.amap.com/v3/geocode/regeo?location={location}&key={key}&radius=1000&extensions=all"
    response = requests.get(url)
    data = response.json()
    if "regeocode" in data and "addressComponent" in data["regeocode"]:
        address_component = data["regeocode"]["addressComponent"]
        province = address_component.get("province", "")
        city = address_component.get("city", "")
        district = address_component.get("district", "")
        return province, city, district
    return "", "", ""

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

# Create a new column for the location string
merged_df['location'] = merged_df.apply(lambda row: f"{row['lon']},{row['lat']}", axis=1)

# API key for Amap
api_key = "634d7ad3bd0bfeb370acfa403505291e"

# Extract address components and add to dataframe
address_components = merged_df['location'].apply(lambda loc: get_address_components(loc, api_key))
address_df = pd.DataFrame(address_components.tolist(), columns=['province', 'city', 'district'])
merged_df = pd.concat([merged_df, address_df], axis=1)

# Group by site and calculate average PL values
grouped_df = merged_df.groupby(['site', 'lat', 'lon', 'province', 'city', 'district'])['PL'].apply(lambda x: list(x)).reset_index()

# Create new columns for each 'site' and 'Plot'
grouped_df['PL'] = grouped_df['PL'].apply(lambda pl_list: {f'PL_{i+1}': pl for i, pl in enumerate(pl_list)})

# Expand 'PL' column into multiple columns
pl_expanded_df = pd.json_normalize(grouped_df['PL'])
result_df = pd.concat([grouped_df.drop(columns=['PL']), pl_expanded_df], axis=1)

# Convert data to JavaScript format with address components
def to_js_format(grouped_df):
    capitals = []
    for _, row in grouped_df.iterrows():
        site = row['site']
        pl_values = {col: row[col] for col in grouped_df.columns if col.startswith('PL_')}
        center = [row['lon'], row['lat']]
        capitals.append({
            "site": str(site),
            "PL": pl_values,
            "center": center,
            "province": str(row['province']),
            "city": str(row['city']),
            "district": str(row['district'])
        })
    return capitals

capitals = to_js_format(result_df)
formatted_capitals = json.dumps(capitals, indent=4)

# Write to JavaScript file
js_content = f"export const capitals = {formatted_capitals};"
with open('site.js', 'w') as file:
    file.write(js_content)

print(f"JavaScript file 'site.js' has been written with address components included.")
