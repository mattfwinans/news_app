import streamlit as st
import requests
#from datetime import date, timedelta, datetime
import datetime as dt
import PIL
from PIL import Image
import base64
import psycopg2
from dotenv import load_dotenv
import os


st.set_page_config(page_title='CSM Search Tool', page_icon=':sunglasses:')



LOGO_IMAGE = "ibm-logo.jpeg"

# st.markdown(
#     """
#     <style>
#     .container {
#         # display: flex;
#         transform: scale(0.5);
#     }

#     .logo-img {
#         float: center;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

st.markdown(
    f"""
    <div>
        <img class="logo-img" src="data:image/jpeg;base64, {base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}", width='200'>
    </div>
    """,
    unsafe_allow_html=True
)

# st.markdown(
#     """ 
#     <div>
#         <img src= "ibm-logo.jpeg">
#     </div>
#     """, 
#     unsafe_allow_html=True

# )


st.title('Customer Success News App')

load_dotenv(load_dotenv())
dbname = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")


#Function to connect to Postgres DB and insert search string

def insert_search(search_data):
    #data to be insterted
    data_insert = str(search_data)
    ts = dt.datetime.now()

    #postgres connection
    conn = psycopg2.connect(host='postgres',
                        port='5432',
                        dbname=dbname,
                        user=user,
                        password=password
                        )

    #building table and posting data to columns    
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS search_db \
        (search_history varchar(250) NOT NULL, \
        search_timestamp timestamp NOT NULL);")
    cur.execute("INSERT INTO search_db (search_history, search_timestamp) VALUES(%s, %s);", (data_insert, ts,))
    conn.commit()
    conn.close()




# with st.container:
# image = Image.open('ibm-logo.jpeg', )

# ibm_logo = st.image(image, caption='IBM', width=200)

# st.header(ibm_logo)

col1, col2, col3 = st.columns([3.5, 1, 2])
with col1:
    search = st.text_input('Enter Account Name or Topic')

    with col2:
        searchcriteria = st.radio('Search By:', ('relevancy', 'popularity', 'publishedAt'))
        # search_date = st.number_input('Search within the last number of days', min_value=1, max_value= 30, step=1, value=7)
        

    with col3:
         search_date = st.number_input('Search within the last number of days', min_value=0, max_value= 30, step=1, value=7)

btn = st.button('Enter')

today = dt.date.today()
lastweek = today - dt.timedelta(days=search_date)


if btn:
    #url = f"https://newsapi.org/v2/everything?category={categories}&q={search}&from={lastweek}&to={today}&sortBy=relevancy&apiKey=7b3643eac6fa499ea6d0c7f2f7abf9b1"
    
    insert_search(search) #post search string to Postgres Database

    url = f"https://newsapi.org/v2/everything?q={search}&from={lastweek}&to={today}&sortBy={searchcriteria}&language=en&apiKey=7b3643eac6fa499ea6d0c7f2f7abf9b1"

    r = requests.get(url)
    r = r.json()
    articles = r['articles']
    
    for article in articles:
        st.header(article['title'])
        st.write(f"<span style='color:light-blue'> Published Date: {article['publishedAt']} </span>", unsafe_allow_html=True)
        if article['author']:
            st.write('Written by:', article['author'])
        st.write('Source:', article['source']['name'])
        st.write('Description:', article['description'])
        st.write('Link to Full Article', article['url'])
        if article['urlToImage']:
            try:
                st.image(article['urlToImage'])
            except PIL.UnidentifiedImageError:
                print('no image to display')
    


#newsapi info: https://newsapi.org/docs/endpoints/everything






#Postgres sample code


# load_dotenv(load_dotenv())
# dbname = os.getenv("POSTGRES_DB")
# user = os.getenv("POSTGRES_USER")
# password = os.getenv("POSTGRES_PASSWORD")


# def insert_search(search):
#     conn = psycopg2.connect(host='postgres',
#                         port='5432',
#                         dbname=dbname,
#                         user=user,
#                         password=password
#                         )
#     sql = """CREATE TABLE IF NOT EXISTS search_db (search_history VARCHAR NOT NULL);
#         INSERT INTO search_db (search_history) VALUES(%s) RETURNING (search);  """


#     cur = conn.cursor()

#     cur.execute(sql, (search, ))
#     conn.commit()
#     conn.close()



# cursor = conn.cursor()
# cursor.execute("INSERT INTO a_table (c1, c2, c3) VALUES(%s, %s, %s)", (v1, v2, v3))
# conn.commit() # <- We MUST commit to reflect the inserted data
# cursor.close()
# conn.close()

# CREATE TABLE IF NOT EXISTS app_user (
#   username varchar(45) NOT NULL,
#   password varchar(450) NOT NULL,
#   enabled integer NOT NULL DEFAULT '1',
#   PRIMARY KEY (username)
# )


