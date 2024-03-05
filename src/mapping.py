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
        file_path = os.path.join(cwd, file)
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print("An error occurred:", e)
        return None  
    

def esaRows(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Filters the DataFrame to extract the valid rows containing ESA values .

    Parameters:
        df (pd.DataFrame): original DataFrame of the Excel file.

    Returns:
        pd.DataFrame: DataFrame containing only rows related to Esa Reports.
    '''
    esa_df = df[df['Bool convert mc commas'] == 'EsaReportField']
    return esa_df


def mapping(df: pd.DataFrame) -> dict:
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


# call to execute code and retrieve mapping
def execute():
    '''
    Executes workflow to retrieve mapping from the 'PCA_FIELDS.xlsx' Excel file.

    Returns:
        dict: Dictionary mapping {"field_value_code": "description"} of rows.
    '''
    excel_file = 'PCA_FIELDS.xlsx'
    df = xlsxToDf(excel_file)
    esaDf = esaRows(df)
    return mapping(esaDf)

execute()

# note: 2182 values ESA found in dict mapping and in Excel file (confirmed)