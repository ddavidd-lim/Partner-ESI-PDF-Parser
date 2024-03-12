from classes import SectionFieldsMap as sfm
import pandas as pd
import os

# TODO: add function to create instances of classes

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
    

# used for lambda to check if section reference cell is part of section number    
def checkSection(value, section):
    return str(value)[0] == section


def esaRows(df: pd.DataFrame, section) -> pd.DataFrame:
    # TODO: take in a section_num parameter to further filter fields
    # TODO: check if the string value of the section reference is goal section -> account for str, float, and int

    '''
    Filters the DataFrame to extract the valid rows containing ESA values .

    Parameters:
        df (pd.DataFrame): original DataFrame of the Excel file.

    Returns:
        pd.DataFrame: DataFrame containing only rows related to Esa Reports.
    '''
    esa_df = df[df['Bool convert mc commas'] == 'EsaReportField']
    all_sections = esa_df['Section Reference']
    section_df = esa_df[all_sections.apply(lambda x: checkSection(x, section))]
    return section_df


def fieldMapping(df: pd.DataFrame) -> dict:
    '''
    Creates mapping of valid field values to their corresponding descriptions in DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing only rows related to Esa Reports.

    Returns:
        dict: Dictionary mapping {"field_value_code": "description"} of rows.
    '''
    questions = {} 
    for index, row in df.iterrows():
        questions[row["Name"]] = row["Section Integer"]
    return questions

def createSections(df):
    df1 = esaRows(df, '1')
    section1 = sfm.SectionFieldsMap(fieldMapping(df1))
    df2 = esaRows(df, '2')
    section2 = sfm.SectionFieldsMap(fieldMapping(df2))
    df3 = esaRows(df, '3')
    section3 = sfm.SectionFieldsMap(fieldMapping(df3))
    df4 = esaRows(df, '4')
    section4 = sfm.SectionFieldsMap(fieldMapping(df4))
    df5 = esaRows(df, '5')
    section5 = sfm.SectionFieldsMap(fieldMapping(df5))
    df6 = esaRows(df, '6')
    section6 = sfm.SectionFieldsMap(fieldMapping(df6))
    df7 = esaRows(df, '7')
    section7 = sfm.SectionFieldsMap(fieldMapping(df7))
    return {1: section1, 2: section2, 3: section3, 4: section4, 5: section5, 6: section6, 7: section7}



# call to execute code and retrieve mapping
def execute():
    # TODO: needs to now return mapping {section_number: {field_values}} for all report sections
    '''
    Executes workflow to retrieve mapping from the 'PCA_FIELDS.xlsx' Excel file.

    Returns:
        dict: Dictionary mapping {"field_value_code": "description"} of rows.
    '''
    excel_file = 'PCA_FIELDS.xlsx'
    df = xlsxToDf(excel_file)
    sections = createSections(df)
    return sections


print(execute())
# note: 2182 values ESA found in dict mapping and in Excel file (confirmed)