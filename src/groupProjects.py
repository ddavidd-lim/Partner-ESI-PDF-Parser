from classes import SectionFieldsMap
import mapping
import pandas as pd
import os
import copy

def xlsxToDf(file: str) -> pd.DataFrame:
    '''
    Reads Excel file and returns information as a pandas Dataframe.

    Parameters:
        file (str): path to the Excel file.

    Returns:
        pd.DataFrame: DataFrame containing the Excel fle data.
    '''
    try:
        cwd = os.getcwd()
        file_path = os.path.join(cwd, "..", "data", "raw", file)
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print("An error occurred:", e)
        return None 
    
# returns set of reports
df = xlsxToDf('ESA_DATA.xlsx')
sub = df['project_number_string']
reports = set(each for each in sub)
print(len(reports))
new_df = df[df['the_data'].notna()] # DF OF DATA WITH DROPPED NULLS
print(new_df)


# TODO: set a dict to have all report num to SFM object
d = dict()
obj = mapping.execute()
for each in reports:
    temp = copy.deepcopy(obj)
    d[each] = temp 
#print(d) # d is a dict of {report_num: SFM}


hold = dict()
for i,row in new_df.iterrows():
    if row["project_number_string"] in hold:
        hold[row["project_number_string"]].append((row["document_spot"], row["the_data"]))
    else:
        hold[row["project_number_string"]] = []
for k,v in hold.items():
    inner = {data[0]:data[1] for data in v}
    d[k].fields = inner

print(d['22-390859.7'].fields) # testing for report answer dict 


# TODO: return dict of {report number: sectionfieldsmap} containing all the reports