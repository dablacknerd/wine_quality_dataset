import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Output,Input

# Load file
df1 = pd.read_csv('data/clean-winequality-red.csv')
df2 = pd.read_csv('data/vif-clean-winequality-red.csv')

features_drop_down = dcc.Dropdown(
          id ='wine-features',
          options = [dict(label=i.title(),value=i) for i in df1.columns],
          value = 'volatile acidity'
)

graph1 = dcc.Graph(id='outlier-free-red-wine-graph')
graph2 = dcc.Graph(id='with-outlier-red-wine-graph')
cb_input = Input(component_id='wine-features',component_property='value')
cb_output1 = Output(component_id='outlier-free-red-wine-graph',component_property='figure')
cb_output2 = Output(component_id='with-outlier-red-wine-graph',component_property='figure')

app = dash.Dash()

app.layout = html.Div([
    html.Div([features_drop_down],style=dict(width='50%',display='inline-block')),
    html.Div([
              html.Div([graph1],style=dict(width='48%',display='inline-block')),
              html.Div([graph2],style=dict(width='48%',display='inline-block')),
             ])
])

@app.callback(cb_output1,[cb_input])
def build_graph_1(wine_feature):
    x_values = df1['quality'].values
    y_values = df1[wine_feature].values

    sct_data = go.Scatter(x=x_values, y=y_values, mode='markers',marker=dict(color='#3335FF'))
    sct_title = 'Red Wine: Quality vs {} (Without Outliers)'.format(wine_feature.title())
    sct_layout = go.Layout(title = sct_title,
                       xaxis = dict(title='Quality'),
                       yaxis = dict(title=wine_feature.title()),
                       hovermode = 'closest')
    return dict(data=[sct_data],layout=sct_layout)

@app.callback(cb_output2,[cb_input])
def build_graph_2(wine_feature):
    x_values = df2['quality'].values
    y_values = df2[wine_feature].values

    sct_data = go.Scatter(x=x_values, y=y_values, mode='markers',marker=dict(color='#C0392B'))
    sct_title = 'Red Wine: Quality vs {} (With Outliers Present)'.format(wine_feature.title())
    sct_layout = go.Layout(title = sct_title,
                       xaxis = dict(title='Quality'),
                       yaxis = dict(title=wine_feature.title()),
                       hovermode = 'closest')
    return dict(data=[sct_data],layout=sct_layout)

if __name__=='__main__':
    app.run_server()
