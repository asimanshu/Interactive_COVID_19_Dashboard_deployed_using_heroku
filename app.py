#!/usr/bin/env python
# coding: utf-8

# In[1]:

import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly


# In[2]:


import pandas as pd
import numpy as np
from datetime import datetime

import plotly.graph_objects as go
import plotly.express as px

from scipy.interpolate import interp1d


# In[3]:


app = dash.Dash(__name__)


# In[4]:


death_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
confirmed_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
recovered_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
country_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')


# In[5]:


death_df.drop('Province/State', axis=1, inplace=True)
confirmed_df.drop('Province/State', axis=1, inplace=True)
recovered_df.drop('Province/State', axis=1, inplace=True)
country_df.drop(['People_Tested', 'People_Hospitalized'], axis=1, inplace=True)


# In[6]:


# change columns name

death_df.rename(columns={'Country/Region': 'Country'}, inplace=True)
confirmed_df.rename(columns={'Country/Region': 'Country'}, inplace=True)
recovered_df.rename(columns={'Country/Region': 'Country'}, inplace=True)
country_df.rename(columns={'Country_Region': 'Country', 'Long_': 'Long'}, inplace=True)


# In[7]:


# sorting country_df with highest confirm case

country_df.sort_values('Confirmed', ascending=False, inplace=True)


# In[8]:


# fixing the size of circle to plot in the map

margin = country_df['Confirmed'].values.tolist()
circel_range = interp1d([1, max(margin)], [0.2,12])
circle_radius = circel_range(margin)


# In[9]:


# ploting world map
# fixing the size of circle

margin = country_df['Confirmed'].values.tolist()
circel_range = interp1d([1, max(margin)], [0.2,12])
circle_radius = circel_range(margin)


# ## NavBar

# In[10]:


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
from dash import html

# navbar code
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(html.A("Daily_Data_", href="#nav-daily-graph", style = {'color': '#fff'}), className="mt-1"),
        dbc.NavItem(html.A("_Most_effected_", href="#nav-top-country-graph", style = {'color': '#fff'}), className="mt-1"),
        dbc.NavItem(html.A("_Comparison_", href="#nav-cr-link", style = {'color': '#fff'}), className="mt-1"),
        dbc.NavItem(html.A("_About_Author", href="#nav-con-link", style = {'color': '#fff'}), className="mt-1"),
    ],
    brand="COVID-19",
    brand_href=" / ",
    color="dark",
    dark=True,
    className="p-3 fixed-top"
    

    
)


# ## Mainheading

# In[11]:


# main heading

main_heading = dbc.Container(
[
    html.H1(["COVID-19 Pandemic Analysis Dashboard"], className="my-5 pt-5 text-center"),
 ]
, className='pt-3')

# what is covid-19

what_is_covid = dbc.Container(
    [
        html.Div([
            html.H3('What is COVID-19?'),
            html.P("A coronavirus is a kind of common virus that causes an infection in your nose, sinuses, or upper throat. Most coronaviruses aren't dangerous."),
            html.P("COVID-19 is a disease that can cause what doctors call a respiratory tract infection. It can affect your upper respiratory tract (sinuses, nose, and throat) or lower respiratory tract (windpipe and lungs). It's caused by a coronavirus named SARS-CoV-2."),
            html.P("It spreads the same way other coronaviruses do, mainly through person-to-person contact. Infections range from mild to serious."),
            
        ]),
        html.Div([html.A(href='https://www.who.int/emergencies/diseases/novel-coronavirus-2019', children=[html.P('More information here')])]),
    ]
, className="mb-5")


# ## Dropdown and slider

# In[12]:


# select, country, no of days and category

world_tally = dbc.Container(
    [
        html.H2('World Data', style = {'text-align': 'center'}),
        
        dbc.Row(
            [
                dbc.Col(children = [html.H4('Confirmed'), 
                        html.Div(country_df['Confirmed'].sum(), className='text-info', style = {'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right p-2', style = {'border-top-left-radius': '6px', 'border-bottom-left-radius': '6px'}),
                
                dbc.Col(children = [html.H4('Recovered', style = {'padding-top': '0px'}),
                        html.Div(country_df['Recovered'].sum(), className='text-success', style = {'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right p-2'),
                
                dbc.Col(children = [html.H4('Death', style = {'padding-top': '0px'}), 
                        html.Div(country_df['Deaths'].sum(), className='text-danger', style = {'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right p-2'),
                
                dbc.Col(children = [html.H4('Active'),
                        html.Div(country_df['Active'].sum(),className='text-warning', style = {'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light p-2', style = {'border-top-right-radius': '6px', 'border-bottom-right-radius': '6px'}),
            ]
        , className='my-4 shadow justify-content-center'),
            
    ]
)


# ## Global map

# In[13]:


# global map heading

global_map_heading = html.H2(children='World map view', className='mt-5 py-4 pb-3 text-center')

# ploting the map
map_fig = px.scatter_geo(country_df, lat="Lat", lon="Long", hover_name="Country", hover_data=["Confirmed", "Deaths", "Recovered", "Active"],
                        color_discrete_sequence=["#e60039"], height=500, size_max=50, size=circle_radius)

map_fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0}, height=520)


# ## Daily covid-19 case report

# In[14]:


# daily data heading

daily_graph_heading = html.H2(id='nav-daily-graph', children='COVID-19 daily data and Total cases ', className='mt-5 pb-3 text-center')


# In[15]:


# dropdown to select the country, category and number of days

daily_country = confirmed_df['Country'].unique().tolist()
daily_country_list = []

my_df_type = ['Confirmed cases', 'Death rate', 'Recovered cases']
my_df_type_list = []

for i in daily_country:
    daily_country_list.append({'label': i, 'value': i})
    
for i in my_df_type:
    my_df_type_list.append({'label': i, 'value': i})
    
# dropdown to select country
country_dropdown = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(children = [html.Label('Select Country'), 
                        html.Div(dcc.Dropdown(id = 'select-country', options = daily_country_list, value='India'))],
                        width=3, className='p-2 mr-5'),
                
                dbc.Col(children = [html.Label('Drag to choose no of Days', style = {'padding-top': '0px'}),
                        html.Div(dcc.Slider( id = 'select-date',
                                            min=10,
                                            max=len(death_df.columns[3:]),
                                            step=1,
                                            value=40
                                        ,className='p-0'), className='mt-3')],
                        width=3, className='p-2 mx-5'),
                
                dbc.Col(children = [html.Label('Select category', style = {'padding-top': '0px'}), 
                        html.Div(dcc.Dropdown(id = 'select-category', options = my_df_type_list, value='Confirmed cases'))],
                        width=3, className='p-2 ml-5'),
            ]
        , className='my-4 justify-content-center'),
            
    ]
)


# In[16]:


# create graph for daily report

def daily_graph_gen(new_df, category):
    daily_data = []
    daily_data.append(go.Scatter(
                  x=new_df['Date'], y=new_df['coronavirus'], name="Covid-19 daily report", line=dict(color='#f36')))
    
    layout = {
        'title' :'Daily ' + category +'  in ' + new_df['Country'].values[0],
        'title_font_size': 26,
        'height':450,
        'xaxis' : dict(
            title='Date',
            titlefont=dict(
            family='Courier New, monospace',
            size=24,
            color='#7f7f7f'
        )),
        'yaxis' : dict(
            title='Covid-19 cases',
            titlefont=dict(
            family='Courier New, monospace',
            size=20,
            color='#7f7f7f'
        )),
        }  
    
    figure = [{
        'data': daily_data,
        'layout': layout
    }]
    
    return figure


# ## Top Effected countries with COVID-19

# In[17]:


# top 10 country with covid-19 heading

top_country_heading = html.H2(id='nav-top-country-graph', children='Top most Effected countries with COVID-19', className='mt-5 pb-3 text-center')


# In[18]:


# dropdown to select no of country
no_of_country = []

top_category = country_df.loc[0:, ['Confirmed', 'Active', 'Deaths', 'Recovered', 'Mortality_Rate']].columns.tolist()
top_category_list = []

for i in range(1,180):
    no_of_country.append({'label': i, 'value': i})
    
for i in top_category:
    top_category_list.append({'label': i, 'value': i})
    

# country dropdown object
top_10_country = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(children = [html.Label('Select no of Country'), 
                        html.Div(dcc.Dropdown(id = 'no-of-country', options = no_of_country, value=10))],
                        width=3, className='p-2 mr-5'),
                
                dbc.Col(children = [html.Label('Select category', style = {'padding-top': '0px'}), 
                        html.Div(dcc.Dropdown(id = 'top-category', options = top_category_list, value='Confirmed'))],
                        width=3, className='p-2 ml-5'),
            ]
        , className='my-4 justify-content-center'),
            
    ]
)


# ## confirmed and recovered case

# In[19]:


# heading 
cr_heading = html.H2(id='nav-cr-link', children='Confirmed and Recovered case', className='mt-5 pb-3 text-center')

# confrirm and recovered cases
top_country = country_df.head(10)
top_country_name = list(top_country['Country'].values)

cr = go.Figure(data=[
    go.Bar(name='Confirmed',marker_color='#f36', x=top_country_name, y=list(top_country['Confirmed'])),
    go.Bar(name='Recovered', marker_color='#1abc9c',x=top_country_name, y=list(top_country['Recovered'])),
])

# Change the bar mode
cr.update_layout(barmode='group', height=600, title_text="Top 10 countires with Confirmed and Recovered case")


# ## Conclusion

# In[20]:


con_heading = html.H2(id='nav-con-link', children='Conclusion', className='mt-5 pb-3 text-center')
end = html.Div(children= [
        html.H3('Sources:'),
        html.Div([html.A(href='https://github.com/CSSEGISandData/COVID-19', children=[html.P('1. John Hopkin University')])]),
        html.Div([html.A(href='https://plotly.com/dash/', children=[html.P( '2. Plotly')])]),
        
        html.H3('About Author'),
        html.H4('Aseem Kumar Anshu'),
        html.Div('I am pursuing Ph.D from Magadh University, Bodh Gaya. I am currently working at Amplipath Diagnostic and Research Centre, Patna.') 
        
])


# ## Main layout

# In[21]:


# main layout for Dash

app.layout = html.Div(
     [navbar,
     main_heading,
     what_is_covid,
     world_tally,
             
     # global map           
     html.Div(children = [global_map_heading,
         dcc.Graph(
             id='global_graph',
             figure=map_fig
         )
        ]
      ),
          
      # daily report graph
      dbc.Container([daily_graph_heading,
                    country_dropdown,
                    html.Div(id='country-total'),
         dcc.Graph(
             id='daily-graphs'
         )
        ]
      ),
    
       # top countrie
      dbc.Container([top_country_heading,
                    top_10_country,
         dcc.Graph(
             id='top-country-graph'
         )
        ]
      ),
        
      # confiremd and recovered cases
      dbc.Container(children = [cr_heading,
         dcc.Graph(
             id='cr',
             figure=cr
         )
        ]
      ),
      
      # conclusion
      dbc.Container(children = [con_heading,
          end
                               ]
      )
    ]
)


# In[22]:


server = app.server


# ## callback for Daily covid-19 case report

# In[23]:


# call back function to make change on click

@app.callback(
     [Output('daily-graphs', 'figure')],
     [Input('select-country', 'value'),
      Input('select-category', 'value'),
      Input('select-date', 'value')]
)

def country_wise(country_name, df_type, number):
    # on select of category copy the dataframe to group by country
    if df_type == 'Confirmed cases':
        df_type = confirmed_df.copy(deep=True)
        category = 'COVID-19 confirmed cases'
        
    elif df_type == 'Death rate':
        df_type = death_df.copy(deep=True)
        category = 'COVID-19 Death rate'
        
    else:
        df_type = recovered_df.copy(deep=True)
        category = 'COVID-19 recovered cases'
        
    
    # group by country name
    country = df_type.groupby('Country')
    
    # select the given country
    country = country.get_group(country_name)
    
    # store daily death rate along with the date
    daily_cases = []
    case_date = []
    
    # iterate over each row
    for i, cols in enumerate(country):
        if i > 3:
            # take the sum of each column if there are multiple columns
            daily_cases.append(country[cols].sum())
            case_date.append(cols)
            zip_all_list = zip(case_date, daily_cases)
            
            # creata a data frame
            new_df = pd.DataFrame(data = zip_all_list, columns=['Date','coronavirus'])

    # append the country to the data frame
    new_df['Country'] = country['Country'].values[0]
    
    # get the daily death rate
    new_df2 = new_df.copy(deep=True)
    for i in range(len(new_df) -1):
        new_df.iloc[i+1, 1] = new_df.iloc[1+i, 1] - new_df2.iloc[i, 1]
        if new_df.iloc[i+1, 1] < 0:
            new_df.iloc[i+1, 1] = 0
    
    new_df = new_df.iloc[-number:]
    
    return (daily_graph_gen(new_df, category))


# ## show total data for each country

# In[24]:


# show total data for each country

@app.callback(
     [Output('country-total', 'children')],
     [Input('select-country', 'value')]
)

def total_of_country(country):
#     country = new_df['Country'].values[0]
    
    # get the country data from country_df
    my_country = country_df[country_df['Country'] == country].loc[:, ['Confirmed', 'Deaths', 'Recovered', 'Active']]
    
    country_total = dbc.Container(
    [   
        html.H4('Total case in '+ country+ ''),
        dbc.Row(
            [
                dbc.Col(children = [html.H6('Confirmed'), 
                        html.Div(my_country['Confirmed'].sum(), className='text-info', style = {'font-size': '28px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right pt-2', style = {'border-top-left-radius': '6px', 'border-bottom-left-radius': '6px'}),
                
                dbc.Col(children = [html.H6('Recovered', style = {'padding-top': '0px'}),
                        html.Div(my_country['Recovered'].sum(), className='text-success', style = {'font-size': '28px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right pt-2'),
                
                dbc.Col(children = [html.H6('Death', style = {'padding-top': '0px'}), 
                        html.Div(my_country['Deaths'].sum(), className='text-danger', style = {'font-size': '28px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right pt-2'),
                
                dbc.Col(children = [html.H6('Active'),
                        html.Div(my_country['Active'].sum(),className='text-warning', style = {'font-size': '28px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light pt-2', style = {'border-top-right-radius': '6px', 'border-bottom-right-radius': '6px'}),
            ]
        , className='mt-1 justify-content-center'),
            
    ]
)
    
    return [country_total]


# ## Callback to show cases for top most effected countries

# In[25]:


@app.callback(
     [Output('top-country-graph', 'figure')],
     [Input('no-of-country', 'value'),
      Input('top-category', 'value')]
    )

# method to get the top countries

def top_ten(number, sort_by):
    # sorting the columns with top death rate
    country_df2 = country_df.sort_values(by=sort_by, ascending=False)
    
    # sort country with highest number of cases
    country_df2 = country_df2.head(number)
    
    top_country_data = []
    top_country_data.append(go.Bar(x=country_df2['Country'], y=country_df2[sort_by]))
    
    layout = {
        'title': 'Top ' + str(number) +' Country - ' + sort_by + ' case',
        'title_font_size': 26,
        'height':500,
        'xaxis': dict(title = 'Countries'),
        'yaxis': dict(title = sort_by)
    }
    
    figure = [{
        'data': top_country_data,
        'layout': layout
    }]
    
    return figure


# In[26]:


@app.callback(
    Output('out-component', 'value'),
    Input('in-component1', 'value'),
    Input('in-component2', 'value')
)
def large_params_function(largeValue1, largeValue2):
    largeValueOutput = someTransform(largeValue1, largeValue2)

    return largeValueOutput


# ## Initialize the app

# In[27]:


if __name__ == '__main__':
    app.run_server()

