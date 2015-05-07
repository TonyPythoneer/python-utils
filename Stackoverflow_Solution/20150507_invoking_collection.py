# Link:
# http://stackoverflow.com/questions/30073691/how-to-carry-out-this-aggregation-in-python/30097122#30097122

response = [
    {'country': 'KR', 'values': ['Server1']},
    {'country': 'IE', 'values': ['Server1', 'Server3', 'Server2']},
    {'country': 'IE', 'values': ['Server1', 'Server3']},
    {'country': 'DE', 'values': ['Server1']},
    {'country': 'DE', 'values': ['Server2']},
]

# merge repeat country
new_res = {}
for e in response:
    if e['country'] not in new_res:
        new_res[e['country']] = e['values']
    else:
        new_res[e['country']].extend(e['values'])
print new_res

'''
{
    'KR': ['Server1'],
    'DE': ['Server1', 'Server2'],
    'IE': ['Server1', 'Server3', 'Server2', 'Server1', 'Server3']
}
'''

from collections import Counter
new_list = []
for country, values in new_res.items():
    # elements are stored as dictionary keys and their counts are stored as dictionary values
    merge_values = Counter(values)

    # calculate percentage
    new_values = []
    total = sum(merge_values.values())
    for server_name, num in merge_values.items():
        #ex: Server1-40.0
        new_values.append("{0}-{1:.1f}".format(server_name, num*100/total))

    percent = merge_values["Server1"]*1.0*100/total

    new_list.append({"country": country,
                     "percent": percent,
                     "values": new_values})

print new_list

import pprint
pprint.pprint(new_list)

'''
[{'country': 'KR', 'values': ['Server1-100.0']},
 {'country': 'DE', 'values': ['Server1-50.0', 'Server2-50.0']},
 {'country': 'IE', 'values': ['Server1-40.0', 'Server2-20.0', 'Server3-40.0']}]
'''
