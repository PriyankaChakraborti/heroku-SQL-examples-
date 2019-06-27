from flask import Flask, render_template, request
import pandas as pd
from bokeh.embed import components
from bokeh.plotting import figure
import numpy as np

app = Flask(__name__)

# Load the Iris Data Set
iris_df = pd.read_csv("https://raw.githubusercontent.com/ecerami/pydata-essentials/master/bokeh_flask/data/iris.data", 
                      names=["Sepal Length", "Sepal Width", "Petal Length", "Petal Width", "Species"])
feature_names = iris_df.columns[0:-1].values.tolist()

# Create dataframe for each separate species
iris_setosa_df = pd.DataFrame(iris_df.loc[iris_df.Species=='Iris-setosa'])
iris_versicolor_df = pd.DataFrame(iris_df.loc[iris_df.Species=='Iris-versicolor'])
iris_virginica_df = pd.DataFrame(iris_df.loc[iris_df.Species=='Iris-virginica'])

def generate_plot_data(data, density=True, bins=10):
    data = np.asarray(data)
    hist, edges = np.histogram(data, density=density, bins=bins)
    return pd.DataFrame({'top': hist,'left': edges[:-1],'right': edges[1:]})

# Create the main plot
def create_figure(current_feature_name, bins):
    
    iris_setosa_df['frequency']=iris_setosa_df.groupby(current_feature_name)[current_feature_name].transform('count')
    iris_versicolor_df['frequency']=iris_versicolor_df.groupby(current_feature_name)[current_feature_name].transform('count')
    iris_virginica_df['frequency']=iris_virginica_df.groupby(current_feature_name)[current_feature_name].transform('count')

    p = figure()

    plot_data = generate_plot_data(iris_setosa_df['frequency'].values, density=False, bins=bins)
    p.quad(bottom=0, top=plot_data['top'],
           left=plot_data['left'], right=plot_data['right'],
           fill_color='blue', line_color='blue', fill_alpha=0.3,line_alpha=0.3,legend='Iris Setosa' )
    
    plot_data = generate_plot_data(iris_versicolor_df['frequency'].values, density=False, bins=bins)
    p.quad(bottom=0, top=plot_data['top'],
           left=plot_data['left'], right=plot_data['right'],
           fill_color='red', line_color='blue', fill_alpha=0.3,line_alpha=0.3,legend='Iris Versicolor' )
    
    plot_data = generate_plot_data(iris_virginica_df['frequency'].values, density=False, bins=bins)
    p.quad(bottom=0, top=plot_data['top'],
           left=plot_data['left'], right=plot_data['right'],
           fill_color='green', line_color='blue', fill_alpha=0.3,line_alpha=0.3,legend='Iris Virginica' )
    
    p.title.text ='Distribution for chosen feature'
    p.xaxis.axis_label = 'Chosen Length'
    p.yaxis.axis_label = 'Count'
    
    return p

# Index page
@app.route('/')
def index():
	# Determine the selected feature
    current_feature_name = request.args.get("feature_name")
    if current_feature_name == None:
        current_feature_name = "Sepal Length"
        
    # Determine the number of bins
    bins = request.args.get("bins")
    if bins == "" or bins == None:
        bins = 10
    else:
        bins = int(bins)
    plot = create_figure(current_feature_name, bins)
    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    return render_template("iris_index.html", script=script, div=div,
                           bins = bins, feature_names=feature_names, 
                           current_feature_name=current_feature_name)

# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
    app.run(port=33507)