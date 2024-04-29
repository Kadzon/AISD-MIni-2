# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
from dash import Dash, dcc, html, Input, Output, State
from dash import Dash, dash_table

from io import StringIO

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

col_style = {'display':'grid', 'grid-auto-flow': 'row'}
row_style = {'display':'grid', 'grid-auto-flow': 'column'}

import plotly.express as px
import pandas as pd

import requests

app = Dash(__name__)

df = pd.read_csv("iris_extended_encoded.csv",sep=',')
df_csv = df.to_csv(index=False)


base_url =  "http://127.0.0.1:5000/iris" 

app.layout = html.Div(children=[
    html.H1(children='Iris classifier'),
    dcc.Tabs([
    dcc.Tab(label="Explore Iris training data", style=tab_style, selected_style=tab_selected_style, children=[

    html.Div([
        html.Div([
            html.Label(['File name to Load for training or testing'], style={'font-weight': 'bold'}),
            dcc.Input(id='file-for-train', type='text', style={'width':'100px'}),
            html.Div([
                html.Button('Load', id='load-val', style={"width":"60px", "height":"30px"}),
                html.Div(id='load-response', children='Click to load')
            ], style=col_style)
        ], style=col_style),

        html.Div([
            html.Button('Upload', id='upload-val', style={"width":"60px", "height":"30px"}),
            html.Div(id='upload-response', children='Click to upload')
        ], style=col_style| {'margin-top':'20px'})

    ], style=col_style | {'margin-top':'50px', 'margin-bottom':'50px', 'width':"400px", 'border': '2px solid black'}),


html.Div([
    html.Div([
        html.Div([
            html.Label(['Feature'], style={'font-weight': 'bold'}),
            dcc.Dropdown(
                df.columns, #['a','b','c'], #<dropdown values for histogram>
                df.columns[0] ,#'a',           #<default value for dropdown>
                id='hist-column'
            )
            ], style=col_style ),
        dcc.Graph( id='selected_hist' )
    ], style=col_style | {'height':'400px', 'width':'400px'}),

    html.Div([

    html.Div([

    html.Div([
        html.Label(['X-Axis'], style={'font-weight': 'bold'}),
        dcc.Dropdown(
            df.columns, 
            df.columns[0] ,
            id='xaxis-column'
            )
        ]),

    html.Div([
        html.Label(['Y-Axis'], style={'font-weight': 'bold'}),
        dcc.Dropdown(
            df.columns, 
            df.columns[0] ,
            id='yaxis-column'
            )
        ])
    ], style=row_style | {'margin-left':'50px', 'margin-right': '50px'}),

    dcc.Graph(id='indicator-graphic')
    ], style=col_style)
], style=row_style),

    html.Div(id='tablecontainer', children=[
        dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], page_size=15,
            id='datatable' )
        ])
    ]),
    dcc.Tab(label="Build model and perform training", id="train-tab", style=tab_style, selected_style=tab_selected_style, children=[
        html.Div([
            html.Div([
                html.Label(['Enter a dataset ID to use in training'], style={'font-weight': 'bold'}),
                html.Div(dcc.Input(id='dataset-for-train', type='text'))
            ], style=col_style | {'margin-top':'20px'}),
            
            html.Div([
                html.Button('New model', id='build-val', style={'width':'90px', "height":"30px"}),
                html.Div(id='build-response', children='Click to build new model and train')
            ], style=col_style | {'margin-top':'20px'}),
            
            html.Div([
                html.Label(['Enter a model ID for re-training'], style={'font-weight': 'bold'}),
                html.Div(dcc.Input(id='model-for-train', type='text'))
            ], style=col_style | {'margin-top':'20px'}),

            html.Div([
                html.Button('Re-Train', id='train-val', style={"width":"90px", "height":"30px"})
            ], style=col_style | {'margin-top':'20px', 'width':'90px'})

        ], style=col_style | {'margin-top':'50px', 'margin-bottom':'50px', 'width':"400px", 'border': '2px solid black'}),

        html.Div(id='container-button-train', children='')
    ]),
    dcc.Tab(label="Score model", id="score-tab", style=tab_style, selected_style=tab_selected_style, children=[
        html.Div([
            html.Div([
                html.Label(['Enter a row text (CSV) to use in scoring'], style={'font-weight': 'bold'}),
                html.Div(dcc.Input(id='row-for-score', type='text', style={'width':'300px'}))
            ], style=col_style | {'margin-top':'20px'}),
            html.Div([
                html.Label(['Enter a model ID for scoring'], style={'font-weight': 'bold'}),
                html.Div(dcc.Input(id='model-for-score', type='text'))
            ], style=col_style | {'margin-top':'20px'}),            
            html.Div([
                html.Button('Score', id='score-val', style={'width':'90px', "height":"30px"}),
                html.Div(id='score-response', children='Click to score')
            ], style=col_style | {'margin-top':'20px'})
        ], style=col_style | {'margin-top':'50px', 'margin-bottom':'50px', 'width':"400px", 'border': '2px solid black'}),
        
        html.Div(id='container-button-score', children='')
    ]),

    dcc.Tab(label="Test Iris data", style=tab_style, selected_style=tab_selected_style, children=[
        html.Div([
            html.Div([
                html.Label(['Enter a dataset ID to use in testing'], style={'font-weight': 'bold'}),
                html.Div(dcc.Input(id='dataset-for-test', type='text'))
            ], style=col_style | {'margin-top':'20px'}),
            html.Div([
                html.Label(['Enter a model ID to use in testing'], style={'font-weight': 'bold'}),
                html.Div(dcc.Input(id='model-for-test', type='text'))
            ], style=col_style | {'margin-top':'20px'}),

            html.Div([
                html.Button('Test', id='test-val'),
            ], style=col_style | {'margin-top':'20px', 'width':'90px'})

        ], style=col_style | {'margin-top':'50px', 'margin-bottom':'50px', 'width':"400px", 'border': '2px solid black'}),

        html.Div(id='container-button-test', children='')
    ])

    ])
])

#explore iris dataset
# callbacks for Explore data tab
@app.callback(
    Output(component_id='load-response', component_property='children'),
    Input(component_id='file-for-train', component_property='value'),
    Input(component_id='load-val', component_property='n_clicks')
)
def update_output_load(filename, n_clicks):
    global df, df_csv

    print("Data loaded from file: ", filename, "and the number of clicks: ", n_clicks)
    if n_clicks is None:
        return 'Click to load'

    if filename is not None and n_clicks is not None:
        df = pd.read_csv(filename, sep=',')
        df_csv = df.to_csv(index=False)

        return 'Load done.'
    else:
        return ''


@app.callback(
    Output(component_id='upload-response', component_property='children'),
    Input(component_id='upload-val', component_property='n_clicks')
)
def update_output_upload(n_clicks):
    global df_csv
    print("Uploaded data with :", n_clicks, "number of clicks")

    if n_clicks is None:
        return 'Click to upload'

    if n_clicks is not None:
        url = f"{base_url}/dataset"
        files = {'train': df_csv}
        response = requests.post(url, files=files)

        return f'Uploaded dataset ID: {response.text}'
    else:
        return ''


#build model and perform training tab
@app.callback(
    Output(component_id="build-response", component_property="children"),
    Input(component_id="dataset-for-train", component_property="value"),
    Input(component_id="build-val", component_property="n_clicks")
)
def update_output_build(dataset_id, n_clicks):
    print("Building model, dataset ID:", dataset_id, "with number clicks", n_clicks)
    if n_clicks is None:
        return 'Click to build new model and train'

    if dataset_id is not None and n_clicks is not None:
        # invoke new model endpoint to build and train model given data set ID
        url = f"{base_url}/model"
        data = {'dataset': dataset_id}
        response = requests.post(url, data=data)
        # return the model ID
        return f'New model ID: {response.text}'
    else:
        return ''


@app.callback(
    Output(component_id="indicator-graphic", component_property="figure"),
    Input(component_id="xaxis-column", component_property="value"),
    Input(component_id="yaxis-column", component_property="value")
)
def update_graph(xaxis_column_name, yaxis_column_name):
    print("Updating graph with X-axis: ", xaxis_column_name, "Y-axis: ", yaxis_column_name)
    fig = px.scatter(x=df.loc[:, xaxis_column_name].values,
                     y=df.loc[:, yaxis_column_name].values)

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    fig.update_xaxes(title=xaxis_column_name)
    fig.update_yaxes(title=yaxis_column_name)

    return fig


@app.callback(
    Output(component_id='selected_hist', component_property='figure'),
    Input(component_id='hist-column', component_property='value')
)
def update_hist(column_name):
    print("Updating histogram column: ", column_name)
    fig = px.histogram(df, x=column_name)

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    fig.update_xaxes(title=column_name)

    return fig


@app.callback(
    Output(component_id='tablecontainer', component_property='children'),
    Input(component_id='load-val', component_property='n_clicks')
)
def update_table(n_clicks):
    print("Update table with this number of clicks: ", n_clicks)
    return dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], page_size=15,
                                id='datatable')


# callbacks for Training tab
@app.callback(
    Output(component_id='container-button-train', component_property='children'),
    Input(component_id="model-for-train", component_property="value"),
    Input(component_id="dataset-for-train", component_property="value"),
    Input(component_id="train-val", component_property="n_clicks")
)
def update_output_train(model_id, dataset_id, n_clicks):
    print("Train with model ID: ", model_id, "; dataset ID: ", dataset_id, "; n_clicks: ", n_clicks)
    if n_clicks is not None and model_id is not None and dataset_id is not None:
        # add API endpoint request here
        url = f"{base_url}/model/{model_id}"
        data = {'dataset': dataset_id}
        response = requests.put(url, params=data)

        train_df = pd.read_json(StringIO(response.text))
        train_fig = px.line(train_df)

        return dcc.Graph(figure=train_fig)
    else:
        return ""


# callbacks for Scoring tab
@app.callback(
    Output(component_id='container-button-score', component_property='children'),
    Input(component_id="model-for-score", component_property="value"),
    Input(component_id="row-for-score", component_property="value"),
    Input(component_id="score-val", component_property="n_clicks")
)
def update_output_score(model_id, fields, n_clicks):
    print("score model ID:", model_id, "; fields: ", fields, "; n_clicks: ",n_clicks)
    if n_clicks is not None and model_id is not None and fields is not None:
        # add API endpoint request for scoring here with constructed input row
        url = f"{base_url}/model/{model_id}"
        data = {'fields': fields}
        response = requests.get(url, params=data)
        return response.text

    else:
        return ""


# callbacks for Testing tab
@app.callback(
    Output(component_id='container-button-test', component_property='children'),
    Input(component_id="model-for-test", component_property="value"),
    Input(component_id="dataset-for-test", component_property="value"),
    Input(component_id="test-val", component_property="n_clicks")
)
def update_output_test(model_id, dataset_id, n_clicks):
    print("Testing model ID: ", model_id, "; dataset ID: ", dataset_id, "; n_clicks: ", n_clicks)
    if n_clicks is not None and model_id is not None and dataset_id is not None:
        # add API endpoint request for testing with given dataset ID
        url = f"{base_url}/model/{model_id}/test"
        data = {'dataset': ','.join(map(str, dataset_id))}
        response = requests.get(url, params=data)
        test_df = pd.read_json(StringIO(response.text))
        test_df = test_df.drop(columns=['Confusion Matrix'])
        test_fig = px.line(test_df)

        return dcc.Graph(figure=test_fig)
    else:
        return ""
#### ends here


'''  STARTING OF MULTI_LINE COMMENT FIELD...move code below above triple quotes to fill in and run

def update_output_load(<add function var mappings here>):
    global df, df_csv

    if nclicks != None:
        # load local data given input filename
        
        return 'Load done.'
    else:
        return ''


@app.callback(
# callback annotations go here
)
def update_output_build(<add function var mappings here>):
    print (nclicks)
    if nclicks != None:
        # invoke new model endpoint to build and train model given data set ID
        
        # return the model ID 
        return 'the model ID'
    else:
        return ''

@app.callback(
# callback annotations go here
)
def update_output_upload(<add function var mappings here>):
    global df_csv

    if nclicks != None:
        # invoke the upload API endpoint

        # return the dataset ID generated
        return 'return the dataset ID'
    else:
        return ''

@app.callback(
# callback annotations go here
)
def update_graph(<add function var mappings here>):

    fig = px.scatter(x=df.loc[:,<x-axis-var-name>].values,
                     y=df.loc[:,<y-axis-var-name>].values)

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    fig.update_xaxes(title=xaxis_column_name)
    fig.update_yaxes(title=yaxis_column_name)

    return fig


@app.callback(
# callback annotations go here
)
def update_hist(<add function var mappings here>):

    fig = px.histogram(df, x=<hist col var name here>)

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    fig.update_xaxes(title=hist_column_name)

    return fig

@app.callback(
# callback annotations go here
)
def update_table(<add function var mappings here>):
    return dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], page_size=15,
        id='datatable' )


# callbacks for Training tab

@app.callback(
# callback annotations go here
)
def update_output_train(<add function var mappings here>):
    if nclicks != None:
        # add API endpoint request here

        train_df = pd.read_json( r.text )
        train_fig = px.line(train_df)

        return dcc.Graph( figure=train_fig )
    else:
        return ""

# callbacks for Scoring tab

@app.callback(
# callback annotations go here
)
def update_output_score(<add function var mappings here>):
    if nclicks != None:
        # add API endpoint request for scoring here with constructed input row

        score_result = <read from return result object>
        
        return score_result
    else:
        return ""
    

# callbacks for Testing tab

@app.callback(
# callback annotations go here
)
def update_output_test(<add function var mappings here>):
    if nclicks != None:
        # add API endpoint request for testing with given dataset ID

        test_df = pd.read_json( r.text )
        test_fig = px.line(test_df)

        return dcc.Graph( figure=test_fig )
    else:
        return ""

'''


if __name__ == '__main__':
    app.run_server(debug=True)
