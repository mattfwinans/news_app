import streamlit as st
import requests
from datetime import date, timedelta
import PIL
from PIL import Image
import base64


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

today = date.today()
lastweek = today - timedelta(days=search_date)


if btn:
    #url = f"https://newsapi.org/v2/everything?category={categories}&q={search}&from={lastweek}&to={today}&sortBy=relevancy&apiKey=7b3643eac6fa499ea6d0c7f2f7abf9b1"
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
