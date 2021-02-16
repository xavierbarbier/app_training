import io
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import base64
import tensorflow as tf
import tensorflow_hub as hub
import os
import numpy as np

export_path_keras = "1613379473.h5"

reloaded = tf.keras.models.load_model(
  export_path_keras, 
  # `custom_objects` tells keras how to load a `hub.KerasLayer`
  custom_objects={'KerasLayer': hub.KerasLayer})

class_names_clean = np.load("class_names_clean.npy")

IMAGE_RES = 224

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    html.Div(id='output-image-upload'),
])


@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'))
def update_output(contents):
    if contents is not None:
      img = str(contents)
      encoded_image = str(contents).split(",")[1]
      decoded_image = base64.b64decode(encoded_image)
      image = tf.io.decode_image(decoded_image, channels=3, dtype=tf.dtypes.uint8, expand_animations=False)
      image = tf.image.resize(image, [IMAGE_RES,IMAGE_RES] )/255.0
      input_arr = keras.preprocessing.image.img_to_array(image)
      input_arr = np.array([input_arr])
      predictions = reloaded.predict(input_arr)
      predicted_ids = np.argmax(predictions, axis=-1)
      predicted_class_names = class_names_clean[predicted_ids]
      return html.Div([        
        html.Img(src=img, width=255),
        html.Hr(),
        html.Div('Prediction'),
        html.Pre(predicted_class_names, style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
