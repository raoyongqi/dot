import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer

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

# Calculate the average lat, lon, and PL for each site
grouped_df = merged_df.groupby('site').agg({
    'lat': 'mean',
    'lon': 'mean',
    'PL': 'mean'
}).reset_index()

# Initialize KBinsDiscretizer
discretizer = KBinsDiscretizer(n_bins=4, encode='ordinal', strategy='uniform')

# Fit and transform PL values
grouped_df['PL_category'] = discretizer.fit_transform(grouped_df[['PL']]).astype(int)

# Map categories to colors
category_colors = {
    0: 'green',
    1: 'yellow',
    2: 'orange',
    3: 'red'
}
grouped_df['color'] = grouped_df['PL_category'].map(category_colors)

# Prepare data for JavaScript
grouped_data = grouped_df[['lat', 'lon', 'PL', 'site', 'color']].dropna().to_dict(orient="records")

# Generate JavaScript code
js_code = 'export const capitals = [\n'

for row in grouped_data:
    site = f'"{row["site"]}"'
    center = f'[{row["lon"]}, {row["lat"]}]'
    pl = f'"{row["PL"]}"'
    color = f'"{row["color"]}"'
    js_code += f'  {{"site": {site}, "PL": {pl}, "center": {center}, "color": {color}}},\n'
js_code += '];\n'

# Write to JS file
JS_LOC = 'my-map-app/src/site.js'
with open(JS_LOC, 'w') as file:
    file.write(js_code)

print(f"JavaScript code has been written to {JS_LOC}")
