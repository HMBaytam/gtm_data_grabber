import json
import pandas as pd
import ga4_functions as ga4
import ua_functions as ua


if __name__ == "__main__":
    data = json.loads(open('gtm.json').read())

    ga4_data = ga4.ga4_data(data)
    ua_data = ua.get_all_ua_tag_info(data)

    ga4_data.to_csv('ga4_tag_list.csv', index=False)
    ua_data.to_csv('ua_tag_list.csv', index=False)
    
    with pd.ExcelWriter('output.xlsx') as writer:  
        ga4_data.to_excel(writer, sheet_name='ga4_data', index=False)
        ua_data.to_excel(writer, sheet_name='ua_data', index=False)

# pretty print json object 
# print(json.dumps(parsed, indent=4, sort_keys=True))

# test csv output
# df.to_csv('ua.csv', index=False)