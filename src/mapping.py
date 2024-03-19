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
        file_path = os.path.join(cwd, "..", "data", "raw", file)
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print("An error occurred:", e)
        return None  
    

def checkSection(value, section: str) -> bool:
    # TODO: check the entire subsection up to three places x.x.x
    '''
    Checks if the value belongs to specified section.

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


def esaRows(df: pd.DataFrame, section: str) -> pd.DataFrame:
    '''
    Filters the DataFrame to extract the valid rows containing ESA values within corresponding section.

    Parameters:
        df (pd.DataFrame): original DataFrame of the Excel file.
        section (str): the report section number to filter.

    Returns:
        pd.DataFrame: DataFrame containing only rows related to Esa Reports within passed in section.
    '''
    esa_df = df[df['Bool convert mc commas'] == 'EsaReportField'] # DATAFRAME OF ALL ESA REPORT ROWS

    all_sections = esa_df['Section Reference']
    section_df = esa_df[all_sections.apply(lambda x: checkSection(x, section))] # DATAFRAME OF ALL SUBSECTION ROWS
    return section_df


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
        questions[row["Name"]] = row["Section Integer"]
    return questions


def createSections(df: pd.DataFrame) -> dict:
    # TODO: iterate through valid subsections to get esa rows and mappings
    # TODO: make final mapping of each subsections and inner dicts
    # TODO: return one instance of section fields map with all data
    '''
    Generates dictionary containing all sections in ESA reports and their data.

    Parameters:
        df (pd.DataFrame): DataFrame containing rows related to Esa Reports and report section.

    Returns:
        dict: Dictionary mapping {section_number: SectionFieldsMap object} containing all sections.
    '''
    esa_df = df[df['Bool convert mc commas'] == 'EsaReportField']

    section_references = esa_df['Section Reference'].dropna()
    section_set = set(section_references)
    edited = set(str(each) for each in section_set)

    final = {}
    for sec in edited:
        temp = esaRows(df, sec)
        d = fieldMapping(temp)
        final[sec] = d
    
    # testing
    print(final)
    for k,v in final.items():
        print(k, v)
    section = sfm.SectionFieldsMap(final)
    print(section)
    print(len(final))
    print(len(edited))
    print(edited)

    return section


# call to execute code and retrieve subsection mappings
def execute() -> dict:
    #TODO: retrieve one object instead of one per section
    '''
    Executes workflow to retrieve section mappings from the 'PCA_FIELDS.xlsx' Excel file.

    Returns:
        dict: Dictionary mapping {section_number: SectionFieldsMap} containing all sections.

    Note: SectionFieldsMap contains fields attribute that stores section field value mappings.
    '''
    excel_file = 'PCA_FIELDS.xlsx'
    df = xlsxToDf(excel_file)
    # call function to get the mapping
    # iterate through mapping and make esaRow dataframe for each
    # make mapping of each and add it to final SectionsFieldMap fields dict
    #sections = esaRows(df)
    sections = createSections(df)
    return sections

if __name__ == "__main__":
    result = execute()
    # excel_file = 'PCA_FIELDS.xlsx'
    # df = xlsxToDf(excel_file)
    # testing(df)
    # print("\nFINAL MAPPING:")
    # print(result)

    # for section in result:
    #     print("\nSECTION", str(section) + ":")
    #     print(result[section].fields)


# note: 2182 values ESA found in dict mapping and in Excel file
