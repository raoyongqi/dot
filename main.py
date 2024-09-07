import pandas as pd

# 读取 Excel 文件
df = pd.read_excel('data/1_Alldata.xlsx',sheet_name='Lacation')


# 生成 JavaScript 代码
js_code = 'export const capitals = [\n'


for _, row in df.iterrows():
    site = f'"{row["Site"]}"'
    center = f'[{row["LON"]}, {row["LAT"]}]'
    js_code += f'  {{"site": {site}, "center": {center} }},\n'
js_code += '];\n'

# 写入到 JS 文件

JS_LOC = 'site.js'
with open(JS_LOC, 'w') as file:
    file.write(js_code)

print(f"JavaScript code has been written to {JS_LOC}")
