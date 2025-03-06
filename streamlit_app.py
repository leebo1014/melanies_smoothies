# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie！ :balloon:")
st.write(
    """
    Choose the fruits you want in custom Smoothie!
    """    
)

# option = st.selectbox(
#    "what is your favorite fruits?",
#    ("Banana", "Strawberries", "Peaches"),
# )

# st.write("your favorite fruits is:", option)


name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will is", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
# st.dataframe(data=my_dataframe, use_container_width=True)

 
ingredients_list = st.multiselect(
    label = '请问您喜欢吃什么水果',
    options=my_dataframe,
    default = None,
    format_func = str,
    max_selections=5 ,
    help = '选择您喜欢吃的水果'
    )

ingredients_string=''

for each_fruit in ingredients_list:
    ingredients_string+=each_fruit+' '

# if ingredients_list:
#     st.write('您喜欢吃的是', ingredients_list)
#     st.text(ingredients_list)

st.write('您喜欢吃的是', ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) values ('"""+ ingredients_string + """','"""+ name_on_order + """')"""

#st.write(my_insert_stmt)

time_to_insert=st.button("Submit Order")

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered,'+name_on_order+'!', icon="✅")




