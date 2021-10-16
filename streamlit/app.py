import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences 

st.set_page_config(
    page_title="MooDy",
    page_icon="streamlit/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)
#######################################
# css

st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
    max-width: 80%;
    padding-top: 5rem;
    padding-right: 5rem;
    padding-left: 5rem;
    padding-bottom: 5rem;
    color: red;
}}
.results-html{{
    background-color: #0e1117;
}}
img{{
    max-width:10%;
    margin-bottom:10px;
    width: 50%;
    margin: 0 auto;
}}
iframe{{
    height: 290px;
}}

</style>
""",
        unsafe_allow_html=True,
    )

#######################################
# containers
header_container = st.container()	
results_container = st.container()	
dolar_widget_container = st.container()	
#######################################
# variables
#alza = '100%'
#baja = '-50%'

#######################################
# body
with header_container:

    # img logo
    st.image('streamlit/logo.png')

    # Headers and text
    st.title("Covid, Health and Economy Dilemma")
    st.header("Correlation between social mood and local economy variable(Dolar)")
    st.write("Information has always been a fundamental axis for any organization and institution, \
            from the incorporation of artificial intelligence it has been possible to generate dynamic metrics \
            that facilitate the reading of social humor, interests, and opinions. MooDy works in different level, \
            first analyze if the comment is positive, negative, or neutral. For doing this we work in our threshold to make this difference representative. \
            Then we evaluate the historical value of the dollar, and the model will predict if it’s goes up or down.")
    
    st.set_option('deprecation.showfileUploaderEncoding', False)

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        filepath = 'streamlit/gru_model.h5'
        data = pd.read_csv(uploaded_file)
        model = load_model (filepath, custom_objects=None, compile=True, options=None)
        X = np.array(data)
        X_test_pad = pad_sequences(X, value=-1000., dtype=float, padding='post', maxlen=30)
        result = model.predict(X_test_pad)
        col_1, col_2= st.columns(2)
        alza = round(float(result[0][0][0]),2)
        baja = -(round(float(result[0][0][1]),2))
        col_1.metric("Alza", round(float(result[0][0][0]),2), alza)
        col_2.metric("Baja", round(float(result[0][0][1]),2), baja)

with results_container:
    
    @st.cache
    def get_line_chart_data():

        return pd.DataFrame(
                np.random.randn(20, 3),
                columns=['a', 'b', 'c']
            )

    df = get_line_chart_data()

    st.line_chart(df)


with dolar_widget_container:
    
    components.iframe("https://dolar-plus.com/api/widget")
