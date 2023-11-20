import pandas as pd
target_file = "data/OFEI1204.txt"
file = open(target_file,"r")
lines = file.readlines()
current_agent = ""
file.close()
table = []
for line in lines:
    normalized_line = line.lower().strip()
    if "agente" in normalized_line:
        current_agent = normalized_line.split(":")[-1].strip()
        continue
    raw_data = normalized_line.split(",")
    clean_data = [register.strip() for register in raw_data]
    if len(clean_data) <= 1:
        continue
    if clean_data[1] != "d":
        continue
    new_row = {
        "agente":current_agent,
        "planta":clean_data[0],
    }
    hours = {f"hora_{i+1}":dato for i,dato in enumerate(clean_data[2:])}
    new_row.update(hours)
    table.append(new_row)
output = pd.DataFrame(table)
output.to_csv("reto1.csv")