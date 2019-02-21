#!/usr/bin/python

import plotly
import plotly.graph_objs as go
import preprocess_data as prepdata
import argparse
import json
import os
from plotly import tools
from collections import defaultdict, Counter
from fnvhash import fnv1a_32
from enum import Enum

## ENUMS ##
class TopKFormat(Enum):
    GLOBAL_K = 0
    MONTHLY = 1

## DEFINITIONS ##
MESSENGER_START = 2009
MESSENGER_END = 2019
TOP_K_PEOPLE = 10
TOP_K_FORMAT = TopKFormat.MONTHLY
INCLUDE_FACEBOOKUSER = False
SCRAMBLE_NAMES = False
VIZ_TARGET_DIRECTORY = 'viz'
MARKER_SIZE = 15
MARKER_OUTLINE_SIZE = 1.5
# if actively editing the code and want a hardcoded location instead of params, edit these
IDE_DEBUGGING = False
IDE_DEBUGGING_NAME = 'Sebastian Rodriguez'

## INTERNAL DEFINITIONS ##
_SCRAMBLE_NAMES = 0 if SCRAMBLE_NAMES is False else 1


## HELPER METHODS ##
#region
def name_to_color(name):
    hash = fnv1a_32(name.encode('utf-8'))
    r = (hash & 0xFF000000) >> 24
    g = (hash & 0x00FF0000) >> 16
    b = (hash & 0x0000FF00) >> 8
    val = 'rgb({}, {}, {})'.format(int(r), int(g), int(b))
    return val
#endregion

def generate_viz(year_data, month_data, filename, title, hidenames, k, kformat):

    # Load flags
    SCRAMBLE_NAMES = hidenames
    _SCRAMBLE_NAMES = 0 if SCRAMBLE_NAMES is False else 1
    TOP_K_PEOPLE = k
    TOP_K_FORMAT = TopKFormat.GLOBAL_K if kformat else TopKFormat.MONTHLY

    # Load data
    json_year_count_data = year_data
    json_month_count_data = month_data

    # Parse scatterplot to dictionaries
    # region
    # Parse year counts
    year_count_dict = defaultdict(lambda: defaultdict(list))
    year_count_dict['METADATA']['total_counts'] = {}
    for y, v in json_year_count_data.items():
        for recp in v:
            if ((recp[0].split('_')[0] == 'facebookuser') and (INCLUDE_FACEBOOKUSER is False)):
                continue
            year_count_dict[recp[0].split('_', 1)[_SCRAMBLE_NAMES]]['x_values'].append(str(y))
            year_count_dict[recp[0].split('_', 1)[_SCRAMBLE_NAMES]]['y_values'].append(recp[1])

    for p in year_count_dict:
        if p == 'METADATA':
            continue
        year_count_dict[p]['total_count'] = sum(year_count_dict[p]['y_values'])
        year_count_dict[p]['plot_obj_scatter'] = go.Scattergl(x=year_count_dict[p]['x_values'], y=year_count_dict[p]['y_values'], mode='lines+markers', name=p, visible=True, marker = dict(size=MARKER_SIZE, color=name_to_color(p), line=dict(width=MARKER_OUTLINE_SIZE)), hoverinfo="y+name")
        year_count_dict['METADATA']['total_counts'][p] = year_count_dict[p]['total_count']

    # Parse month counts (12 graphs per month)
    month_count_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for y, v in json_month_count_data.items():
        month_count_dict['METADATA'][y]['total_counts'] = {}
        for m, v0 in v.items():
            for recp in v0:
                if ((recp[0].split('_')[0] == 'facebookuser') and (INCLUDE_FACEBOOKUSER is False)):
                    continue
                month_count_dict[recp[0].split('_', 1)[_SCRAMBLE_NAMES]][y]['x_values'].append(str(m))
                month_count_dict[recp[0].split('_', 1)[_SCRAMBLE_NAMES]][y]['y_values'].append(recp[1])

    for p in month_count_dict:
        if p == 'METADATA':
            continue
        for y, v in month_count_dict[p].items():
            month_count_dict[p][y]['total_counts'] = sum(month_count_dict[p][y]['y_values'])
            month_count_dict[p][y]['plot_obj_scatter'] = go.Scattergl(x=month_count_dict[p][y]['x_values'], y=month_count_dict[p][y]['y_values'], mode='lines+markers', name=p, visible=False, marker = dict(size=MARKER_SIZE, color=name_to_color(p), line=dict(width=MARKER_OUTLINE_SIZE)), hoverinfo="y+name")
            month_count_dict['METADATA'][y]['total_counts'][p] = month_count_dict[p][y]['total_counts']
    # endregion

    # Parse boxplot to dictionaries
    # region
    # Parse year counts
    byear_count_dict = defaultdict(lambda: defaultdict(list))
    byear_count_dict['METADATA']['total_counts'] = {}
    for y, v in json_year_count_data.items():
        for recp in v:
            if ((recp[0].split('_')[0] == 'facebookuser') and (INCLUDE_FACEBOOKUSER is False)):
                continue
            byear_count_dict[recp[0].split('_', 1)[_SCRAMBLE_NAMES]]['x_values'].append(str(y))
            byear_count_dict[recp[0].split('_', 1)[_SCRAMBLE_NAMES]]['y_values'].append(recp[1])

    for p in byear_count_dict:
        if p == 'METADATA':
            continue
        byear_count_dict[p]['total_count'] = sum(byear_count_dict[p]['y_values'])
        byear_count_dict[p]['plot_obj_scatter'] = go.Bar(x=byear_count_dict[p]['x_values'], y=byear_count_dict[p]['y_values'], name=p, showlegend=False, visible=True, marker = dict(color=name_to_color(p)), hoverinfo="y+name")
        byear_count_dict['METADATA']['total_counts'][p] = byear_count_dict[p]['total_count']

    # Parse month counts (12 graphs per month)
    bmonth_count_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for y, v in json_month_count_data.items():
        bmonth_count_dict['METADATA'][y]['total_counts'] = {}
        for m, v0 in v.items():
            for recp in v0:
                if ((recp[0].split('_')[0] == 'facebookuser') and (INCLUDE_FACEBOOKUSER is False)):
                    continue
                bmonth_count_dict[recp[0].split('_', 1)[_SCRAMBLE_NAMES]][y]['x_values'].append(str(m))
                bmonth_count_dict[recp[0].split('_', 1)[_SCRAMBLE_NAMES]][y]['y_values'].append(recp[1])

    for p in bmonth_count_dict:
        if p == 'METADATA':
            continue
        for y, v in bmonth_count_dict[p].items():
            bmonth_count_dict[p][y]['total_counts'] = sum(bmonth_count_dict[p][y]['y_values'])
            bmonth_count_dict[p][y]['plot_obj_scatter'] = go.Bar(x=bmonth_count_dict[p][y]['x_values'], y=bmonth_count_dict[p][y]['y_values'], name=p, showlegend=False, visible=False, marker = dict(color=name_to_color(p)), hoverinfo="y+name")
            bmonth_count_dict['METADATA'][y]['total_counts'][p] = bmonth_count_dict[p][y]['total_counts']
    # endregion

    # Keep trace statuses for button interactivity
    # region
    trace_status = dict()
    trace_status['year_view'] = []
    trace_status['month_view'] = {}
    for y in range(MESSENGER_START, MESSENGER_END + 1):
        trace_status['month_view'][str(y) + '-01-01'] = []

    btrace_status = dict()
    btrace_status['year_view'] = []
    btrace_status['month_view'] = {}
    for y in range(MESSENGER_START, MESSENGER_END + 1):
        btrace_status['month_view'][str(y) + '-01-01'] = []
    # endregion

    # Generate list of top people (based on option)
    # region
    top_ppl_years = defaultdict(int)
    top_ppl_months = dict()
    btop_ppl_years = defaultdict(int)
    btop_ppl_months = dict()

    if TOP_K_FORMAT is TopKFormat.GLOBAL_K:
        # populate year view
        top_ppl_years = Counter(year_count_dict['METADATA']['total_counts']).most_common(TOP_K_PEOPLE)
        btop_ppl_years = Counter(byear_count_dict['METADATA']['total_counts']).most_common(TOP_K_PEOPLE)
        # populate month view
        for y in month_count_dict['METADATA']:
            top_ppl_months[y] = Counter(month_count_dict['METADATA'][y]['total_counts']).most_common(TOP_K_PEOPLE)
        for y in bmonth_count_dict['METADATA']:
            btop_ppl_months[y] = Counter(bmonth_count_dict['METADATA'][y]['total_counts']).most_common(TOP_K_PEOPLE)
    elif TOP_K_FORMAT is TopKFormat.MONTHLY:
        # populate month view
        for y in month_count_dict['METADATA']:
            top_ppl_months[y] = Counter(month_count_dict['METADATA'][y]['total_counts']).most_common(TOP_K_PEOPLE)
        for y in bmonth_count_dict['METADATA']:
            btop_ppl_months[y] = Counter(bmonth_count_dict['METADATA'][y]['total_counts']).most_common(TOP_K_PEOPLE)
        # use month view to populate year view
        for y in top_ppl_months:
            for p in top_ppl_months[y]:
                top_ppl_years[p[0]] += p[1]
        for y in btop_ppl_months:
            for p in btop_ppl_months[y]:
                btop_ppl_years[p[0]] += p[1]
    # endregion

    # Populate data based on top people
    # region
    # Scatter
    data = list()
    if TOP_K_FORMAT is TopKFormat.GLOBAL_K:
        for p in top_ppl_years:
            data.append(year_count_dict[p[0]]['plot_obj_scatter'])
            trace_status['year_view'].append({
                        'person': p,
                    })
    elif TOP_K_FORMAT is TopKFormat.MONTHLY:
        for p in sorted(top_ppl_years, key=top_ppl_years.get, reverse=True):
            data.append(year_count_dict[p]['plot_obj_scatter'])
            trace_status['year_view'].append({
                        'person': p,
                    })

    for y in range(MESSENGER_START, MESSENGER_END + 1):
        y0 = str(y) + '-01-01'
        for j in top_ppl_months[y0]:
            if (month_count_dict[j[0]][y0]['plot_obj_scatter'] == []):
                continue
            data.append(month_count_dict[j[0]][y0]['plot_obj_scatter'])
            trace_status['month_view'][y0].append({
                    'person': j[0],
                    'year': y
                })

    # Box
    bdata = list()
    if TOP_K_FORMAT is TopKFormat.GLOBAL_K:
        for p in btop_ppl_years:
            bdata.append(byear_count_dict[p[0]]['plot_obj_scatter'])
            btrace_status['year_view'].append({
                        'person': p,
                    })
    elif TOP_K_FORMAT is TopKFormat.MONTHLY:
        for p in sorted(btop_ppl_years, key=btop_ppl_years.get, reverse=True):
            bdata.append(byear_count_dict[p]['plot_obj_scatter'])
            btrace_status['year_view'].append({
                        'person': p,
                    })

    for y in range(MESSENGER_START, MESSENGER_END + 1):
        y0 = str(y) + '-01-01'
        for j in btop_ppl_months[y0]:
            if (bmonth_count_dict[j[0]][y0]['plot_obj_scatter'] == []):
                continue
            bdata.append(bmonth_count_dict[j[0]][y0]['plot_obj_scatter'])
            btrace_status['month_view'][y0].append({
                    'person': j[0],
                    'year': y
                })
    # endregion

    # Generate list of visibilities for button displays
    # region
    # Scatter
    button_visibility_vectors = list()
    vector = list()
    for t in trace_status['year_view']: # t is dict
        vector.append(True)
    for t, v in trace_status['month_view'].items():
        for y in v:
            vector.append(False)
    button_visibility_vectors.append(vector)

    for y in range(MESSENGER_START, MESSENGER_END + 1):
        vector = list()
        for t in trace_status['year_view']: # t is dict
            vector.append(False)
        for t, v in trace_status['month_view'].items():
            for year in v:
                if year['year'] == y:
                    vector.append(True)
                else:
                    vector.append(False)
        button_visibility_vectors.append(vector)

    # Box
    bbutton_visibility_vectors = list()
    vector = list()
    for t in btrace_status['year_view']: # t is dict
        vector.append(True)
    for t, v in btrace_status['month_view'].items():
        for y in v:
            vector.append(False)
    bbutton_visibility_vectors.append(vector)

    for y in range(MESSENGER_START, MESSENGER_END + 1):
        vector = list()
        for t in btrace_status['year_view']: # t is dict
            vector.append(False)
        for t, v in btrace_status['month_view'].items():
            for year in v:
                if year['year'] == y:
                    vector.append(True)
                else:
                    vector.append(False)
        bbutton_visibility_vectors.append(vector)
    # endregion

    # Generate buttons, menus, and UI
    # region
    # Scatter
    buttons = list()
    for y in range(MESSENGER_START, MESSENGER_END + 1):
        buttons.append(
            dict(
                label = y,
                method = 'update',
                args = [
                    {'visible': button_visibility_vectors[y - MESSENGER_START + 1]},
                    {'title': 'FriendTrend - {}: {}'.format(title, str(y)) }
                    ]

                ))
    buttons.append(dict(
                label = 'Overview',
                method = 'update',
                args = [
                    {'visible': button_visibility_vectors[0]},
                    {'title': 'FriendTrend - {}'.format(title) }
                    ]

                ))
    updatemenus=list([
        dict(
            type = 'buttons',
            buttons=buttons,
            active=11,
            direction = 'left',
            showactive = True,
            x = 0.5,
            xanchor = 'auto',
            y = -0.1,
            yanchor = 'auto' 
        ),
        dict(
            type='dropdown',
            buttons=list([
            dict(label = 'Linear',
                 method = 'relayout',
                 args = [dict(yaxis=dict(type='linear', autorange=True, domain=[0.51, 1]), yaxis2=dict(domain=[0, 0.49]))]),
            dict(label = 'Log',
                 method = 'relayout',
                 args = [dict(yaxis=dict(type='log', autorange=True, domain=[0.51, 1]), yaxis2=dict(domain=[0, 0.49]))])]),
            direction = 'down',
            showactive = True,
            x = -0.075,
            xanchor = 'left',
            y = 1,
            yanchor = 'top'
        )])

    fig = tools.make_subplots(rows=2, cols=1)

    for t in data:
        fig.append_trace(t, 1, 1)
    for t in bdata:
        fig.append_trace(t, 2, 1)

    fig['layout'].update(
        title='FriendTrend - ' + str(title),
		autosize=True,
		updatemenus=updatemenus,
		hovermode='closest',
        barmode='stack',
		showlegend=True,
        legend=dict(traceorder='normal'),
		yaxis1=dict(
			type='linear',
			autorange=True,
            domain=[0.51, 1]
		),
        yaxis2=dict(
			type='linear',
			autorange=True,
            domain=[0, 0.49]
		),
        xaxis1=dict(
            type='date',
            tickformat='%b %Y',
            showgrid=True,
            autorange=True,
            visible=True
        ),
        xaxis2=dict(
            type='date',
            tickformat='%b %Y',
            showgrid=True,
            autorange=True,
            visible=True
        ))

    config = {
        'modeBarButtonsToRemove' : ['toImage', 'select2d', 'lasso2d', 'toggleSpikelines']        
    }
    #endregion

    # PLOT!
    plotly.offline.plot(fig, auto_open=True, config=config, filename=filename)

if __name__== "__main__":

    try:
        os.mkdir(VIZ_TARGET_DIRECTORY)
    except FileExistsError:
        pass

    if IDE_DEBUGGING is False:
        parser = argparse.ArgumentParser()

        parser.add_argument('--datapath', default='data/messages/inbox/', help='path to the messages/inbox sub-directory in the Messenger data dump')
        parser.add_argument('--hidenames', default=False, action='store_true', help='whether or not to use real names in the visualization')
        parser.add_argument('--topk', default=10, type=int, help='number of top K friends to show')
        parser.add_argument('--topkglobal', default=False, action='store_true', help='populate the top K friends globally and display <K for each monthly view')
        parser.add_argument('name', help='your Facebook display name (as written)')

        args = parser.parse_args()

        datasets = prepdata.main(args.datapath, args.name, False)

        generate_viz(datasets.messages_yearly, datasets.messages_monthly, VIZ_TARGET_DIRECTORY + '/' + args.name + '-messages.html', 'Total Messages', args.hidenames, args.topk, args.topkglobal)
        generate_viz(datasets.days_interacted_yearly, datasets.days_interacted_monthly, VIZ_TARGET_DIRECTORY + '/' + args.name + '-daysinteracted.html', 'Days Interacted', args.hidenames, args.topk, args.topkglobal)
    else:
        datasets = prepdata.main('data/messages/inbox/', IDE_DEBUGGING_NAME, False, args.hidenames, args.topk, args.topkglobal)

        generate_viz(datasets.messages_yearly, datasets.messages_monthly, VIZ_TARGET_DIRECTORY + '/' + IDE_DEBUGGING_NAME + '-messages.html', 'Total Messages', args.hidenames, args.topk, args.topkglobal)
        generate_viz(datasets.days_interacted_yearly, datasets.days_interacted_monthly, VIZ_TARGET_DIRECTORY + '/' + IDE_DEBUGGING_NAME + '-daysinteracted.html', 'Days Interacted', args.hidenames, args.topk, args.topkglobal)
    