import pandas as pd

def find_event_type(plot_times, df_event):
    event_type_list = []
    for plot_time in plot_times:
        mask = (df_event['BEGIN_DATE_TIME'] <= plot_time) & (plot_time <= df_event['END_DATE_TIME'])
        filtered_events = df_event.loc[mask, 'EVENT_TYPE']
        event_type_list.append(filtered_events.iloc[0] if not filtered_events.empty else "None")

    return event_type_list
