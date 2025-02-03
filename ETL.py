import glob   
import pandas as pd       
import xml.etree.ElementTree as ET
from datetime import datetime
from arg import get_input
import os



## Extraire les données json
def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process,lines=True)
    return dataframe

## Extraire les données csv
def extract_from_csv(file_to_process):
    dataframe = pd.read_csv(file_to_process)
    return dataframe


## Extraire des données de xml
def extract_from_xml(file_to_process):
    
    tree = ET.parse(file_to_process)
    root = tree.getroot()
    for person in root:
        name = person.find("name").text
        height = float(person.find("height").text)
        weight = float(person.find("weight").text)
        dataframe = pd.DataFrame({"name":name, "height":height, "weight":weight}  , index=range(len(root)))
    return dataframe


## Extraire tous les fichoers dans le dossiers.
def extract(data_dir):
   
    
    #Extraire tous les fichiers csv
    
    for csvfile in glob.glob(data_dir+"*.csv"):
        extracted_data = extract_from_csv(csvfile)
        
    #Extraire tous les fichiers json
    for jsonfile in glob.glob(data_dir+"*.json"):
        extracted_data = pd.concat([extracted_data, extract_from_json(jsonfile)], ignore_index=True)
    
    #Extraire tous les fichiers xml
    for xmlfile in glob.glob(data_dir+"*.xml"):
        extracted_data = pd.concat([extracted_data, extract_from_xml(xmlfile)], ignore_index=True)
        
    return extracted_data

## Log des fichiers extraits
def log(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Année-nom du mois-Jour-Hour-Minute-Seconde
    now = datetime.now() # get actual time
    timestamp = now.strftime(timestamp_format)
    with open("logfile.txt","a") as f:
        f.write(timestamp + ',' + message + '\n')


## Charger les données dans une autre source
def load(targetfile,data_to_load):
 
    data_to_load.to_csv(targetfile, index=False)  


if __name__=="__main__":
    args=get_input()
    print("Extraction start")
    log('Extraction start')
    data_extract=extract(data_dir=args.datadir)
  
    print("Loading start")
    log('Loading start')
    os.chdir(args.outputdir)
    load(args.targetfile, data_extract)
    os.chdir("..")
    log("Extraction ending successfully")  
    print('Extraction ending successfully')
  
