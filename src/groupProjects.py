import mapping
import pandas as pd
import copy


def findReports(df: pd.DataFrame) -> set:
    '''
    Generates a set of report names from the ESA_Data DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing ESA report data.

    Returns:
        set: Set of all reports found in ESA_Data.
    ''' 
    report_nums = df['project_number_string']
    reports = set(num for num in report_nums)
    return reports


def mapReportsToObject(reports: set) -> dict:
    '''
    Maps each unique report number to its corresponding SFM object.

    Parameters:
        reports (set): A set of all report numbers.

    Returns:
        dict: Dictionary mapping of {report_num: sfm object} containing all reports.
    '''   
    report_mapping = dict()
    sfm = mapping.execute()

    for each in reports:
        temp = copy.deepcopy(sfm)
        report_mapping[each] = temp 
    return report_mapping


def updateMapping(valid_df: pd.DataFrame, report_mapping: dict) -> dict:
    '''
    Combines question-answer data with report mapping dictionary to update SFM objects.

    Parameters:
        valid_df (pd.DataFrame): DataFrame containing non-null answer values.
        report_mapping (dict): Dictionary mapping report numbers to SFM objects.

    Returns:
        dict: Updated report mapping dictionary containing unique question-answer SFM objects.
    ''' 
    hold = dict()
    for _,row in valid_df.iterrows():
        if row["project_number_string"] in hold:
            hold[row["project_number_string"]].append((row["document_spot"], row["the_data"]))
        else:
            hold[row["project_number_string"]] = []

    for key,value in hold.items():
        data_dict = {data[0]:data[1] for data in value}
        report_mapping[key].fields = data_dict
    return report_mapping


# call to execute function to retrieve final mapping for testing
def execute() -> dict:
    '''
    Executes workflow to retrieve report dictionary for testing from the 'ESA_Data.xlsx' Excel file.

    Returns:
        dict: Dictionary mapping {report_num: sfm object} of all testing reports.
    ''' 
    df = mapping.xlsxToDf('ESA_DATA.xlsx')
    valid_df = df[df['the_data'].notna()] # HANDLED NULL VALUES FOR TESTING

    report_set = findReports(df)
    report_dict = mapReportsToObject(report_set)
    result = updateMapping(valid_df, report_dict)
    return result


if __name__ == "__main__":
    # run to view readable version of script (118 test reports)
    result = execute()

    for report_num, data in result.items():
        print("\nREPORT: ", report_num)
        print(data) # test with data.fields to retrieve dict in SFM object