#Dashboard
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_leaflet as dl
import plotly.express as px
import pandas as pd
import base64
from CRUD_Python_Module import AnimalShelter

#Database credentials
username = "aacuser"
password = "password123"

#Connect to database
db = AnimalShelter(username, password)
df = pd.DataFrame.from_records(db.read({}))
if '_id' in df.columns:
    df.drop(columns=['_id'], inplace=True)

app = Dash(__name__)

#Logo
image_filename = 'Grazioso Salvare Logo.png'
try:
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    logo_img = html.Img(
        src='data:image/png;base64,{}'.format(encoded_image.decode()),
        style={'height':'100px'}
    )
except FileNotFoundError:
    logo_img = html.Div("Logo file not found", style={'color':'red', 'font-weight':'bold'})

app.layout = html.Div([
    html.Center(html.B(html.H1('CS-340 Dashboard'))),
    html.H2("Aubrey Karczewski"),
    html.Center(logo_img),
    html.Hr(),
    html.Hr(),

    #Filter options
    html.Div([
        html.Label("Filter by Rescue Type:"),
        dcc.RadioItems(
            id='filter-type',
            options=[
                {'label': 'Water Rescue', 'value': 'Water Rescue'},
                {'label': 'Mountain/Wilderness Rescue', 'value': 'Mountain/Wilderness'},
                {'label': 'Disaster/Individual Tracking', 'value': 'Disaster/Tracking'},
                {'label': 'Reset', 'value': 'Reset'}
            ],
            value='Reset',
            labelStyle={'display': 'inline-block', 'margin-right':'15px'}
        )
    ]),
    html.Hr(),

    #Data table
    dash_table.DataTable(
        id='datatable-id',
        columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],
        data=df.to_dict('records'),
        page_size=10,
        sort_action='native',
        filter_action='native',
        row_selectable='single',
        selected_rows=[0]
    ),
    html.Br(),
    html.Hr(),

    #Chart and map
    html.Div(className='row', style={'display': 'flex'}, children=[
        html.Div(id='graph-id', className='col s12 m6'),
        html.Div(id='map-id', className='col s12 m6')
    ])
])

#Callbacks
@app.callback(
    Output('datatable-id','data'),
    [Input('filter-type', 'value')]
)
def update_dashboard(filter_type):

    if filter_type == 'Reset':
        records = db.read({})

    elif filter_type == 'Water Rescue':
        records = db.read({
            "animal_type": "Dog",
            "breed": {"$in": [
                "Labrador Retriever Mix",
                "Chesapeake Bay Retriever",
                "Newfoundland"
            ]}
        })

    elif filter_type == 'Mountain/Wilderness':
        records = db.read({
            "animal_type": "Dog",
            "breed": {"$in": [
                "German Shepherd",
                "Alaskan Malamute",
                "Old English Sheepdog",
                "Siberian Husky",
                "Rottweiler"
            ]}
        })

    elif filter_type == 'Disaster/Tracking':
        records = db.read({
            "animal_type": "Dog",
            "breed": {"$in": [
                "Doberman Pinscher",
                "German Shepherd",
                "Bloodhound",
                "Belgian Malinois"
            ]}
        })

    else:
        records = []

    df_filtered = pd.DataFrame.from_records(records)

    if '_id' in df_filtered.columns:
        df_filtered.drop(columns=['_id'], inplace=True)

    return df_filtered.to_dict('records')

@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data")]
)
def update_graphs(viewData):

    if not viewData:
        return []

    dff = pd.DataFrame.from_dict(viewData)
    fig = px.pie(dff, names='breed', title='Breed Distribution of Filtered Animals')
    return [dcc.Graph(figure=fig)]

@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):

    if not selected_columns:
        return[]

    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "selected_rows")]
)
def update_map(viewData, selected_rows):

    if not viewData or not selected_rows:
        return []

    dff = pd.DataFrame.from_dict(viewData)
    row = selected_rows[0]

    try:
        lat = float(dff.iloc[row]['latitude'])
        lon = float(dff.iloc[row]['longitude'])
    except Exception:
        lat = 30.75
        lon = -97.48

    breed = dff.iloc[row].get('breed', 'Unknown')
    name = dff.iloc[row].get('name', 'Unknown')

    return [
        dl.Map(
            style={'width': '1000px', 'height': '500px'},
            center=[lat, lon],
            zoom=10,
            children=[
                dl.TileLayer(id="base-layer-id"),
                dl.Marker(
                    position=[lat, lon],
                    children=[
                        dl.Tooltip(breed),
                        dl.Popup([html.H1("Animal Name"), html.P(name)])
                    ]
                )
            ]
        )
    ]

#Run server
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
