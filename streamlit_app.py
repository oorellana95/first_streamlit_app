import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt") # Get fruit list 
my_fruit_list = my_fruit_list.set_index('Fruit') # Set index
fruits_choosen = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries']) #  pick list
fruits_to_show = my_fruit_list.loc[fruits_choosen]
streamlit.dataframe(fruits_to_show) # Display the table on the page.

def get_fruityvie_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())     # normalize the json semi-structured data to structured data
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information.')
  else:
    fruityvice_data = get_fruityvie_data(fruit_choice)
    streamlit.dataframe(fruityvice_data)

except URLError as e:
  streamlit.error()
  

# Snowflake connector
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()
        
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)
    
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
        return "Thanks for adding " + new_fruit
        

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
        
if streamlit.button('Add Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    message = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(message)
