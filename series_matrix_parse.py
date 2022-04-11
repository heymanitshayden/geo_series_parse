import sys, os, tarfile
import re
import pandas as pd 
import numpy as np
# !{sys.executable} -m pip install numpy
# !{sys.executable} -m pip install pandas
with open('/users/haydenthomas/rna_seq_data/dmd_data/GSE199692_series_matrix.txt') as f:
    contents = f.readlines()
#metadata for series
series_title_line = ''
series_accession_line = ''
series_subdate_line = ''
series_contributors = []
series_summary_line = ''
series_type_line = ''
series_institution_line = ''
series_inst_department_line = ''
series_contact_name_line = ''
series_contact_line = ''
series_project_line = ''
series_sample_protocol_lines = []

#metadata for samples 
gsm_line = ''
gsm_type_line = ''
lib_source_line = ''
sample_organism_line = ''
sample_sub_date_line = ''
sample_source_line = ''
sample_organism_line = ''
sample_lib_select_line = ''
sample_lib_source_line = ''
sample_lib_strategy_line = ''
sample_sra_line = ''
sample_biosamp_line = ''
#loop through file lines to get metadata for series and samples
for i in contents: 
    #get series meta
    if 'Series_title' in i: 
        series_title_line=i.strip('\n')
    if 'Series_geo_accession' in i: 
        series_accession_line=i.strip('\n')
    if 'Series_submission_date' in i: 
        series_subdate_line=i.strip('\n')
    if 'Series_contributor' in i: 
        series_contributors.append(i.strip('\n'))
    if 'Series_summary' in i: 
        series_summary_line=i.strip('\n')
    if 'Series_type' in i:
        series_type_line=i.strip('\n')
    if 'Series_contact_institute' in i: 
        series_institution_line=i.strip('\n')
    if 'Series_contact_department' in i: 
        series_inst_department_line=i.strip('\n')
    if 'Series_contact_name' in i: 
        series_contact_name_line=i.strip('\n')
    if 'Series_contact_email' in i:
        series_contact_line=i.strip('\n')
    if 'Series_relation' in i: 
        series_project_line=i.strip('\n')
    if 'Sample_extract_protocol' in i: 
        series_sample_protocol_lines.append(i.strip('\n'))
    #get samples meta
    if 'Sample_geo_accession' in i: 
        gsm_line = i.strip('\n')
    if 'Sample_title' in i:
        gsm_type_line = i.strip('\n')
    if 'Sample_source_name' in i:
        sample_source_line=i.strip('\n')
    if 'Sample_organism' in i: 
        sample_organism_line=i.strip('\n')
    if 'Sample_library_selection' in i: 
        sample_lib_select_line=i.strip('\n')
    if 'Sample_library_source' in i: 
        sample_lib_source_line=i.strip('\n')
    if 'Sample_library_strategy' in i: 
        sample_lib_strategy_line=i.strip('\n')
    if 'BioSample' in i: 
        sample_biosamp_line=i.strip('\n')
    if 'SRA' in i: 
        sample_sra_line=i.strip('\n')


# print('Series Title: {}'.format(series_title_line))
# print('Series Accession: {}'.format(series_accession_line))
# print('Series Submission: {}'.format(series_subdate_line))
# print('Series Summary: {}'.format(series_summary_line))

def text_between_quotes(text, n=None):
    between_quotes = text.split('"')[1::2]
    # if you have an odd number of quotes (ie. the quotes are unbalanced), 
    # discard the last element
    if len(between_quotes) % 2 == 0 and not text.endswith('"'):
        use = between_quotes[:-1] 
    else: 
        use = between_quotes
    # check that the length of list is the same as the number of samples, 
    # if not, multiply the list by number of samples
    if n != None: 
        if len(use) !=n and len(use)==1: 
            return use*n 
        else: 
            return use
    else: 
        return use

def flatten_list(item, n=None): 
    elements = [text_between_quotes(text) for text in item]
    flatten_elements= [item for sublist in elements for item in sublist]
    final_list = []
    for element in flatten_elements: 
        if element not in final_list:
            final_list.append(element)
    one_string = ' '.join(final_list)
    if n == None: 
        return [one_string]
    else: 
        # multiply the list by n to match length to the total number of samples
        string_per_sample = [one_string]*n
        return string_per_sample

SERIES_TITLE = text_between_quotes(series_title_line)
SERIES_ACCESSION = text_between_quotes(series_accession_line)
SERIES_SUBMISSION = text_between_quotes(series_subdate_line)
SERIES_CONTRIBUTORS = flatten_list(series_contributors)
SERIES_SUMMARY = text_between_quotes(series_summary_line)
SERIES_TYPE = text_between_quotes(series_type_line)
SERIES_INSTITUTION = text_between_quotes(series_institution_line)
SERIES_DEPARTMENT = text_between_quotes(series_inst_department_line)
SERIES_CONTACT_NAME = text_between_quotes(series_contact_name_line)
SERIES_CONTACT = text_between_quotes(series_contact_line)
SERIES_BIO_PROJECT = text_between_quotes(series_project_line)
SERIES_SAMPLES_PROTOCOL = flatten_list(series_sample_protocol_lines)

SAMPLE_IDS = text_between_quotes(gsm_line)
N_SAMPLES = len(SAMPLE_IDS)
SAMPLE_TITLE = text_between_quotes(gsm_type_line, n=N_SAMPLES)
SAMPLE_SOURCE = text_between_quotes(sample_source_line, n=N_SAMPLES)
SAMPLE_ORGANISM = text_between_quotes(sample_organism_line, n=N_SAMPLES)
SAMPLE_LIBRARY_STRG = text_between_quotes(sample_lib_strategy_line, n=N_SAMPLES)
SAMPLE_LIBRARY_SORC = text_between_quotes(sample_lib_source_line, n=N_SAMPLES)
SAMPLE_LIBRARY_SLCT = text_between_quotes(sample_lib_select_line, n=N_SAMPLES)
SAMPLE_SRA_LINK = text_between_quotes(sample_sra_line, n=N_SAMPLES )
SAMPLE_BIOSAMP_LINK = text_between_quotes(sample_biosamp_line, n=N_SAMPLES)
SERIES_ACCESSION_PER_SAMPLE = SERIES_ACCESSION * N_SAMPLES

series_df = pd.DataFrame(list(zip(SERIES_ACCESSION, SERIES_TITLE, 
    SERIES_SUBMISSION, SERIES_CONTRIBUTORS, SERIES_SUMMARY,
    SERIES_TYPE, SERIES_BIO_PROJECT, SERIES_SAMPLES_PROTOCOL,
    SERIES_INSTITUTION, SERIES_DEPARTMENT, SERIES_CONTACT_NAME, SERIES_CONTACT)))

series_df.columns = ['SERIES_ACCESSION_ID', 'SERIES_TITLE', 'SUBMISSION_DATE', 
    'CONTRIBUTORS', 'SUMMARY', 'SERIES_TYPE', 'BIO_PROJECT_ID', 'SAMPLE_PROTOCOL',
    'INSTITUTION', 'DEPARTMENT', 'CONTACT_NAME', 'CONTACT']

samples_df = pd.DataFrame(list(zip(SERIES_ACCESSION_PER_SAMPLE, SAMPLE_IDS,
    SAMPLE_TITLE, SAMPLE_SOURCE, SAMPLE_ORGANISM, SAMPLE_LIBRARY_SLCT,
    SAMPLE_LIBRARY_SORC, SAMPLE_LIBRARY_STRG, SAMPLE_BIOSAMP_LINK, SAMPLE_SRA_LINK)))

samples_df.columns = ['SERIES_ACCESSION_ID', 'SAMPLE_ACCESSION_ID', 'SAMPLE_TYPE',
    'SAMPLE_SOURCE', 'SOURCE_ORGANISM', 'LIBRARY_TYPE', 'LIBRARY_SOURCE', 'SEQUENCING_STRATEGY', 
    'BIOSAMP_LINK', 'SRA_LINK']