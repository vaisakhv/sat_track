import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque
import datetime
import time

from pyorbital.orbital import Orbital
satellite = Orbital('AQUA')

X = []
Y = []
X.append(time.strftime("%H:%M:%S"))
lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
Y.append(alt)
initial_trace = go.Scatter(
    x=list(X),
    y=list(Y),
    name='Scatter',
    mode='lines+markers'
)

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph',
                  animate=False,
                  figure={'data': [initial_trace]
                          }),
        dcc.Interval(
            id='graph-update',
            interval=1*1000
        ),
    ]
)


@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(n):
    import time
    lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())

    X.append(time.strftime("%H:%M:%S"))
    Y.append(alt)

    trace = go.Scatter(
        x=X,
        y=Y,
        name='Scatter',
        mode='lines'
    )

    return {'data': [trace]
    }


if __name__ == '__main__':
    app.run_server(debug=True)
