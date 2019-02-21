import plotly
import plotly.graph_objs as go
from plotly import tools
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
        year_count_dict[p]['plot_obj_scatter'] = go.Scattergl(x=year_count_dict[p]['x_values'], y=year_count_dict[p]['y_values'], mode='lines+markers', name=p, visible=True, marker = dict(size=MARKER_SIZE, color=name_to_color(p), line=dict(width=MARKER_OUTLINE_SIZE)), hoverinfo="y+text", text='{}'.format(p))
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
            month_count_dict[p][y]['plot_obj_scatter'] = go.Scattergl(x=month_count_dict[p][y]['x_values'], y=month_count_dict[p][y]['y_values'], mode='lines+markers', name=p, visible=False, marker = dict(size=MARKER_SIZE, color=name_to_color(p), line=dict(width=MARKER_OUTLINE_SIZE)), hoverinfo="y+text", text='{}'.format(p))
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
        byear_count_dict[p]['plot_obj_scatter'] = go.Bar(x=byear_count_dict[p]['x_values'], y=byear_count_dict[p]['y_values'], name=p, visible=True, marker = dict(color=name_to_color(p)))
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
            bmonth_count_dict[p][y]['plot_obj_scatter'] = go.Bar(x=bmonth_count_dict[p][y]['x_values'], y=bmonth_count_dict[p][y]['y_values'], name=p, visible=False, marker = dict(color=name_to_color(p)))
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
    elif TOP_K_FORMAT is TopKFormat.MONTH_CUMULATIVE:
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

    # Generate buttons and menus
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

    # Box
    bbuttons = list()
    for y in range(MESSENGER_START, MESSENGER_END + 1):
        bbuttons.append(
            dict(
                label = y,
                method = 'update',
                args = [
                    {'visible': bbutton_visibility_vectors[y - MESSENGER_START + 1]},
                    {'title': 'Year ' + str(y)}
                    ]
                ))
    bbuttons.append(dict(
                label = 'Global',
                method = 'update',
                args = [
                    {'visible': bbutton_visibility_vectors[0]},
                    {'title': 'Global'}
                    ]
                ))

    bupdatemenus=list([
        dict(
            type = 'buttons',
            buttons=bbuttons,
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
    # endregion

    # Set figure objects
    # region
    layout = go.Layout(
		title='FriendTrend',
		#autosize=True,
		updatemenus=updatemenus,
        #updatemenus2=bupdatemenus,
		hovermode='closest',
        barmode='stack',
		showlegend=True,
		yaxis=dict(
			type='linear',
			autorange=True
		),
        yaxis2=dict(
			type='linear',
			autorange=True
		),
        xaxis=dict(
            type='date',
            autorange=True # possibly no autorange
        )
    )

    fig = tools.make_subplots(rows=2, cols=1, subplot_titles=('ScatterPlot', 'BarPlot'))

    for t in data:
        fig.append_trace(t, 1, 1)
    for t in bdata:
        fig.append_trace(t, 2, 1)

    fig['layout'].update(
        title='FriendTrend',
		autosize=True,
		updatemenus=updatemenus,
		hovermode='closest',
        barmode='stack',
		showlegend=True,
		yaxis=dict(
			type='log',
			autorange=True
		),
        yaxis2=dict(
			type='linear',
			autorange=True
		),
        xaxis=dict(
            type='date',
            autorange=True # possibly no autorange
        ))

    config = {
        'modeBarButtonsToRemove' : ['toImage', 'select2d', 'lasso2d', 'toggleSpikelines']        
    }
    #endregion

    # PLOT!
    plotly.offline.plot(fig, auto_open=False, config=config, filename=filename)

if __name__== "__main__":
    generate_viz('messages_yearly_scratch.json', 'messages_monthly_scratch.json', 'messages.html')
    #generate_viz('days_interacted_yearly_scratch.json', 'days_interacted_monthly_scratch.json', 'daysinteracted.html')

# see if you can append visibility (scatter box) for all together, shouldnt need 2 update menus