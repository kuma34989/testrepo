# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# create list of launch sites from spacex_df
sites = []
sites.append({'label':'All Sites', 'value':'ALL'}) # add 'All sites' option

sites_unique = spacex_df['Launch Site'].unique().tolist() # get name of all unique sites
for site in sites_unique:
    sites.append({'label': site, 'value': site}) # add those to the list

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.P("Launch site:"),
                                dcc.Dropdown(id='site-dropdown',
                                             options=sites,
                                             value='ALL',
                                             placeholder='Select a Launch Site here',
                                             searchable=True
                                             # style={'width':'80%','padding':'3px','font-size':'20px','text-align-last':'center'}
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                marks = {0: '0 kg', 1000: '1,000 kg', 2000: '2,000 kg', 3000: '3,000 kg', 4000: '4,000 kg', 5000: '5,000 kg', 
                                                        6000: ',6000 kg', 7000: '7,000 kg', 8000: '8,000 kg', 9000: '9,000 kg', 10000: '10,000 kg'},
                                                value=[min_payload, max_payload]
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(site_selected):
    filtered_df = spacex_df
    if site_selected == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Success Count for all launch sites')
    else:
        filtered_df=spacex_df[spacex_df['Launch Site'] == site_selected]
        filtered_df=filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class_freq')
        fig=px.pie(filtered_df,values='class_freq', names='class', title=f"Total Success Launches for site {site_selected}")
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
                [Input(component_id='site-dropdown',component_property='value'),
                Input(component_id='payload-slider',component_property='value')])
def scatter(site_selected, payload):
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0], payload[1])]
    
    if site_selected=='ALL':
        fig=px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Success count on Payload mass for all sites')
    else:
        fig=px.scatter(filtered_df[filtered_df['Launch Site'] == site_selected], x='Payload Mass (kg)', y='class', color='Booster Version Category', title=f"Success count on Payload mass for site {site_selected}")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
