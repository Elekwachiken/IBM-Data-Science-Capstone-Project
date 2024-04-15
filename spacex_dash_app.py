# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Launch Sites Dropdown options
unique_launch_sites = spacex_df['Launch Site'].unique().tolist()
launch_sites = []
launch_sites.append({'label': 'All Sites', 'value': 'All Sites'})
for launch_site in unique_launch_sites:
    launch_sites.append({'label': launch_site, 'value': launch_site})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.Div([
        html.H1('SpaceX Launch Records Dashboard', 
                style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        html.Div([
            dcc.Dropdown(
                id = 'site-dropdown',
                options = launch_sites,
                placeholder = 'Select a Launch Site here',
                searchable = True ,
                clearable = False,
                value = 'All Sites'
                ),
            html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart')),
        ], style={'padding': '0 30px'}),
        html.Br(),

        html.Div([
            html.Div("Payload range (Kg):", 
                     style={'color': '#503D36','font-size': 20, 'padding': '0 30px', 'margin-left': '11px'}
                     ),
        # TASK 3: Add a slider to select payload range
        html.Div([
            dcc.RangeSlider(
                id = 'payload_slider',
                min = 0,
                max = 10000,
                step = 1000,
                marks = {
                    0: {'label': '0 Kg', 'style': {'color': '#77b0b1'}},
                    1000: {'label': '1000 Kg'},
                    2000: {'label': '2000 Kg'},
                    3000: {'label': '3000 Kg'},
                    4000: {'label': '4000 Kg'},
                    5000: {'label': '5000 Kg'},
                    6000: {'label': '6000 Kg'},
                    7000: {'label': '7000 Kg'},
                    8000: {'label': '8000 Kg'},
                    9000: {'label': '9000 Kg'},
                    10000: {'label': '10000 Kg', 'style': {'color': '#f50'}},
                    }, 
                value = [min_payload,max_payload]
                ), 
            ], style={'padding': '40px 30px'}),

        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
        ]),
        ],style={'padding': '0 20px'})
    ])
                

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id = 'success-pie-chart', component_property = 'figure'),
    [Input(component_id = 'site-dropdown', component_property = 'value')]
    )
def update_piegraph(site_dropdown):
    if (site_dropdown == 'All Sites' or site_dropdown == 'None'):
        all_sites  = spacex_df[spacex_df['class'] == 1] # All Success only for all sites.
        fig = px.pie(
                all_sites,
                names = 'Launch Site',
                title = 'Total Success Launches by All Sites',
                hole = .2,
                color_discrete_sequence = px.colors.sequential.RdBu
            )
    else:
        site_specific  = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        fig = px.pie(
                site_specific,
                names = 'class',
                title = 'Total Success Launches for Site &#8608; '+site_dropdown,
                hole = .2
            )
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'), 
    [Input(component_id = 'site-dropdown', component_property = 'value'), 
     Input(component_id = "payload_slider", component_property = "value")]
    )
def update_scattergraph(site_dropdown,payload_slider):
    if (site_dropdown == 'All Sites' or site_dropdown == 'None'):
        low, high = payload_slider
        all_sites  = spacex_df
        inrange = (all_sites['Payload Mass (kg)'] > low) & (all_sites['Payload Mass (kg)'] < high)
        fig = px.scatter(
                all_sites[inrange], 
                x = "Payload Mass (kg)", 
                y = "class",
                title = 'Correlation Between Payload and Success for All Sites',
                color="Booster Version Category",
                size='Payload Mass (kg)',
                hover_data=['Payload Mass (kg)']
            )
    else:
        low, high = payload_slider
        site_specific  = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        inrange = (site_specific['Payload Mass (kg)'] > low) & (site_specific['Payload Mass (kg)'] < high)
        fig = px.scatter(
                site_specific[inrange],
                x = "Payload Mass (kg)",
                y = "class",
                title = 'Correlation Between Payload and Success for Site &#8608; '+site_dropdown,
                color="Booster Version Category",
                size='Payload Mass (kg)',
                hover_data=['Payload Mass (kg)']
            )
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
