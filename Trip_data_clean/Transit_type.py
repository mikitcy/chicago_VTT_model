import pandas as pd

def get_transit_types(row):

    # transit type for all combinations
    types = []

    if row['Direction'] == 0:
        types.append('NA')
    else:
        if row['Bus_duration'] > 0:
            types.append('Bus')
        if row['Subway_duration'] > 0:
            types.append('Subway')
        if row['Train_duration'] > 0:
            types.append('Train')

    return ' & '.join(types) if types else 'Walk'




