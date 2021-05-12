import geopandas as gpd
import pandas as pd
import json

from core import *

from bokeh.io import output_notebook, show, output_file, curdoc
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, HoverTool, Slider
from bokeh.layouts import widgetbox, row, column
from bokeh.palettes import brewer



def get_data(country='France'):
    file_save = open(DATA_PATH + '/analysis/save-dict.json', 'r')
    data = json.load(file_save)
    file_save.close()

    print(data[country])

# get_data()
def geo_dataframe_reformat():
    shapefile = DATA_PATH +  '/datasets/countries_110m/ne_110m_admin_0_countries.shp'

    # geopandas data
    gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
    gdf.columns = ['country', 'country_code', 'geometry']

    file = open(DATA_PATH + '/analysis/correspondence-dict.json', 'r')
    correspondence_dict = json.load(file)
    file.close()

    countries_reformated = []
    for country in list(gdf['country']):
        # countries_reformated.append(get_country(country, correspondence_dict)[0])
        countries_reformated.append(get_country_from_api(country))

        print(country + ' -> ' + str(countries_reformated[len(countries_reformated) - 1]))

    gdf['country_reformated'] = countries_reformated
    # [get_country(country, correspondence_dict)[0] for country in list(gdf['country'])]

    gdf.to_csv(shapefile[:-3] + 'csv')

    print(list(gdf['country_reformated']))
    print(gdf)

def geo_dataframe(country='France'):
    shapefile = DATA_PATH +  '/datasets/countries_110m/ne_110m_admin_0_countries.shp'
    csvfile = DATA_PATH +  '/datasets/countries_110m/ne_110m_admin_0_countries.csv'

    # geo data
    gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
    gdf.columns = ['country', 'country_code', 'geometry']

    # add reformated countries
    df_countries = pd.read_csv(csvfile, sep=';')
    merged = gdf.merge(df_countries, left_on = 'country', right_on = 'country', how = 'left')

    # add countries data
    file_save = open(DATA_PATH + '/analysis/save-dict.json', 'r')
    data = json.load(file_save)
    file_save.close()
    # print(data)
    df = pd.DataFrame(data[country].items(), columns=['entity', 'value'])
    print(df)
    merged = merged.merge(df, left_on = 'country_reformated', right_on = 'entity', how = 'left')
    merged = merged.fillna('No Data')

    return merged


def map(country='France'):

    merged = geo_dataframe(country)

    #Read data to json
    merged_json = json.loads(merged.to_json())
    #Convert to str like object
    json_data = json.dumps(merged_json)

    #Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson = json_data)

    #Define a sequential multi-hue color palette.
    palette = brewer['YlGnBu'][8]
    #Reverse color order so that dark blue is highest obesity.
    palette = palette[::-1]
    #Instantiate LinearColorMapper that linearly maps numbers in a range,
    #into a sequence of colors. Input nan_color.
    color_mapper = LinearColorMapper(palette=palette,
                                     low=0, high=400,
                                     nan_color='#d9d9d9')

    #Define custom tick labels for color bar.
    # tick_labels = {'0': '0%', '5': '5%',
    #                '10':'10%', '15':'15%',
    #                '20':'20%', '25':'25%',
    #                '30':'30%','35':'35%',
    #                '40': '>40%'}
    # tick_labels = {'0': '<40', '40': '>40'}

    #Add hover tool
    hover = HoverTool(tooltips = [('Country/region', '@country') ,('value', '@value')])

    #Create color bar.
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=2,
                         width=500, height=20,
                         border_line_color=None, location=(0,0),
                         orientation='horizontal') #,
                         #major_label_overrides=tick_labels)


    #Create figure object.
    p = figure(title = 'Pays évoqués dans les Cablegate originaires de ' + country,
               plot_height = 600 , plot_width = 950,
               toolbar_location = None, tools = [hover])

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    p.title.text_font_size = '20pt'

    #Add patch renderer to figure.
    p.patches('xs', 'ys', source = geosource,
              fill_color = {'field' :'value', 'transform' : color_mapper},
              line_color = 'black', line_width = 0.25, fill_alpha = 1)


    p.add_layout(color_bar, 'below')

    # Define the callback function: update_plot
    # def update_plot(attr, old, new):
    #     yr = slider.value
    #     new_data = json_data(yr)
    #     geosource.geojson = new_data
    #     p.title.text = 'Share of adults who are obese, %d' %yr

    # Make a slider object: slider
    # slider = Slider(title = 'Year',
    #                 start = 1975, end = 2016,
    #                 step = 1, value=2016)
    # slider.on_change('value', update_plot)

    # Make a column layout of widgetbox(slider) and plot, and add it to the current document
    layout = column(p) #,widgetbox(slider))
    curdoc().add_root(layout)

    #Display plot
    show(layout)

def json_to_dict(path):
    file_save = open(path, 'r')
    data = json.load(file_save)
    file_save.close()
    return data

# map('Libya')
# map('France')
# map('Spain')
map('India')
