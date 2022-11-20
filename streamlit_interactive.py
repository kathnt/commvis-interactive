# Katsumi Ibraki
# si649f22 interactive vis

# imports we will use
import altair as alt
from altair import pipe, limit_rows, to_values
import plotly.express as px
import pandas as pd
import streamlit as st
import numpy as np

#Title
st.title("Curry Visualizations")
st.markdown('by Katsumi Ibaraki')


### Variations (Vis 1)
recipe = pd.read_csv('recipe_copy.csv')
df_melt = recipe.melt(id_vars=['title', 'NER', 'Country', 'Distance'])

dropdown_options = ['garlic',
 'salt',
 'coconut milk',
 'onion',
 'fish sauce',
 'water',
 'red curry',
 'ginger',
 'vegetable oil',
 'tomatoes',
 'curry powder',
 'lime',
 'sugar',
 'cilantro',
 'brown sugar',
 'turmeric',
 'basil',
 'garam masala',
 'ground coriander',
 'cumin',
 'soy sauce',
 'rice',
 'shrimp',
 'potatoes',
 'red bell pepper',
 'green curry',
 'chicken breasts',
 'chicken broth',
 'cinnamon',
 'chili powder',
 'carrots',
 'canola oil',
 'peanut oil',
 'cumin seeds',
 'butter',
 'peanuts',
 'red pepper',
 'light coconut milk',
 'green beans',
 'flour',
 'coriander seeds',
 'cloves',
 'lemon juice',
 'green onions',
 'green chilies',
 'pepper',
 'kosher salt']

df_melt=df_melt[df_melt['variable'].isin(dropdown_options)]

t = lambda data: pipe(data, limit_rows(max_rows=23855), to_values)
alt.data_transformers.register('custom', t)
alt.data_transformers.enable('custom')

def new_theme():
    font = "Times"
    
    return {
        "config" : {
             "title": {'font': font},
             "axis": {
                  "labelFont": font,
                  "titleFont": font
             },
            'legend': {
                  "labelFont": font,
                  "titleFont": font
             },
            'view': {
                'height': 300,
                'width': 400,
            },
            'mark': {
                'color': '#ab5787',
                'fill': '#ab5787'
            },
            "range": {
                "category": ["#f63366", "#fffd80", "#0068c9", "#ff2b2b", "#09ab3b"],
                
            },
        }
    }

alt.themes.register('new_theme', new_theme)
alt.themes.enable('new_theme')

dropdown = alt.binding_select(options=dropdown_options, name='Ingredient ')
selection = alt.selection_single(
    fields=['variable'],
    init={'variable': dropdown_options[0]},
    bind=dropdown
)


color_selection = alt.selection_single(on='mouseover', empty='none') 

colorCondition = alt.condition(color_selection,alt.value(0.5),alt.value(1)) 



ing_chart = alt.Chart(df_melt).transform_joinaggregate(
    groupby=['Country']
).mark_bar(size=20).encode(
    y = alt.Y('Country', sort=['India','Sri Lanka','Bangladesh','Pakistan','Japan','Singapore','Myanmar','Thailand','Vietnam',
                               'Indonesia','South Africa']),
    x = alt.X('mean(value):Q',axis=alt.Axis(format='.0%',title='Percentage of Recipes')),
    opacity = colorCondition,
    tooltip=[ 'Country', alt.Tooltip('mean(value):Q', format=".1%", title='Percentage')]
).add_selection(
    selection
).add_selection(
    color_selection
).transform_filter(
    selection
)

def make_ing_chart(ing_name):
    temp_ing_chart = alt.Chart(df_melt).transform_joinaggregate(
        groupby=['Country']
    ).mark_bar(size=20).encode(
        y = alt.Y('Country', sort=['India','Sri Lanka','Bangladesh','Pakistan','Japan','Singapore','Myanmar','Thailand','Vietnam',
                                   'Indonesia','South Africa']),
        x = alt.X('mean(value):Q',axis=alt.Axis(format='.0%',title='Percentage of Recipes')),
        opacity = colorCondition,
        #color = alt.value(color_str),
        tooltip=[ 'Country', alt.Tooltip('mean(value):Q', format=".1%", title='Percentage')]
    ).add_selection(
        color_selection
    ).transform_filter(
        alt.datum.variable==ing_name
    )
    temp_ing_chart

### Proteins (Vis 2)
recipe_filtered = pd.read_csv('manual_cleaned.csv')

recipe_chicken = recipe_filtered[(recipe_filtered['NER'].str.contains("chicken")) | (recipe_filtered['title'].str.contains("chicken|Chicken"))]
recipe_beef = recipe_filtered[(recipe_filtered['NER'].str.contains("beef")) | (recipe_filtered['title'].str.contains("beef|Beef"))]
recipe_pork = recipe_filtered[(recipe_filtered['NER'].str.contains("pork")) | (recipe_filtered['title'].str.contains("pork|Pork"))]
recipe_lamb = recipe_filtered[(recipe_filtered['NER'].str.contains("lamb|mutton")) | (recipe_filtered['title'].str.contains("lamb|Lamb|mutton|Mutton"))]
recipe_shellfish = recipe_filtered[(recipe_filtered['NER'].str.contains("clam|mussel|oyster|scallop|shrimp|lobster|crayfish|crab")) | (recipe_filtered['title'].str.contains("clam|Clam|mussel|Mussel|oyster|Oyster|scallop|Scallop|shrimp|Shrimp|lobster|Lobster|crayfish|Crayfish|crab|Crab"))]
recipe_fish = recipe_filtered[(recipe_filtered['NER'].str.contains("fish|tilapia|snapper|cod|mahi-mahi|halibut|basa|ling|tuna")) | (recipe_filtered['title'].str.contains("fish|Fish|tilapia|Tilapia|snapper|Snapper|cod|Cod|mahi-mahi|Mahi-mahi|halibut|Halibut|basa|Basa|ling|Ling|tuna|Tuna"))]

recipe_bean = recipe_filtered[(recipe_filtered['NER'].str.contains("tempeh|bean|tofu")) | (recipe_filtered['title'].str.contains("tempeh|Tempeh|bean|Bean|Tofu|tofu"))]
recipe_egg = recipe_filtered[(recipe_filtered['NER'].str.contains("egg")) | (recipe_filtered['title'].str.contains("egg|Egg"))]
recipe_vegan = recipe_filtered[(recipe_filtered['title'].str.contains("vege|Vege"))]

recipe_chicken.insert(7,'Protein','Chicken')
recipe_chicken.insert(8,'Protein Group','Meat')

recipe_beef.insert(7,'Protein','Beef')
recipe_beef.insert(8,'Protein Group','Meat')

recipe_pork.insert(7,'Protein','Pork')
recipe_pork.insert(8,'Protein Group','Meat')

recipe_lamb.insert(7,'Protein','Lamb')
recipe_lamb.insert(8,'Protein Group','Meat')

recipe_shellfish.insert(7,'Protein','Shellfish')
recipe_shellfish.insert(8,'Protein Group','Seafood')

recipe_fish.insert(7,'Protein','Fish')
recipe_fish.insert(8,'Protein Group','Seafood')

recipe_bean.insert(7,'Protein','Bean')
recipe_bean.insert(8,'Protein Group','Vegetarian')

recipe_egg.insert(7,'Protein','Egg')
recipe_egg.insert(8,'Protein Group','Vegetarian')

recipe_vegan.insert(7,'Protein','Vegan')
recipe_vegan.insert(8,'Protein Group','Vegetarian')

new_recipe = pd.concat([recipe_chicken, recipe_beef, recipe_pork, recipe_lamb, recipe_shellfish, recipe_fish, recipe_bean, recipe_egg, recipe_vegan])

def protein_theme():
    font = "Times"
    
    return {
        "config" : {
             "title": {'font': font},
             "axis": {
                  "labelFont": font,
                  "titleFont": font
             },
            'legend': {
                  "labelFont": font,
                  "titleFont": font
             },
            'view': {
                'height': 300,
                'width': 400,
            },
            'mark': {
                'color': '#ab5787',
                'fill': '#ab5787'
            },
            "range": {
                "category": ['#F88379', '#EE4B2B', '#C41E3A', '#880808','#0047AB','#89CFF0','#90EE90','#32CD32','#478778'],
                
            },
        }
    }

alt.themes.register('protein_theme', protein_theme)
alt.themes.enable('protein_theme')

pt_color_selection = alt.selection_single(on='mouseover') 
pt_colorCondition = alt.condition(pt_color_selection,alt.Color('Protein:N', sort=['Chicken','Beef','Lamb', 'Pork','Shellfish','Fish', 'Bean', 'Egg', 'Vegan']),alt.value('#E5E4E2')) 

pt_selection = alt.selection_multi(fields=['Protein:N'], bind='legend')

pt_text = alt.Chart(new_recipe).mark_text(align='center', dy=10, baseline='middle', color='white').encode(
    x = alt.X('Protein Group:N'),
    y = alt.Y('count():Q', stack='zero'),
    order='count():Q',
    detail='Protein',
    text=alt.Text('Protein:N'),
).properties(
    width=500,
    height=500
)

protein_bars = alt.Chart(new_recipe).mark_bar(size=90).transform_joinaggregate(
    groupby = ['Protein'],
    cnt ='count()',
).transform_joinaggregate(
    groupby= ['Protein Group'],
    group_cnt='count()'
).transform_calculate(
    ptg = 'datum.cnt / 9863',
    grp_ptg = 'datum.cnt / datum.group_cnt'
).encode(
    x = alt.X('Protein Group:N'),
    y = alt.Y('count():Q', stack='zero'),
    order='count():Q',
    color = pt_colorCondition,
    #opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
    tooltip=[ 'Protein', 'Protein Group', alt.Tooltip('ptg:Q', format=".1%", title='Within All Recipes'), alt.Tooltip('grp_ptg:Q', format=".1%", title='Within Protein Group')]
).add_selection(
    pt_color_selection
).add_selection(
    pt_selection
).properties(
    width=500,
    height=500
)


### History (vis 3)
df = pd.read_csv('curry_history.csv')
# Adds all available categories to each time frame
catg = df['State'].unique()
dts = df['Year'].unique()
exist = df['Years of Existence'].unique()

for tf in dts:
    for i in catg:
        for ex in exist:
            df.loc[len(df.index)] = [tf, '', i, '', ex]
fig = px.choropleth(df, locations="Country",
                    color=df["Years of Existence"],
                    title='<b>Spread of Curry (15th Century ~ 21st Century)</b>',
#                     color_discrete_map={
#                         'New': '#ff0d0d',
#                         'Exist' : '#98FB98'},
#                     category_orders={
#                       'category' : [
#                           'New','Exist'
#                       ]
#                     },
                    color_continuous_scale=['#ff0000', '#ffeded'],
                    hover_name="Country",
                    hover_data={"Year":False, "Country":False, "State":False, "Exist From":True, "Years of Existence":True},
                    locationmode="country names",
                    animation_frame='Year',
                    # color_continuous_midpoint = 3,
# color_continuous_scale=px.colors.sequential.thermal_r)
                   )
fig.update_layout(
    showlegend=True,
    legend_title_text='<b>Years of Existence</b>',
    font={"size": 14, "color": "#808080", "family" : "Times"},
    margin={"r":30,"t":40,"l":0,"b":0},
    legend=dict(orientation='v'),
    geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='#e0fffe'),
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family="Times"
    )
)

# Adjust map geo options
fig.update_geos(showcountries=True, showcoastlines=True,
                showland=True, fitbounds=False,
                lataxis_range=[-40.0, 60.0],
                lonaxis_range=[1.0, 155.0],
                subunitcolor='white')

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500



##### Display graphs

st.sidebar.title("")
#adding a selectbox

choice = st.sidebar.selectbox(

    'Select a visualization to display',
    ('Variations','Protein Distribution','History')
)

if choice=='Variations':
    st.header('Variations in Ingredients')
    st.subheader('Some ingredients are common across all countries, while some ingredients are used only in certain countries.')
    st.markdown('First, we look at **garlic**, which is quite common in most curry recipes.')
    make_ing_chart('garlic')
    st.markdown('Another very common ingredient is **onions/shallots**.')
    make_ing_chart('onion')
    st.markdown('On the other hand, **fish sauce** is only common in Myanmar, Vietnam, and Thailand.')
    make_ing_chart('fish sauce')
    st.markdown('**Soy sauce** is also not very common, but are used in Singapore, Japan, and Myanmar.')
    make_ing_chart('soy sauce')
    st.markdown('When looking at spices, Japan and Thailand have low usage of **turmeric**.')
    make_ing_chart('turmeric')
    st.markdown('With **cumin**, Japan, Thailand, Myanmar, and Vietnam all have low usage.')
    make_ing_chart('cumin')
    st.subheader('\n')
    st.caption('With the interactive chart below, choose an ingredient from the drop down and see if you can find other trends...')
    ing_chart
    
elif choice=='Protein Distribution':
    st.header('Protein Distribution')
    st.caption('The distribution of common proteins used in curry, by protein group (meat, seafood, vegetarian)')
    (protein_bars + pt_text)

elif choice=='History':
    st.header('History')
    st.caption('New countries are indicated with bright red, and the color becomes lighter as the curry in that country becomes older.')
    st.plotly_chart(fig, use_container_width=True)



