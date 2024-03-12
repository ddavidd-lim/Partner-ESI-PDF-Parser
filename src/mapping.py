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
    '''
    Checks if the value belongs to specified section.

    Parameters:
        value (int, str, float): the value in DataFrame to check.
        section (str): the report section number to check against.

    Returns:
        bool: True if value is included in section, False otherwise.
    '''
    return str(value)[0] == section


def esaRows(df: pd.DataFrame, section: str) -> pd.DataFrame:
    '''
    Filters the DataFrame to extract the valid rows containing ESA values within corresponding section.

    Parameters:
        df (pd.DataFrame): original DataFrame of the Excel file.
        section (str): the report section number to filter.

    Returns:
        pd.DataFrame: DataFrame containing only rows related to Esa Reports within passed in section.
    '''
    esa_df = df[df['Bool convert mc commas'] == 'EsaReportField']
    all_sections = esa_df['Section Reference']
    section_df = esa_df[all_sections.apply(lambda x: checkSection(x, section))]
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
    '''
    Generates dictionary containing all sections in ESA reports and their data.

    Parameters:
        df (pd.DataFrame): DataFrame containing rows related to Esa Reports and report section.

    Returns:
        dict: Dictionary mapping {section_number: SectionFieldsMap object} containing all sections.
    '''
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


# call to execute code and retrieve section mappings
def execute() -> dict:
    '''
    Executes workflow to retrieve section mappings from the 'PCA_FIELDS.xlsx' Excel file.

    Returns:
        dict: Dictionary mapping {section_number: SectionFieldsMap} containing all sections.

    Note: SectionFieldsMap contains fields attribute that stores section field value mappings.
    '''
    excel_file = 'PCA_FIELDS.xlsx'
    df = xlsxToDf(excel_file)
    sections = createSections(df)
    return sections

if __name__ == "__main__":
    result = execute()
    print("\nFINAL MAPPING:")
    print(result)

    for section in result:
        print("\nSECTION", str(section) + ":")
        print(result[section].fields)


# note: 2182 values ESA found in dict mapping and in Excel file