from classes import SectionFieldsMap as sfm
import pandas as pd
import os


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
        file_path = os.path.join(cwd, "data", "raw", file)
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print("An error occurred:", e)
        return None  
    

def checkSection(value, section: str) -> bool:
    '''
    Checks if the value belongs to specified subsection.

    Parameters:
        value (int, str, float): the value in DataFrame to check.
        section (str): the report section number to check against.

    Returns:
        bool: True if value is included in subsection, False otherwise.
    '''
    test = str(value).split(".")
    check = str(section).split(".")
    
    if test == check:
        return True  
    if len(test) > 5:
        last_sub = test[:5]
        return last_sub == check 
    return False


def fieldMapping(df: pd.DataFrame) -> dict:
    '''
    Creates mapping of valid field values to their corresponding descriptions in DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing rows related to Esa Reports and report section.

    Returns:
        dict: Dictionary mapping {"field_value_code": "description"} of rows.
    '''
    questions = {} 
    for index, row in df.iterrows():
        questions[row["Name"]] = row["Description"]
    return questions


def createSections(df: pd.DataFrame) -> sfm.SectionFieldsMap:
    '''
    Generates dictionary containing all sections in ESA reports and their data.

    Parameters:
        df (pd.DataFrame): DataFrame containing rows related to Esa Reports and report section.

    Returns:
        sfm.SectionFieldsMap: Object with dictionary mapping {subsection_num: {field: descript.}}} for all subsections.
    '''
    sub_df = df['Section'].dropna()
    #section_set = set(sub_df)
    edited = set(str(each) for each in sub_df)

    data = {}
    for sec in edited:
        mapping = fieldMapping(df)
        data[sec] = mapping
        
    subsections = sfm.SectionFieldsMap(data)
    return subsections

# call to retrieve mapping for front-end, runs independent of execute()
def mappingForHover() -> dict:
    '''
    Generates field value dictionary to be used for the hover front-end feature.

    Returns:
        dict: Dictionary mapping {field: descript.} of all ESA fields.
    '''
    excel_file = 'scraped_data_esa.xlsx'
    df = xlsxToDf(excel_file)
    mapping = fieldMapping(df)
    print(len(mapping))
    return mapping


# call to execute function to retrieve final mapping 
def execute() -> sfm.SectionFieldsMap:
    '''
    Executes workflow to retrieve subsection mappings from the 'PCA_FIELDS.xlsx' Excel file.

    Returns:
        sfm.SectionFieldsMap: Object with dictionary mapping {subsection_num: {field: descript.}}} for all subsections.

    Note: SectionFieldsMap contains fields attribute that stores this mapping.
    '''
    excel_file = 'scraped_data_esa.xlsx'
    df = xlsxToDf(excel_file)
    sections = createSections(df)
    return sections

if __name__ == "__main__":
    # run for testing purposes
    result = execute()
    for section in result.fields:
        print("\nSECTION", str(section) + ":")
        print(result.fields[section])
    
    print("\nFINAL MAPPING OBJECT:")
    print(result)


# note: 488 field names scraped from site 