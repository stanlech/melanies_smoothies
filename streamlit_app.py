# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
streamlit.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
streamlit.write(
    """Choose the fruits you want in your custom Smoothie.
    """
)

name_an_order = streamlit.text_input("Name on Smoothie:")
streamlit.write("The name on your Smoothie will be:", name_an_order)
cnx = streamlit.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#streamlit.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = streamlit.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections = 5
)
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
            ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_an_order + """')"""
    
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = streamlit.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        streamlit.success('Your Smoothie is ordered, ' + name_an_order + '!', icon="✅")
