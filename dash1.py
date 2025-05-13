import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objs as go
import plotly.express as px

# Load the dataset
file_path = r'C:\Users\91988\Downloads\bengaluru_house_prices.csv'  # Raw string path to CSV file
df1 = pd.read_csv(file_path)
df = df1.head()

# Initialize the Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 'padding': '20px', 'backgroundColor': 'skyblue'},
    children=[
        # Marquee Tag for your name at the top
        html.Div(
            children=[
                html.Marquee(
                    children=[
                        "Welcome to the Visualization Dashboard - Created by RAVINDRA!"
                    ],
                    style={'fontSize': '30px', 'color': 'black', 'fontWeight': 'bold', 'backgroundColor': 'orange'}
                )
            ],
            style={'textAlign': 'center', 'marginBottom': '20px'}
        ),
        # Heading for the page
        html.H1(
            'Visualization from CSV Data',
            style={
                'color': 'brown',
                'textAlign': 'center',
                'fontSize': '36px',
                'textTransform': 'uppercase',
                'fontWeight': 'bold',
                'fontFamily': 'Verdana, sans-serif'
            }
        ),
        html.P(
            'Choose Your Visualization! Select the Graph Type and the Columns for plotting from the dropdowns below and watch the magic happen!.',
            style={
                'color': '#2c3e50',
                'fontSize': '18px',
                'fontFamily': 'Georgia, serif',
                'textAlign': 'center',
                'lineHeight': '1.6'
            }
        ),
        # Dropdown for chart type
        html.Div(
            style={'marginTop': '50px', 'padding': '50px', 'backgroundColor': '#F5F5DC', 'borderRadius': '20px'},
            children=[
                html.Label('SELECT THE CHART THAT WILL GET DISPLAYED:', style={'fontSize': '20px', 'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='chart-dropdown',
                    options=[
                        {'label': 'Line Chart', 'value': 'line'},
                        {'label': 'Bar Chart', 'value': 'bar'},
                        {'label': 'Scatter Plot', 'value': 'scatter'},
                        {'label': 'Box Plot', 'value': 'boxplot'},
                        {'label': 'Histogram', 'value': 'histogram'},
                        {'label': 'Heatmap', 'value': 'heatmap'},
                        {'label': 'Pie Chart', 'value': 'piechart'}
                    ],
                    placeholder='Select chart here',
                    style={'fontSize': '18px', 'color': '#2c3e50'}
                )
            ]
        ),
        # Dropdowns for X and Y columns
        html.Div(
            style={'marginTop': '20px', 'padding': '10px', 'backgroundColor': '#F5F5DC', 'borderRadius': '20px'},
            children=[
                html.Label('Select X-axis:', style={'fontSize': '18px', 'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='x-column-dropdown',
                    options=[{'label': col, 'value': col} for col in df.columns],
                    placeholder='Select X-axis column',
                    style={'fontSize': '18px', 'color': '#2c3e50'}
                ),
                html.Label('Select Y-axis:', style={'fontSize': '18px', 'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='y-column-dropdown',
                    options=[{'label': col, 'value': col} for col in df.columns],
                    placeholder='Select Y-axis column',
                    style={'fontSize': '18px', 'color': '#2c3e50'}
                )
            ]
        ),
        # Graph component to display the selected chart
        html.Div(
            style={'marginTop': '20px', 'padding': '10px', 'border': '1px solid #d1d1d1', 'borderRadius': '20px'},
            children=[
                dcc.Graph(id='chart-graph')
            ]
        )
    ]
)

# Callback to update the graph based on dropdown selection
@app.callback(
    Output('chart-graph', 'figure'),
    [Input('chart-dropdown', 'value'),
     Input('x-column-dropdown', 'value'),
     Input('y-column-dropdown', 'value')]
)
def update_graph(chart_type, x_column, y_column):
    if not x_column or not y_column:
        return go.Figure()  # Empty figure if no columns are selected

    # Create the appropriate chart
    if chart_type == 'line':
        figure = go.Figure(data=[go.Scatter(x=df[x_column], y=df[y_column], mode='lines', name='Line Chart')])
        figure.update_layout(title='Line Chart', xaxis_title=x_column, yaxis_title=y_column)
    elif chart_type == 'bar':
        figure = go.Figure(data=[go.Bar(x=df[x_column], y=df[y_column], name='Bar Chart')])
        figure.update_layout(title='Bar Chart', xaxis_title=x_column, yaxis_title=y_column)
    elif chart_type == 'scatter':
        figure = go.Figure(data=[go.Scatter(x=df[x_column], y=df[y_column], mode='markers', name='Scatter Plot')])
        figure.update_layout(title='Scatter Plot', xaxis_title=x_column, yaxis_title=y_column)
    elif chart_type == 'boxplot':
        figure = go.Figure(data=[go.Box(x=df[x_column], y=df[y_column], name='Box Plot')])
        figure.update_layout(title="Box Plot", xaxis_title=x_column, yaxis_title=y_column)
    elif chart_type == 'histogram':
        figure = go.Figure(data=[go.Histogram(x=df[x_column], name='Histogram')])
        figure.update_layout(title="Histogram", xaxis_title=x_column)
    elif chart_type == 'heatmap':
        # Create a heatmap using plotly express (requires numeric data for heatmaps)
        heatmap_data = df.corr()  # Compute the correlation matrix for the heatmap
        figure = px.imshow(heatmap_data, text_auto=True)
        figure.update_layout(title="Heatmap")
    elif chart_type == 'piechart':
        # Create a Pie chart (using value counts for the X-column)
        pie_data = df[x_column].value_counts().reset_index()
        pie_data.columns = [x_column, 'count']
        figure = px.pie(pie_data, names=x_column, values='count')
        figure.update_layout(title="Pie Chart")
    else:
        figure = go.Figure()  # Empty figure if no chart type is selected

    return figure

# Run the app
app.run_server(port=8052, debug=True, use_reloader=False)  # Change the port if needed