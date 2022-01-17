import json
import pandas as pd

def get_all_ua_tags(data):
    # gets all ua tags in gtm
    all_ua_tags = [
        [
            x['tagId'],
            x['name'],
            x['parameter']
        ]  for x in data['containerVersion']['tag'] if 'ua' in x['type']
    ]

    # created a DataFrame from the 
    return pd.DataFrame (all_ua_tags, columns = ['tag_id', 'tag_name', 'parameter_object']), all_ua_tags

def get_ua_tag_track_type(all_ua_tags):
    # the following creates a dictionary to map tag ids with their corresponding tracking type - page view or event
    ua_event_track_type = {}
    for line in all_ua_tags:
        for params in line[-1]:
            if params['key'] == 'trackType':
                ua_event_track_type[str(line[0])] = str(params['value'])
    return ua_event_track_type
    
def get_ua_event_parameters(all_ua_tags):
    # the following creates a dictionary to map tag ids with their corresponding event category, action, and label (if available)
    ua_event_parameters = {}
    for line in all_ua_tags:
        list = []
        for params in line[-1]:
            if params['key'] == 'eventCategory':
                list.append('Category: '+params['value'])
            if params['key'] == 'eventAction':
                list.append('Action: '+params['value'])
            if params['key'] == 'eventLabel':
                list.append('Label: '+params['value'])
            ua_event_parameters[str(line[0])] = '\n'.join(list)
    return ua_event_parameters
    
def get_ua_event_dimensions(all_ua_tags):
    # the following creates a dictionary to map tag ids with their corresponding custom event dimensions (if available)
    ua_custom_event_dimensions = {}
    for line in all_ua_tags:
        for params in line[-1]:
            if params['key'] == 'dimension':
                cds = []
                for el in params['list']:
                    cds.append(f"cd_{el['map'][0]['value']}_{el['map'][1]['value']}")
                ua_custom_event_dimensions[str(line[0])] = '\n'.join(cds)
    return ua_custom_event_dimensions

def get_ua_event_metrics(all_ua_tags):
    ''' 
    This for loop is not working, it's always returning no metrics even though the json file has custom event metrics
    the following creates a dictionary to map tag ids with their corresponding custom event metrics (if available)
    '''
    ua_event_custom_metrics = {}
    for line in all_ua_tags:
        for params in line[-1]:
            if params['key'] == 'metric':
                cms = []
                for el in params['list']:
                    cms.append(f"cm_{el['map'][0]['value']}_{el['map'][1]['value']}")
                ua_event_custom_metrics[str(line[0])] = '\n'.join(cms)
    
    return ua_event_custom_metrics

def get_ua_tag_triggers(data):
    # the following creates a dictionary to map tag ids with their corresponding triggers
    ua_tag_trigger_id = {
        tag['tagId']: tag['firingTriggerId'] for tag in data['containerVersion']['tag'] if tag['type'] == 'ua'
    }
    for item in ua_tag_trigger_id:
        ua_trigger_names = [
            trigger['name'] for trigger in data['containerVersion']['trigger'] if trigger['triggerId'] in ua_tag_trigger_id[item]
        ]
        ua_tag_trigger_id[item] = '\n'.join(ua_trigger_names)
    return ua_tag_trigger_id

def get_ua_tag_blocking_triggers(data):                
    ua_tag_blocking_trigger_id = {
        tag['tagId']: tag['blockingTriggerId'] for tag in data['containerVersion']['tag'] if tag['type'] == 'ua' and 'blockingTriggerId' in tag.keys()
    }
    for item in ua_tag_blocking_trigger_id:
        ua_trigger_names = [
            trigger['name'] for trigger in data['containerVersion']['trigger'] if trigger['triggerId'] in ua_tag_blocking_trigger_id[item]
        ]
        ua_tag_blocking_trigger_id[item] = '\n'.join(ua_trigger_names)
    return ua_tag_blocking_trigger_id

def get_all_ua_tag_info(data):
    df, ua_tags = get_all_ua_tags(data)
    df['track_type'] = df['tag_id'].map(get_ua_tag_track_type(ua_tags))
    df['event_parameters'] = df['tag_id'].map(get_ua_event_parameters(ua_tags))
    df['event_dimensions'] = df['tag_id'].map(get_ua_event_dimensions(ua_tags))
    df['event_metrics'] = df['tag_id'].map(get_ua_event_metrics(ua_tags))
    df['tag_triggers'] = df['tag_id'].map(get_ua_tag_triggers(data))
    df['tag_blocking_triggers'] = df['tag_id'].map(get_ua_tag_blocking_triggers(data))
    df.drop(['parameter_object'], axis=1, inplace=True)
    return df

# data = json.loads(open('gtm.json').read())
# tag_with_cm = data['containerVersion']['tag'][55]

# ua_event_custom_metrics = {}
# test_cms = []

# for params in tag_with_cm['parameter']:
#     if params['key'] == 'metric':
#         for el in params['list']:
#             test_cms.append(f'cm_{el["map"][0]["value"]}_{el["map"][1]["value"]}')
#         ua_event_custom_metrics['55'] = '\n'.join(test_cms)
# print(json.dumps(ua_event_custom_metrics, indent=4, sort_keys=True))