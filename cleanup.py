import pandas as pd
import numpy as np
import modules

pd.options.mode.chained_assignment = None  # default='warn'

# Vorwort: Was wird im CleanUp alles bereinigt - und was nicht?
# Im Cleanup werden:
# - Spalten zusammengeführt
# - Umwandlungen zu NaN Values durchgeführt ('', 'None', '-')
# - Groß- und Kleinschreibungen standardisiert
# - In geringem Umfang Werteumwanldungen, z.B. mittels Dictionaries durchgeführt

# Was wird nicht bereinigt:
# - Es werde keine pauschale Änderungen der vorliegenden Strings vorgenommen (z.B. entfernen von Spiegelstrichen)
# -- Diese sollen individuell innerhalb der Analyse angepasst werden
# - Entfernen von unrealistischen Werten

# Declare/ Change Column Headers
name_wage_offer_from = "wage_offer_from"
name_wage_offer_unit_of_pay = "wage_offer_unit_of_pay"
name_case_received_date = "case_received_date"
name_decision_date = "decision_date"
name_employer_state = "employer_state"
name_case_number = "case_number"
name_foreign_worker_info_education_other = "foreign_worker_info_education_other"
name_country_of_citizenship = "country_of_citizenship"
name_case_status = "case_status"
name_us_economic_sector = "us_economic_sector"
name_employer_name = "employer_name"
name_employer_city = "employer_city"
name_pw_amount_9089 = "prevailing_wage_amount_9089"
name_pw_unit_of_pay_9089 = "prevailing_wage_unit_of_pay_9089"
name_foreign_worker_info_education = "foreign_worker_info_education"
name_pw_level_9089 = "prevailing_wage_level_9089"
name_pw_soc_title = "prevailing_wage_soc_title"
name_class_of_admission = "class_of_admission"
name_pw_job_title = "prevailing_wage_job_title_9089"
name_foreign_worker_info_birth_country = "foreign_worker_info_birth_country"


# Generate cleaned us_perm_visas
def generate_cleaned_df(filepath_orig_csv , folderpath_output):
    """
    Executes all necessary cleaning steps in order to obtain a dataset, which is suitable for the subsequent analysis.
    @params:
        filepath_orig_csv  - Required  : filepath of the original dataset
        folderpath_output  - Required  : folderpath for the export of the cleaned dataset
    """
    inital_df = pd.read_csv(filepath_orig_csv)
    cleaned_df = pd.DataFrame()

    # wage_offer_from_9089
    # wage_offered_from_9089
    cleaned_df[name_wage_offer_from] = clean_wage_offer_from(inital_df)

    # wage_offer_unit_of_pay_9089
    # wage_offered_unit_of_pay_9089
    cleaned_df[name_wage_offer_unit_of_pay] = clean_wage_offer_unit_of_pay(inital_df)

    # case_received_date
    cleaned_df[name_case_received_date] = clean_case_received_date(inital_df)

    # case_received_date
    cleaned_df[name_case_received_date] = clean_case_received_date(inital_df)

    # decision_date
    cleaned_df[name_decision_date] = clean_decision_date(inital_df)

    # employer_state
    cleaned_df[name_employer_state] = clean_employer_state(inital_df)

    # case_no
    # case_number
    cleaned_df[name_case_number] = clean_case_number(inital_df)

    # foreign_worker_info_education_other
    # fw_info_education_other
    cleaned_df[name_foreign_worker_info_education_other] = clean_foreign_worker_info_education_other(inital_df)

    # country_of_citizenship
    # country_of_citzenship
    cleaned_df[name_country_of_citizenship] = clean_country_of_citizenship(inital_df)

    # case_status
    cleaned_df[name_case_status] = inital_df["case_status"]

    # us_economic_sector
    cleaned_df[name_us_economic_sector] = inital_df["us_economic_sector"]

    # case_status
    cleaned_df[name_employer_name] = clean_employer_name(inital_df)

    # employer_city
    cleaned_df[name_employer_city] = clean_employer_city(inital_df)

    # pw_amount_9089
    cleaned_df[name_pw_amount_9089] = clean_pw_amount_9089(inital_df)

    # pw_unit_of_pay_9089
    cleaned_df[name_pw_unit_of_pay_9089] = clean_pw_unit_of_pay_9089(inital_df)

    # foreign_worker_info_education
    cleaned_df[name_foreign_worker_info_education] = inital_df["foreign_worker_info_education"]

    # pw_level_9089
    cleaned_df[name_pw_level_9089] = inital_df["pw_level_9089"]

    # pw_soc_title
    cleaned_df[name_pw_soc_title] = inital_df["pw_soc_title"]

    # us_economic_sector
    cleaned_df[name_us_economic_sector] = inital_df["us_economic_sector"]

    # class_of_admission
    cleaned_df[name_class_of_admission] = inital_df["class_of_admission"]

    # pw_job_title_9089
    # pw_job_title_908
    # add_these_pw_job_title_9089
    cleaned_df[name_pw_job_title] = clean_pw_job_title(inital_df)

    # foreign_worker_info_birth_country
    # fw_info_birth_country
    cleaned_df[name_foreign_worker_info_birth_country] = clean_foreign_worker_info_birth_country(inital_df)

    print(cleaned_df.head())
    cleaned_df.to_csv(folderpath_output + 'us_perm_visas_cleaned.csv')

## Cleaning Steps ##


def clean_wage_offer_from(inital_df=pd.DataFrame):
    col_list = ["wage_offer_from_9089", "wage_offered_from_9089"]
    temp_df = inital_df[col_list].copy()

    # Firstly, all string types will be transformed into a format, which can be converted into a float type.
    # Secondly every cell is converted into float.
    temp_df["wage_offer_from_9089"] = temp_df["wage_offer_from_9089"].apply(clean_currency).astype('float')

    # The two different columns 'wage_offer_from_9089' and 'wage_offered_from_9089' get merged because they both contain similar information and don't overap each other.
    # The columns get merged through simmple addition, therefore all NaN values are replaced by zero.
    temp_df['wage_offer_from_merged'] = mergeTwoColumns(temp_df, "wage_offer_from_9089", "wage_offered_from_9089")

    # Only the cleaned up column 'wage_offer_merged' gets returned
    return temp_df['wage_offer_from_merged']


def clean_currency(x):
    """
    If the value is a string, then remove delimiters.
    Otherwise, the value is numeric and needs no further adjustments.
    Additionally the provided dataset contains two '#############' values. These will get replaced by NaN.
    Source: https://pbpython.com/currency-cleanup.html (with slight changes)
    """
    if isinstance(x, str):
        if x == '#############':
            x = np.nan
        else:
            return (x.replace(',', ''))
    return (x)

def clean_wage_offer_unit_of_pay(inital_df=pd.DataFrame):
    col_list = ["wage_offer_unit_of_pay_9089", "wage_offered_unit_of_pay_9089"]
    temp_df = inital_df[col_list].copy()

    # The two different columns 'wage_offer_unit_of_pay_9089' and 'wage_offered_unit_of_pay_9089' get merged.
    temp_df['wage_offer_of_pay_unit_merged'] = mergeTwoColumns(temp_df, "wage_offer_unit_of_pay_9089", "wage_offered_unit_of_pay_9089")

    # The units used in the two columns are different. They have to get standardized.
    temp_df['wage_offer_of_pay_unit_merged'] = standardize_pay_unit_columns(temp_df['wage_offer_of_pay_unit_merged'])

    return temp_df['wage_offer_of_pay_unit_merged']

def standardize_pay_unit_columns(pay_unit_column=pd.DataFrame):
    """
    Throughout the datasample different wording is used in the column of the pay units.
    By creating a dictionary containing all abbreviations, we can replace contained long-wording strings by their abbreviations.
    """
    unit_abbreviations = {
        "Year": "yr",
        "Month": "mth",
        "Bi-Weekly": "bi",
        "Week": "wk",
        "Hour": "hr"
    }

    return pay_unit_column.replace(unit_abbreviations)


def clean_case_received_date(inital_df=pd.DataFrame):
    col_list = ["case_received_date"]
    temp_df = inital_df[col_list].copy()

    # Convert the column to datetime.
    temp_df['case_received_date'] = pd.to_datetime(temp_df['case_received_date'])

    return temp_df['case_received_date']


def clean_decision_date(inital_df=pd.DataFrame):
    col_list = ["decision_date"]
    temp_df = inital_df[col_list].copy()

    # Convert the column to datetime.
    temp_df['decision_date'] = pd.to_datetime(temp_df['decision_date'])

    return temp_df['decision_date']


def clean_employer_state(inital_df=pd.DataFrame):
    col_list = ["employer_state"]
    temp_df = inital_df[col_list].copy()

    # In this column state abbreviations are used simultaneously with long-written state names.
    # This will be changed into long-written state names only.

    # States
    web_table = pd.read_html(
        'https://www.infoplease.com/us/postal-information/state-abbreviations-and-state-postal-codes',
        match='State/District')
    states_abbreviations_df = web_table[0].rename(columns={"State/District": "name"})

    # Territories
    web_table = pd.read_html(
        'https://www.infoplease.com/us/postal-information/state-abbreviations-and-state-postal-codes',
        match='Territory/Associate')
    states_abbreviations_df = states_abbreviations_df.append(web_table[0].rename(columns={"Territory/Associate": "name"}))

    # Standardized Format
    states_abbreviations_df['name'] = states_abbreviations_df['name'].str.upper()
    abbr_dictionary = states_abbreviations_df.set_index('Postal Code')['name'].to_dict()

    # Replace abbreviations by long-names
    temp_df['employer_state'] = temp_df['employer_state'].replace(abbr_dictionary)

    # Replace BC with British Columbia
    temp_df['employer_state'] = temp_df['employer_state'].str.replace('BC', 'BRITISH COLUMBIA')

    return temp_df['employer_state']


def clean_case_number(inital_df=pd.DataFrame):
    col_list = ["case_no", "case_number"]
    temp_df = inital_df[col_list].copy()

    # The two different columns get merged because they both contain similar information.
    temp_df['case_number_merged'] = mergeTwoColumns(temp_df, "case_no",
                                                               "case_number")

    return temp_df['case_number_merged']


def clean_foreign_worker_info_education_other(inital_df=pd.DataFrame):
    col_list = ["foreign_worker_info_education_other", "fw_info_education_other"]
    temp_df = inital_df[col_list].copy()

    temp_df['foreign_worker_info_education_other'] = replaceNoneOrEmptyByNa(temp_df['foreign_worker_info_education_other'])
    temp_df['fw_info_education_other'] = replaceNoneOrEmptyByNa(temp_df['foreign_worker_info_education_other'])

    # The two different columns get merged because they both contain similar information.
    temp_df['fw_info_education_other_merged'] = mergeTwoColumns(temp_df, "foreign_worker_info_education_other",
                                                               "fw_info_education_other")

    # Cells which contain empty values, even after the merge, will get converted into NaN values. Providing better data for the subsequent analysis.
    temp_df['fw_info_education_other_merged'] = replaceNoneOrEmptyByNa(temp_df['fw_info_education_other_merged'])

    return temp_df['fw_info_education_other_merged']

def replaceNoneOrEmptyByNa(inital_df=pd.DataFrame):
    """
    Removes empty values.
    Multiple Columns contain empty or semi-empty values like "", "None", etc.
    This function is used to remove the most common empty values.
    """
    temp_df = inital_df.copy()

    # Missing Values and 'None' get replaced by NaN.
    temp_df = temp_df.replace(r'^\s*$', np.nan, regex=True)
    temp_df = temp_df.replace('', np.nan, regex=True)
    temp_df = temp_df.replace(['NaN', 'NaT', 'nan', 'None', 'none', '-'], np.nan)

    return temp_df

def clean_country_of_citizenship(inital_df=pd.DataFrame):
    col_list = ["country_of_citizenship", "country_of_citzenship"]
    temp_df = inital_df[col_list].copy()

    # The two different columns get merged because they both contain similar information.
    temp_df['country_of_citizenship_merged'] = mergeTwoColumns(temp_df, "country_of_citizenship",
                                                               "country_of_citzenship")

    return temp_df['country_of_citizenship_merged']


def clean_pw_amount_9089(inital_df=pd.DataFrame):
    col_list = ["pw_amount_9089"]
    temp_df = inital_df[col_list].copy()

    # Firstly, all string types will be transformed into a format, which can be converted into a float type.
    # Secondly every cell is converted into float.
    temp_df["pw_amount_9089"] = temp_df["pw_amount_9089"].apply(clean_currency).astype('float')

    return temp_df['pw_amount_9089']


def clean_pw_unit_of_pay_9089(inital_df=pd.DataFrame):
    col_list = ["pw_unit_of_pay_9089"]
    temp_df = inital_df[col_list].copy()

    # Units are not standardized. Standardized values facilitate analyses.
    temp_df['pw_unit_of_pay_9089'] = standardize_pay_unit_columns(temp_df['pw_unit_of_pay_9089'])

    return temp_df['pw_unit_of_pay_9089']


def clean_employer_name(inital_df=pd.DataFrame):
    col_list = ["employer_name"]
    temp_df = inital_df[col_list].copy()

    # Replacing the values by uppercase values, reduces the numer of unique values.
    temp_df["employer_name"] = temp_df["employer_name"].str.upper()

    return temp_df['employer_name']


def clean_employer_city(inital_df=pd.DataFrame):
    col_list = ["employer_city"]
    temp_df = inital_df[col_list].copy()

    temp_df["employer_city"] = temp_df["employer_city"].str.upper()

    # Delete uncommon characters at the end of a city name
    temp_df["employer_city"] = cutOffUnusualCharacters(temp_df["employer_city"])

    return temp_df['employer_city']


def clean_pw_job_title(inital_df=pd.DataFrame):
    col_list = ["pw_job_title_9089", "pw_job_title_908", "add_these_pw_job_title_9089"]
    temp_df = inital_df[col_list].copy()

    # The different columns get merged because they both contain similar information.
    temp_df['pw_job_title_merged'] = mergeTwoColumns(temp_df, 'pw_job_title_9089', 'pw_job_title_908')
    temp_df['pw_job_title_merged'] = mergeTwoColumns(temp_df, 'pw_job_title_merged', 'add_these_pw_job_title_9089')

    temp_df['pw_job_title_merged'] = temp_df['pw_job_title_merged'].str.lower()

    # Delete characters like ,.* at the end of a string
    temp_df["pw_job_title_merged"] = cutOffUnusualCharacters(temp_df["pw_job_title_merged"])

    # Convert plural to singular
    temp_df["pw_job_title_merged"] = temp_df["pw_job_title_merged"].apply(cutOfflastCharacter, stringToCutOff = "s")

    return temp_df['pw_job_title_merged']

def cutOffUnusualCharacters(df = pd.DataFrame):
    """
    Removes unusual charaters at the end of a string.

    """
    df = df.apply(cutOfflastCharacter, stringToCutOff=",")
    df = df.apply(cutOfflastCharacter, stringToCutOff="...")
    df = df.apply(cutOfflastCharacter, stringToCutOff=".")
    df = df.apply(cutOfflastCharacter, stringToCutOff="*")
    df = df.apply(cutOfflastCharacter, stringToCutOff="`")
    df = df.apply(cutOfflastCharacter, stringToCutOff="/")
    df = df.apply(cutOfflastCharacter, stringToCutOff="?")
    df = df.apply(cutOfflastCharacter, stringToCutOff="+")
    return df

def cutOfflastCharacter(x, stringToCutOff = str):
    """ If the value is a string, check if the last part of the string is equal to the stringToCutOff. If yes, then remove it.
        @params:
        x               - Required  : Original String
        stringToCutOff  - Required  : Declares the string, which should be cut of at the end of x
    """
    lengthOfChar = len(stringToCutOff)

    if isinstance(x, str):
        length = len(x)
        if x[length - lengthOfChar :] == stringToCutOff:
            x = x[:- lengthOfChar]
    return (x)


def clean_foreign_worker_info_birth_country(inital_df=pd.DataFrame):
    col_list = ["foreign_worker_info_birth_country", "fw_info_birth_country"]
    temp_df = inital_df[col_list]

    temp_df["foreign_worker_info_birth_country"] = temp_df["fw_info_birth_country"].str.upper()

    return temp_df['foreign_worker_info_birth_country']

def mergeTwoColumns(inital_df=pd.DataFrame, firstColumn = str, secondColumn = str):
    """
    Merges two columns.
    Are both column overlapping, the firstColumn will be treated as Prio1,
        meaning only missing values of the firstColumn will get filled with values of secondColumn.
    @params:
        inital_df           - Required  : dataFrame containing the relevant columns
        firstColumn         - Required  : name of the firstColumn to merge
        secondColumn        - Required  : name of the secondColumn to merge
    """
    temp_df = inital_df.copy()

    # Columns are merged by addition, if the values are numbers.
    # Float columns can overlap, because they have can have 0 values, instead of NaN.
    if temp_df[firstColumn].dtype in [np.dtype('float64'), np.dtype('float32'), np.dtype('int32')] and temp_df[
        secondColumn].dtype in [np.dtype('float64'), np.dtype('float32'), np.dtype('int32')]:
        temp_df[firstColumn] = temp_df[firstColumn].fillna(0)
        temp_df[secondColumn] = temp_df[secondColumn].fillna(0)

        temp_df['merged'] = (temp_df[firstColumn] + temp_df[secondColumn])

        # Cells which contain zero, even after the merge, will get converted into NaN values. Providing better data for the subsequent analysis.
        temp_df['merged'] = temp_df['merged'].replace(0, np.nan)
        print("Spalten wurden durch Addition zusammengeführt.")

    else:
        if modules.areTwoColumnsOverlapping(temp_df, firstColumn, secondColumn) == True:
            temp_df['merged'] = temp_df[firstColumn].fillna(temp_df[secondColumn])
            print("Achtung: Es liegen überlappende Spalten vor. Die erste Spalte wurde bei fehlenden Werte mit Inhalten der zweiten Spalte befüllt.")

        else:
            # Columns are concatenated, if their values are f.e. objects.
            # The columns get merged through simmple concatenation, therefore all NaN values are replaced by ''.
            temp_df['merged'] = temp_df[firstColumn].fillna('') + temp_df[secondColumn].fillna('')
            # Cells which contain '', even after the merge, will get converted into NaN values. Providing better data for the subsequent analysis.
            temp_df['merged'] = temp_df['merged'].replace('', np.nan)

            print("Spalten waren nicht überlappend und wurden fehlerfrei zusammengeführt.")

    return temp_df['merged']

#Optional:
def convert_case_status_to_certified_or_denied(df=pd.DataFrame):
    # The dataset conatins 'withdrawn' cases. This case can be disturbing is the subsequent analysis. Therefore they are deleted of the dataset.
    df = df[df[name_case_status] != 'Withdrawn']
    # The status 'certified' and 'certified-expired' are merged as 'certified'.
    df.loc[df[name_case_status] == 'Certified-Expired', 'case_status'] = 'Certified'

    return df