import pandas as pd
import numpy as np

import timeit
import os
import pickle

import sklearn.cluster
from Levenshtein import distance

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

# drug_char dict
drug_char_dict = {'1':'Suspect', '2':'Concominant', '3': 'Interacting', '':'Unknown'}
# admin_route dict
admin_route_dict = {'001': 'Auricular', '002': 'Buccal', '003': 'Cutaneous', '004': 'Dental', '005': 'Endocervical',
                    '006': 'Endosinusal', '007': 'Endotracheal', '008':'Epidural', '009':'Extra-amniotic',
                    '010':'Hemodialysis', '011':'Intra corpus cavernosum', '012': 'Intra-amniotic', '013': 'Intra-arterial',
                   '014': 'Intra-articual', '015': 'Intra-uterine', '016': 'Intracardiac', '017': 'Intracavernous',
                   '018': 'Intracerebral', '019': 'Intracervical', '020': 'Intracisternal', '021': 'Intracorneal',
                   '022': 'Intracoronary', '023': 'Intradermal', '024': 'Intradiscal', '025': 'Intrahepatic', '026': 'Intralesional',
                   '027': 'Intralymphatic', '028': 'Intramedullar', '029': 'Intrameningeal', '030': 'Intramuscular',
                    '031': 'Intraocular', '032': 'Intrapericardial', '033': 'Intraperitoneal', '034': 'Intrapleural',
                   '035': 'Intrasynovial', '036': 'Intratumor', '037': 'Intrathecal', '038': 'Intrathoracic', '039': 'Intratracheal',
                   '040': 'Intravenous bolus', '041': 'Intravenous drip', '042':'Intravenous','043': 'Intravesical',
                   '044': 'Iontophoresis', '045': 'Nasal', '046': 'Occlusive dressing technique', '047': 'Ophthalmic',
                   '048': 'Oral', '049': 'Oropharingeal', '050': 'Other', '051':'Parenteral', '052':'Periarticular',
                   '053': 'Perineural', '054':'Rectal', '055':'Respiratory (inhalation)','056':'Retrobulbar', '057':'Sunconjunctival',
                   '058': 'Subcutaneous', '059': 'Subdermal', '060':'Sublingual', '061':'Topical', '062':'Transdermal',
                   '063':'Transmammary', '064':'Transplacental', '065':'Unknown', '066':'Urethral', '067':'Vaginal',
                   'NA':'Not Listed', '':'Not Listed'}


# Program for generating list of unique values from a df_column
def unique_gen(test_col, df_2):
    """
    Takes in the df_column and generates a list of unique entries
    """
    series_data = df_2[test_col]
    column_list = []
    # Get unique entries raw, this will have redundancies bc it is order dependent
    tmp = series_data.unique()
    for i in range(0,len(tmp)):
        column_list.append(tmp[i])

    # Remove all commas
    column_list = [w.replace(',', '') for w in column_list]
    # Replace special chars with commas
    column_list = [w.replace('_', ',') for w in column_list]
    column_list = [w.replace('.', ',') for w in column_list]

    # Turn repeated commas into just one comma
    commas = ',,'
    for i in range(0,100):
        column_list = [w.replace(commas, ',') for w in column_list]
        commas = commas + ','
    column_list = [w.replace(',,,', ',') for w in column_list]
    column_list = [w.replace(',,', ',') for w in column_list]

    # Remove the first comma
    column_list = [w.lstrip(',') for w in column_list]
    # Remove the last comma
    column_list = [w.rstrip(',') for w in column_list]

    # Separate out entries with multiple entries
    column_list = [w.split(',') for w in column_list]

    # Organize into one long list where redundancies are separated
    dummy_list = []
    for i in range(0,len(column_list[:])):
        for j in range(0,len(column_list[i][:])):
            dummy_list.append(column_list[i][j])

    # Get unique values
    unique = list(set(dummy_list))

    if test_col == 'drug_char':
        result = []
        result = [drug_char_dict[l1] for l1 in unique]
        unique = result

    if test_col == 'admin_route':
        result = []
        result = [admin_route_dict[l1] for l1 in unique]
        unique = result
    if test_col == 'unii':
        result = []
        result = [unii_dict[l1] for l1 in unique]
        unique = result
    return unique


# This function takes the pd.series from the downloaded data and converted it into a list of lists to
# handle and track multiple drug entries
def entries_col_to_lists(test_col, df_2):
    """
    This function takes the pd.series (df column) from the downloaded data and converts
    it to a nested list to
    handle and track multiple drug, and opendfa entries
    """
    print('Converting series to list...')

    series_data = df_2[test_col]

    column_list = []
    for i in range(0,len(series_data)):
        column_list.append(series_data[i])

    print('Removing commas...')
    # Remove all commas
    column_list = [w.replace(',', '') for w in column_list]
    # Strip first occurence of '_._'
    column_list = [w.lstrip('_._') for w in column_list]
    # Strip first occurence of '_.._'
    column_list = [w.lstrip('_.._') for w in column_list]

    print('Converting to list of lists')
    # Separate out entries on '_._' for multiple druges
    column_list = [w.split('_._') for w in column_list]
    # Separate out entries on '_.._' for multiple openfda apps
    column_list = [[w.split('_.._') for w in word] for word in column_list]
    # clean up the first hyphen
    column_list = [[[w.lstrip('_') for w in word1] for word1 in word] for word in column_list]

    if test_col == 'drug_char':
        result = []
        result = [[[drug_char_dict[l1] for l1 in l2] for l2 in l3] for l3 in column_list]
        column_list = result
    if test_col == 'admin_route':
        result = []
        result = [[[admin_route_dict[l1] for l1 in l2] for l2 in l3] for l3 in column_list]
        column_list = result
    if test_col == 'unii':
        result = []
        result = [[[unii_dict[l1] for l1 in l2] for l2 in l3] for l3 in column_list]
        column_list = result

    return column_list

def value_gen(col_as_list, unique_list):
    """
    Takes in the column as a list and generates counts for unique entries
    """
    count = []
    percent = []
    i = 0
    print('Progress on {} entries...'.format(len(unique_list)))
    for search in unique_list:
        # Generate nested list of booleans
        check = [[search in w1 for w1 in word] for word in col_as_list]
        # Check if any patient record is True
        indeces = [any(word) for word in check]
        # Get count
        count.append(sum(indeces))
        # Get percent
        percent.append(round(sum(indeces)/len(col_as_list)*100,2))

        # Progress tracker
        i += 1
        if i % 1000 == 0:
            print('{} entries scanned.'.format(i))
        if i == len(unique_list):
            print('{} entries scanned.'.format(i))

    # Convert to Dataframe
    data = [unique_list, count, percent]
    df_values = pd.DataFrame(data).transpose() # convert to df
    df_values.columns = ['Entry', 'Count', 'Percent'] # set column names

    return df_values

# This function does the data wrangling with the above functions.
def data_wrangling(df_2, test_col):
    """
    Takes in a df and column label and runs it through unique_list, entries_col_to_lists, and value_gen. Then saves the files.
    """
    starttime = timeit.default_timer()
    print('Working on column \'{}\'\n'.format(test_col))
    # Extract out unique entries for a feature column
    unique_list = unique_gen(test_col, df_2)
    print('{} unique entries.'.format(len(unique_list)))

    # Generate embedded lists
    col_as_list = entries_col_to_lists(test_col, df_2)
    print('Check that len of lists col ({}) is equal to len of series ({})'.format(len(col_as_list), len(df_2[test_col])))

    # Generate df for value counts
    unique_counts = value_gen(col_as_list, unique_list)

    print('Saving...')
    # List of unique entries
    file_name = './progress/wrangled/' + test_col + '_unique.txt'
    with open(file_name, "wb") as fp:   #Pickling
        pickle.dump(unique_list, fp)

    # dataframe of counts for each entry
    df_file = './progress/wrangled/' + test_col + '_counts.csv'
    unique_counts.to_csv(df_file, index = False)  # where to save it, usually as a .pkl
    print('Size of saved df is {d2:0.3f} MB.'.format(d2 = os.path.getsize(df_file)/10**6))

    # list of lists for entries
    file_name = './progress/wrangled/' + test_col + '_aslist.txt'
    with open(file_name, "wb") as fp:   #Pickling
        pickle.dump(col_as_list, fp)

    elapsed = timeit.default_timer()-starttime
    print('Done with \'{}\' in {} seconds. \n\n'.format(test_col, round(elapsed,2)))

# This function calculates the percent outcome for serious metrics from a given feature input
def percent_gen(test_col, correlate_col, df_2, num_entries = 5):
    """
    Takes in a test_col, correlate_col, and df then saves a df with ratios over [some search list].
    """
    #### Load in the data for the test_col ####
    # Load the unique names
    file_name = './progress/wrangled/' + test_col + '_unique.txt'
    with open(file_name, "rb") as fp:   # Unpickling
        unique_list = pickle.load(fp)
    # Load data frame of counts
    df_file = './progress/wrangled/' + test_col + '_counts.csv'
    unique_counts = pd.read_csv(df_file)
    # load list of lists
    file_name = './progress/wrangled/' + test_col + '_aslist.txt'
    with open(file_name, "rb") as fp:   # Unpickling
        col_as_list = pickle.load(fp)

    # Generate search queries from unique_counts
    if len(unique_list) < num_entries:
        num_entries = len(unique_list)

    search = unique_counts.sort_values(by = 'Percent', axis = 0, ascending = False)['Entry'][0:num_entries]
    # initialize lists
    s1 = []
    count_s1 = []
    c1 = []
    count_s1_0 = []
    count_s1_1 = []
    percent_1 = []
    consolidate = []

    i = 0
    print('{} searches to perform with \'{}\' and \'{}\'.\n'.format(num_entries, test_col, correlate_col))
    # Generate percents for all search entries
    for search1 in search:
        if search1 is not np.nan:
            # Initialize df_2
            df_tmp = df_2[[test_col, correlate_col]]

            # list of search entries
            s1.append(search1)
            # list of correlate_col
            c1.append(correlate_col)

            # Get nested list of booleans if one of the entries are in the col_as_list
            check = [[str(search1) in w1 for w1 in word] for word in col_as_list]
            # Get booleans that serve as indeces if any entry is true
            indeces = [any(word) for word in check]
            # add to list
            count_s1.append(sum(indeces))

            # filter out rows
            df_tmp = df_tmp[indeces]
            # filter out nas
            df_tmp = df_tmp.dropna()

            # get correlate = 0, 1
            if correlate_col == 'serious':
                s1_0 = len(df_tmp[df_tmp[correlate_col] == 2])
                s1_1 = len(df_tmp[df_tmp[correlate_col] == 1])
            else:
                s1_0 = len(df_tmp[df_tmp[correlate_col] == 0])
                s1_1 = len(df_tmp[df_tmp[correlate_col] == 1])
            count_s1_0.append(s1_0)
            count_s1_1.append(s1_1)

            # ratio of 1 to 0
            if s1_0 == 0 and s1_1 == 0:
                percent_1.append('Undefined')
            else:
                percent_1.append(round(s1_1/(s1_0+s1_1)*100,2))

            # consolidate into another list for all search entries
            consolidate.append([s1, c1, count_s1, count_s1_0, count_s1_1, percent_1])

            # Progress Tracker
            i += 1
            if i%100 == 0:
                print('{} searches complete.'.format(i))
            if i == num_entries:
                print('{} searches complete.'.format(i))

    # set df
    df_ratios = pd.DataFrame([s1, c1, count_s1,  count_s1_0, count_s1_1, percent_1]).transpose()
    df_ratios.columns = ['Entry', 'Correlate', 'Count_entry',  'Serious_0', 'Serious_1', 'Percent_1']

    # Save the df_ratios
    # dataframe of counts for each entry
    df_file = './progress/wrangled/percent_1/' + test_col + '_' + correlate_col +  '_percent_1.csv'
    df_ratios.to_csv(df_file, index = False)  # where to save it, usually as a .pkl
    print('Done.\n')


# One Hot encoder
def one_hot_encode_drugs(test_col, df):
    """
    Takes in a column and returns a one-hot-encoded df from the categorical values.
    """
    # Convert df column to a list
    col_list = entries_col_to_lists(test_col, df)

    # Undo the first nested layer
    col_list = [[x for y in entry for x in y] for entry in col_list]

    # One hot encoder
    # For more information, see the following link:
    # https://stackoverflow.com/questions/46864816/convert-data-frame-of-comma-separated-strings-to-one-hot-encoded
    print('One Hot Encoding...')
    df_OHE = pd.Series(col_list).str.join(',').str.split(',',expand = True).apply(pd.Series.value_counts, 1).iloc[:,:].fillna(0)
    print('Done.')
    return df_OHE





def entry_condenser(unique_col, char_lim = None):
    """
    Takes in a list of unique column entries and returns a dictionary to convert a col to lower-d space
    """
    # https://stats.stackexchange.com/questions/123060/clustering-a-long-list-of-strings-words-into-similarity-groups
    words_og = unique_col

    # Cut off all but the first set of characters
    if char_lim is not None:
        words = [w[:char_lim] for w in words_og]
    else:
        words = words_og

    # Get similarity matrix
    words = np.asarray(words)
    lev_similarity = -1*np.array([[distance(w1,w2) for w1 in words] for w2 in words])
    # Fit an affinity model
    affprop = sklearn.cluster.AffinityPropagation(affinity="precomputed", damping=0.5)
    affprop.fit(lev_similarity)

    # Group the words with their respective clusters
    cluster_list = []
    gen_name_list = []
    for cluster_id in np.unique(affprop.labels_):
        exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
        cluster = np.unique(words[np.nonzero(affprop.labels_==cluster_id)])
        cluster_str = ", ".join(cluster)
        for name in cluster:
            cluster_list.append(exemplar)
            gen_name_list.append(name)

    gen_name_dict = dict(zip(gen_name_list, cluster_list))

    return gen_name_dict
