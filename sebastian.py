import plotly
import plotly.graph_objs as go
import json
from collections import defaultdict, Counter
from fnvhash import fnv1a_32
from enum import Enum

## ENUMS ##
class TopKFormat(Enum):
    GLOBAL_K = 0
    MONTH_CUMULATIVE = 1

## DEFINITIONS ##
MESSENGER_START = 2009
MESSENGER_END = 2019
TOP_K_PEOPLE = 10
TOP_K_FORMAT = TopKFormat.MONTH_CUMULATIVE
INCLUDE_FACEBOOKUSER = False
SCRAMBLE_NAMES = False

## INTERNAL DEFINITIONS ##
_SCRAMBLE_NAMES = 0 if SCRAMBLE_NAMES is False else 1

MARKER_SIZE = 15
MARKER_OUTLINE_SIZE = 1.5

## HELPER METHODS ##
# String reverser to hide names
def reverse(s):
    str = "" 
    for i in s: 
        str = i + str
    return str

def name_to_color(name):
    hash = fnv1a_32(name.encode('utf-8'))
    r = (hash & 0xFF000000) >> 24
    g = (hash & 0x00FF0000) >> 16
    b = (hash & 0x0000FF00) >> 8
    val = 'rgb({}, {}, {})'.format(int(r), int(g), int(b))
    return val

def generate_viz(year_data, month_data, filename):
    # Load data
    json_year_count_data = json.loads(open(year_data).read())
    json_month_count_data = json.loads(open(month_data).read())

    # People need color assignments

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
        year_count_dict[p]['plot_obj_scatter'] = go.Scattergl(x=year_count_dict[p]['x_values'], y=year_count_dict[p]['y_values'], mode='lines+markers', name=p, visible=True, marker = dict(size=MARKER_SIZE, color=name_to_color(p), line=dict(width=MARKER_OUTLINE_SIZE)))
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
            month_count_dict[p][y]['plot_obj_scatter'] = go.Scattergl(x=month_count_dict[p][y]['x_values'], y=month_count_dict[p][y]['y_values'], mode='lines+markers', name=p, visible=False, marker = dict(size=MARKER_SIZE, color=name_to_color(p), line=dict(width=MARKER_OUTLINE_SIZE)))
            month_count_dict['METADATA'][y]['total_counts'][p] = month_count_dict[p][y]['total_counts']

    # Keep trace statuses for button interactivity
    trace_status = dict()
    trace_status['scatter'] = {}
    trace_status['scatter']['year_view'] = []
    trace_status['scatter']['month_view'] = {}
    for y in range(MESSENGER_START, MESSENGER_END + 1):
        trace_status['scatter']['month_view'][str(y) + '-01-01'] = []
    trace_status['box'] = {}

    # Generate list of top people (based on option)
    top_ppl_years = defaultdict(int)
    top_ppl_months = dict()
    if TOP_K_FORMAT is TopKFormat.GLOBAL_K:
        # populate year view
        top_ppl_years = Counter(year_count_dict['METADATA']['total_counts']).most_common(TOP_K_PEOPLE)
        # populate month view
        for y in month_count_dict['METADATA']:
            top_ppl_months[y] = Counter(month_count_dict['METADATA'][y]['total_counts']).most_common(TOP_K_PEOPLE)
    elif TOP_K_FORMAT is TopKFormat.MONTH_CUMULATIVE:
        # populate month view
        for y in month_count_dict['METADATA']:
            top_ppl_months[y] = Counter(month_count_dict['METADATA'][y]['total_counts']).most_common(TOP_K_PEOPLE)
        # use month view to populate year view
        for y in top_ppl_months:
            for p in top_ppl_months[y]:
                top_ppl_years[p[0]] += p[1]


    # Populate data based on top people
    data = list()
    data_debug_count = 0
    for p in sorted(top_ppl_years, key=top_ppl_years.get, reverse=True):
        data.append(year_count_dict[p]['plot_obj_scatter'])
        trace_status['scatter']['year_view'].append({
                    'person': p,
                })

    for y in range(MESSENGER_START, MESSENGER_END + 1):
        y0 = str(y) + '-01-01'
        for j in top_ppl_months[y0]:
            if (month_count_dict[j[0]][y0]['plot_obj_scatter'] == []):
                continue
            data.append(month_count_dict[j[0]][y0]['plot_obj_scatter'])
            trace_status['scatter']['month_view'][y0].append({
                    'person': j[0],
                    'year': y
                })

    # Generate list of visibilities for button displays
    button_visibility_vectors = list()
    vector = list()
    for t in trace_status['scatter']['year_view']: # t is dict
        vector.append(True)
    for t, v in trace_status['scatter']['month_view'].items():
        for y in v:
            vector.append(False)
    button_visibility_vectors.append(vector)

    for y in range(MESSENGER_START, MESSENGER_END + 1):
        vector = list()
        for t in trace_status['scatter']['year_view']: # t is dict
            vector.append(False)
        for t, v in trace_status['scatter']['month_view'].items():
            for year in v:
                if year['year'] == y:
                    vector.append(True)
                else:
                    vector.append(False)
        button_visibility_vectors.append(vector)

    # Generate buttons
    buttons = list()
    for y in range(MESSENGER_START, MESSENGER_END + 1):
        buttons.append(
            dict(
                label = y,
                method = 'update',
                args = [
                    {'visible': button_visibility_vectors[y - MESSENGER_START + 1]},
                    {'title': 'Year ' + str(y)}
                    ]
                ))
    buttons.append(dict(
                label = 'Global',
                method = 'update',
                args = [
                    {'visible': button_visibility_vectors[0]},
                    {'title': 'Global'}
                    ]
                ))

    #use execute in layout-updatemenus

    updatemenus=list([
        dict(
            type = 'buttons',
            buttons=buttons,
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
                 args = [dict(yaxis=dict(type='linear', autorange=True))]),
            dict(label = 'Log',
                 method = 'relayout',
                 args = [dict(yaxis=dict(type='log', autorange=True))])]),
            direction = 'down',
            showactive = True,
            x = -0.075,
            xanchor = 'left',
            y = 1,
            yanchor = 'top'
        )])

    layout = go.Layout(
		title='FriendsList',
		autosize=True,
		updatemenus=updatemenus,
		hovermode='closest',
		showlegend=True,
		yaxis=dict(
			type='linear',
			autorange=True
		),
        xaxis=dict(
            type='date',
            autorange=True # possibly no autorange
        )
    )

    # dont forget the config to get rid of buttons we dont need

    fig = {
        "data": data,
        "layout": layout
    }

    config = {
        'modeBarButtonsToRemove' : ['toImage', 'select2d', 'lasso2d', 'toggleSpikelines']        
    }

    plotly.offline.plot(fig, auto_open=False, config=config, filename=filename)

if __name__== "__main__":
    generate_viz('messages_yearly_scratch.json', 'messages_monthly_scratch.json', 'messages.html')
    generate_viz('days_interacted_yearly_scratch.json', 'days_interacted_monthly_scratch.json', 'daysinteracted.html')