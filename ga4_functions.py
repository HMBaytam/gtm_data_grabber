import pandas as pd

def get_all_ga4_tags(data):
    '''
    function input = {json object}
    function return = list [int, str, str, list]

    This function runs a long list comprehension sequence that will extract a list that returns the following

    [the gtm tag id, the gtm tag name, the ga4 event name, [a list with all the event parameters]]
    '''
    ga4_tags = [
        [
            # tagId refers to gtm tag id
            x['tagId'],

            # name refers to gtm tag name
            x['name'],

            # parameter.[0].value refers to the ga4 event name
            # object.array.object
            x['parameter'][0]['value'],

            # this is an embedded list comprehension that returns a list with all the parameter names
            [param['map'][0]['value'] for param in x['parameter'][1]['list']]
        ]  
        # 'type': 'gaawe' refers to GA4 event configuration 
        # P.S - 'type': 'gaawc' refers to GA4 base tag configuration that holds the tacking id and other base settings
        for x in data['containerVersion']['tag'] if 'gaawe' in x['type']
    ]
    return ga4_tags

def export_cleaned_ga4_tags(ga4_tags):
    '''
    function input = list [int, str, str, list]
    function return = None
    Exports dataFrame to csv
    dataFrame('int', 'str', 'str', 'str')

    This function takes in the list generated from the get_all_ga4_tags() function and converts it to a pandas dataFrame
    The clean up process is changing the list of ga4 event parameters into a string. 
    The list is joined on '\n' new line -- this way the column with the ga4 event parameters will be easily readable by th CSV user
    '''

    # create a dataFrame from the ga4_tags list input
    df = pd.DataFrame (ga4_tags, columns = ['tag_id', 'tag_name', 'event_name', 'event_params_list'])

    # this list comprehension creates a list with a string of event parameters 
    event_params_string = ['\n'.join(list) for list in df['event_params_list']]

    # event parameters string added to the DataFrame
    df['event_parameters'] = event_params_string

    # dropped the column with the list of event parameters
    df.drop(['event_params_list'], axis=1, inplace=True)

    return df

def ga4_data(data):
    return export_cleaned_ga4_tags(
        get_all_ga4_tags(data)
    )
