import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None  # default='warn'

# Vorwort: Was wird im CleanUp alles bereinigt - und was nicht?
# Im Cleanup werden:
# - Spalten zusammengeführt
# - Umwandlungen zu NaN Values durchgeführt ('', 'None', '-')
# - Groß und Kleinschreibungen stadardisiert
# - In geringem Umfang Werteumwanldungen, z.B. mittels Dictionaries durchgenommen

# Was wird nicht bereinigt:
# - Es werde keine pauschale Änderungen der vorliegenden Strings vorgenommen (z.B. entfernen von Spiegelstrichen)
# -- Diese sollen individuell innerhalb der Analyse angepasst werden
# - Entfernen von unrealistischen Werten

#Spaltennamen definieren
##Hier können schnelle Spaltenüberschriftenänderungen vorgenommen werden, wenn gewünscht.
##Achtung: Dadurch kann es jedoch passieren, dass nachgelagerte Analyse nicht mehr funtkionieren


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




def generate_cleaned_df(filepath_orig_csv , folderpath_output):
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


def clean_wage_offer_from(inital_df=pd.DataFrame):
    col_list = ["wage_offer_from_9089", "wage_offered_from_9089"]
    temp_df = inital_df[col_list]

    # Firstly, all string types will be transformed into a format, which can be converted into a float type.
    # Secondly every cell is converted into float.
    temp_df["wage_offer_from_9089"] = temp_df["wage_offer_from_9089"].apply(clean_currency).astype('float')

    # The two different columns 'wage_offer_from_9089' and 'wage_offered_from_9089' get merged because they both contain similar information and don't overap each other.
    # The columns get merged through simmple addition, therefore all na values are replaced by zero.
    temp_df['wage_offer_from_merged'] = temp_df['wage_offer_from_9089'].fillna(0) + temp_df[
        'wage_offered_from_9089'].fillna(0)

    # Cells which contain zero, even after the merge, will get converted into NaN values. Providing better data for the subsequent analysis.
    temp_df['wage_offer_from_merged'].replace(0, np.nan, inplace=True)

    # only the cleaned up column 'wage_offer_merged' gets returned
    return temp_df['wage_offer_from_merged']


def clean_currency(x):
    """ If the value is a string, then remove delimiters
    otherwise, the value is numeric and can be converted.

    Additionally the provided data contains two '#############' values. These will get replaced by NaN.

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
    temp_df = inital_df[col_list]

    # The two different columns 'wage_offer_unit_of_pay_9089' and 'wage_offered_unit_of_pay_9089' get merged because they both contain similar information and don't overap each other.
    # The columns get merged through simmple concatenation, therefor all na values are replaced by ''.
    temp_df['wage_offer_of_pay_unit_merged'] = temp_df['wage_offer_unit_of_pay_9089'].fillna('') + temp_df[
        'wage_offered_unit_of_pay_9089'].fillna('')

    # Cells which contain '', even after the merge, will get converted into NaN values. Providing better data for the subsequent analysis.
    temp_df['wage_offer_of_pay_unit_merged'].replace('', np.nan, inplace=True)

    temp_df['wage_offer_of_pay_unit_merged'] = normalize_pay_unit_columns(temp_df['wage_offer_of_pay_unit_merged'])

    return temp_df['wage_offer_of_pay_unit_merged']


def normalize_pay_unit_columns(pay_unit_column=pd.DataFrame):
    # throughout the datasample different wording is used in the column of the pay units.
    # By creating a dictionary containing all abbreviations, we can replace contained long-wording strings by their abbreviations.
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
    temp_df = inital_df[col_list]

    # Convert to column to datetime
    temp_df['case_received_date'] = pd.to_datetime(temp_df['case_received_date'])

    return temp_df['case_received_date']


def clean_decision_date(inital_df=pd.DataFrame):
    col_list = ["decision_date"]
    temp_df = inital_df[col_list]

    # Convert to column to datetime
    temp_df['decision_date'] = pd.to_datetime(temp_df['decision_date'])

    return temp_df['decision_date']


def clean_employer_state(inital_df=pd.DataFrame):
    col_list = ["employer_state"]
    temp_df = inital_df[col_list]

    # In this column state abbreviations are used simultaneously with long-written state names. This will be changed into long-written state names only.

    ##States
    web_table = pd.read_html(
        'https://www.infoplease.com/us/postal-information/state-abbreviations-and-state-postal-codes',
        match='State/District')
    states_abbreviations_df = web_table[0]

    # Standardized Format
    states_abbreviations_df['State/District'] = states_abbreviations_df['State/District'].str.upper()
    abbr_dictionary = states_abbreviations_df.set_index('Postal Code')['State/District'].to_dict()

    # Replace abbreviations by long-names
    temp_df['employer_state'] = temp_df['employer_state'].replace(abbr_dictionary)

    ##Territories
    web_table = pd.read_html(
        'https://www.infoplease.com/us/postal-information/state-abbreviations-and-state-postal-codes',
        match='Territory/Associate')
    states_abbreviations_df = web_table[0]

    # Standardized Format
    states_abbreviations_df['Territory/Associate'] = states_abbreviations_df['Territory/Associate'].str.upper()
    abbr_dictionary = states_abbreviations_df.set_index('Postal Code')['Territory/Associate'].to_dict()

    # Replace abbreviations by long-names
    temp_df['employer_state'] = temp_df['employer_state'].replace(abbr_dictionary)

    # Replace BC with British Columbia
    temp_df['employer_state'] = temp_df['employer_state'].str.replace('BC', 'British Columbia')

    return temp_df['employer_state']


def clean_case_number(inital_df=pd.DataFrame):
    col_list = ["case_no", "case_number"]
    temp_df = inital_df[col_list]

    # The two different columns 'case_no' and 'case_number' get merged because they both contain similar information and don't overap each other.
    # The columns get merged through simmple concatenation, therefor all na values are replaced by ''.
    temp_df['case_number_merged'] = temp_df['case_no'].fillna('') + temp_df['case_number'].fillna('')

    # Cells which contain '', even after the merge, will get converted into NaN values. Providing better data for the subsequent analysis.
    temp_df['case_number_merged'].replace('', np.nan, inplace=True)

    return temp_df['case_number_merged']


def clean_foreign_worker_info_education_other(inital_df=pd.DataFrame):
    col_list = ["foreign_worker_info_education_other", "fw_info_education_other"]
    temp_df = inital_df[col_list]

    temp_df['foreign_worker_info_education_other'] = temp_df['foreign_worker_info_education_other'].replace(r'^\s*$',
                                                                                                            np.nan,
                                                                                                            regex=True)
    temp_df['fw_info_education_other'] = temp_df['fw_info_education_other'].replace(r'^\s*$', np.nan, regex=True)
    temp_df['foreign_worker_info_education_other'] = temp_df['foreign_worker_info_education_other'].replace('None',
                                                                                                            np.nan,
                                                                                                            regex=True)
    temp_df['fw_info_education_other'] = temp_df['fw_info_education_other'].replace('None', np.nan, regex=True)

    # The two different columns 'foreign_worker_info_education_other' and 'fw_info_education_other' get merged because they both contain similar information and don't overap each other.
    # The columns get merged through simmple concatenation, therefor all na values are replaced by ''.
    temp_df['fw_info_education_other_merged'] = temp_df['foreign_worker_info_education_other'].fillna('') + temp_df[
        'fw_info_education_other'].fillna('')

    # Cells which contain '', even after the merge, will get converted into NaN values. Providing better data for the subsequent analysis.
    temp_df['fw_info_education_other_merged'] = temp_df['fw_info_education_other_merged'].replace(r'^\s*$', np.nan,
                                                                                                  regex=True)

    return temp_df['fw_info_education_other_merged']


def clean_country_of_citizenship(inital_df=pd.DataFrame):
    col_list = ["country_of_citizenship", "country_of_citzenship"]
    temp_df = inital_df[col_list]

    # The two different columns 'foreign_worker_info_education_other' and 'fw_info_education_other' get merged because they both contain similar information and don't overap each other.
    # The columns get merged through simmple concatenation, therefor all na values are replaced by ''.
    temp_df['country_of_citizenship_merged'] = temp_df['country_of_citizenship'].fillna('') + temp_df[
        'country_of_citzenship'].fillna('')

    # Cells which contain '', even after the merge, will get converted into NaN values. Providing better data for the subsequent analysis.
    temp_df['country_of_citizenship_merged'] = temp_df['country_of_citizenship_merged'].replace('', np.nan, regex=True)

    return temp_df['country_of_citizenship_merged']


def clean_pw_amount_9089(inital_df=pd.DataFrame):
    col_list = ["pw_amount_9089"]
    temp_df = inital_df[col_list]

    # Firstly, all string types will be transformed into a format, which can be converted into a float type.
    # Secondly every cell is converted into float.
    temp_df["pw_amount_9089"] = temp_df["pw_amount_9089"].apply(clean_currency).astype('float')

    return temp_df['pw_amount_9089']


def clean_pw_unit_of_pay_9089(inital_df=pd.DataFrame):
    col_list = ["pw_unit_of_pay_9089"]
    temp_df = inital_df[col_list]

    temp_df['pw_unit_of_pay_9089'] = normalize_pay_unit_columns(temp_df['pw_unit_of_pay_9089'])

    return temp_df['pw_unit_of_pay_9089']


def clean_employer_name(inital_df=pd.DataFrame):
    col_list = ["employer_name"]
    temp_df = inital_df[col_list]

    temp_df["employer_name"] = temp_df["employer_name"].str.upper()

    return temp_df['employer_name']


def clean_employer_city(inital_df=pd.DataFrame):
    col_list = ["employer_city"]
    temp_df = inital_df[col_list]

    temp_df["employer_city"] = temp_df["employer_city"].str.upper()

    # Delete special character at the end of a city name
    temp_df["employer_city"] = temp_df["employer_city"].str.rstrip(',.`')

    return temp_df['employer_city']


def clean_pw_job_title(inital_df=pd.DataFrame):
    col_list = ["pw_job_title_9089", "pw_job_title_908", "add_these_pw_job_title_9089"]
    temp_df = inital_df[col_list]

    temp_df['pw_job_title_merged'] = temp_df['pw_job_title_9089'].fillna('') + temp_df['pw_job_title_908'].fillna('')

    # Cells which contain '', even after the merge, will get converted into NaN values. Providing better data for the subsequent analysis.
    temp_df['pw_job_title_merged'].replace('', np.nan, inplace=True)

    # Only NaN Cases of pw_job_title_merged wil be merged with add_these_pw_job_title_9089
    temp_df['pw_job_title_merged'] = temp_df['pw_job_title_merged'].fillna(temp_df['add_these_pw_job_title_9089'])

    temp_df['pw_job_title_merged'] = temp_df['pw_job_title_merged'].str.lower()

    temp_df["pw_job_title_merged"] = temp_df["pw_job_title_merged"].apply(turn_plural_to_singular_string)

    return temp_df['pw_job_title_merged']


def turn_plural_to_singular_string(x):
    """ If the value is a string, check if the last character is 's'. If yes, then remove it.
    """
    if isinstance(x, str):
        if x[-1] == 's':
            x = x[0: len(x) - 1]
    return (x)


def clean_foreign_worker_info_birth_country(inital_df=pd.DataFrame):
    col_list = ["foreign_worker_info_birth_country", "fw_info_birth_country"]
    temp_df = inital_df[col_list]

    temp_df["foreign_worker_info_birth_country"] = temp_df["fw_info_birth_country"].str.upper()

    return temp_df['foreign_worker_info_birth_country']

#Optional:
def convert_case_status_to_certified_or_denied(df=pd.DataFrame):
    # Datensatz enthält Fälle die zurückgezogen wurden 'withdrawn'. Da diese Fälle nicht relevant sind werden sie aus dem Datensatz gelöscht.
    df = df[df.name_case_status != 'Withdrawn']
    # Der Status 'certified' und der Status 'certified-expired' werden zu dem Wert 'certified' zusammengefasst.
    df.loc[df.name_case_status == 'Certified-Expired', 'case_status'] = 'Certified'

    return df