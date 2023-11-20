import chardet
import pandas as pd

def read_txt_to_dataframe(target_file:str)->pd.DataFrame:
    output = []
    raw_file = open(target_file,"rb")
    raw_data = raw_file.readlines()
    raw_file.close()
    for data in raw_data:
        pre_processed_data = data.decode(chardet.detect(data)["encoding"])
        #print(data.decode("ascii"))
        processed_data = pre_processed_data.replace('"',"").strip().split(",")
        if processed_data[0] == "Total":
            break
        new_row = {
            "CENTRAL (dDEC, dSEGDES, dPRU…)":processed_data[0]
        }
        hours = {f"hora_{i+1}":float(dato) for i,dato in enumerate(processed_data[1:])}
        hours["total"] = sum(hours.values())
        new_row.update(hours)
        output.append(new_row)
    return pd.DataFrame(output)

dataset_1 = pd.read_excel("data/Datos Maestros VF.xlsx",dtype=None)
print(dataset_1.columns)
relevant_rows = [
    "Nombre visible Agente",
    "AGENTE (OFEI)",
    "CENTRAL (dDEC, dSEGDES, dPRU…)",
    'Tipo de central (Hidro, Termo, Filo, Menor)',
]

pre_processed_dataset = dataset_1[relevant_rows]
#pre_processed_dataset = pre_processed_dataset.drop_duplicates()
filtered_dataset = pre_processed_dataset[
    (("EMGESA" == pre_processed_dataset["Nombre visible Agente"]) | ("EMGESA S.A." == pre_processed_dataset["Nombre visible Agente"])) & 
    (("T" == pre_processed_dataset['Tipo de central (Hidro, Termo, Filo, Menor)'])| ("H" == pre_processed_dataset["Tipo de central (Hidro, Termo, Filo, Menor)"]))
    ]

dataset_2 = read_txt_to_dataframe("data/dDEC1204.TXT")
join_dataset = pd.merge(filtered_dataset,dataset_2,on="CENTRAL (dDEC, dSEGDES, dPRU…)",how="inner")
final_dataset = join_dataset[join_dataset["total"] > 0]
final_dataset.to_csv("reto2.csv")
