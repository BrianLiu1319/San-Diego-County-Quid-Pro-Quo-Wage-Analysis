import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import os

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

county = 'Carlsbad'

# Load the CSV files
wages_path = os.path.join(BASE_DIR, f'{county}PoliceDepartmentWageData.csv')
contributions_path = os.path.join(BASE_DIR, f'{county}PoliceContributionsBinder.csv')

wages = pd.read_csv(wages_path)
contributions = pd.read_csv(contributions_path)

# Convert date columns to datetime
wages['Year'] = pd.to_datetime(wages['Year'], format='%Y')
contributions['DATE'] = pd.to_datetime(contributions['DATE'])

# Extract the year from the contributions date
contributions['Year'] = contributions['DATE'].dt.year

# Convert 'AMOUNT' to numeric, forcing errors to NaN and then filling NaN with 0
contributions['AMOUNT'] = pd.to_numeric(contributions['AMOUNT'].str.replace(',', ''), errors='coerce').fillna(0)

# Create a Dash application
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='position-dropdown',
        options=[{'label': pos, 'value': pos} for pos in wages['Position'].unique()],
        value=wages['Position'].unique()[0]
    ),
    dcc.Graph(id='salary-contribution-graph'),
    dcc.Store(id='clicked-points', data=[])
])

@app.callback(
    Output('salary-contribution-graph', 'figure'),
    [Input('position-dropdown', 'value'),
     Input('clicked-points', 'data')]
)
def update_graph(selected_position, clicked_points):
    fig = go.Figure()

    # Filter wage data for the selected position
    position_data = wages[wages['Position'] == selected_position]
    fig.add_trace(go.Scatter(
        x=position_data['Year'],
        y=position_data['MedianPositionSalary'],
        mode='lines',
        name=selected_position,
        line=dict(width=2),
        hovertemplate='%{x|%Y}: $%{y:.2f}<extra></extra>'
    ))

    # Merge wages and contributions data on the year
    merged_data = contributions.merge(position_data, left_on='Year', right_on=position_data['Year'].dt.year, how='inner')

    # Add contributions data as scatter points with tooltips
    fig.add_trace(go.Scatter(
        x=merged_data['DATE'],
        y=merged_data['MedianPositionSalary'],
        mode='markers',
        name='Contributions',
        marker=dict(size=10, color='red', symbol='circle'),
        text=merged_data.apply(lambda row: f"Date: {row['DATE'].strftime('%Y-%m-%d')}<br>"
                                           f"Candidate: {row['NAME OF CANDIDATE']}<br>"
                                           f"Office: {row['OFFICE SOUGHT OR HELD']}<br>"
                                           f"Support/Oppose: {row['SUPPORT OR OPPOSE']}<br>"
                                           f"Amount: ${row['AMOUNT']:.2f}<br>"
                                           f"Won/Lost: {row['WON OR LOST']}", axis=1),
        hoverinfo='text'
    ))

    # Add persistent text boxes for clicked points
    for point in clicked_points:
        fig.add_annotation(
            x=point['x'],
            y=point['y'],
            text=point['text'],
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            ax=0,
            ay=-40,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='black',
            borderwidth=1,
            font=dict(color='black', size=10)
        )

    fig.update_layout(
        title=f'Salary and Contributions for {selected_position}',
        xaxis_title='Year',
        yaxis_title='Median Salary',
        hovermode='closest'
    )

    return fig

@app.callback(
    Output('clicked-points', 'data'),
    Input('salary-contribution-graph', 'clickData'),
    State('clicked-points', 'data')
)
def store_click_data(clickData, clicked_points):
    if clickData is None:
        return clicked_points

    # Extract data from click event
    point = clickData['points'][0]
    new_point = {
        'x': point['x'],
        'y': point['y'],
        'text': point['text']
    }

    # Check if the point is already clicked
    if new_point in clicked_points:
        # Remove the point if it's already clicked
        clicked_points.remove(new_point)
    else:
        # Add new point to clicked points
        clicked_points.append(new_point)

    return clicked_points

if __name__ == '__main__':
    app.run_server(debug=True)
