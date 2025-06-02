import streamlit as st
import pandas as pd

st.title('DataFrame Example')

dataframe = pd.DataFrame({
    'first column' : [1, 2, 3, 4],
    'second column' : [10, 20, 30, 40]
})

st.dataframe(dataframe)

st.table(dataframe)

st.metric(label = '온도', value="10°C", delta='1.2°C')
st.metric(label = '삼성전자', value='61,000원', delta='-1,200원')

col1, col2, col3 = st.columns(3)
col1.metric(label = '달러(USD)', value="1,383원", delta='-12.00원')
col2.metric(label = '일본JPY(100엔)', value="958.63원", delta='-7.44원')
col3.metric(label = '유럽연합EUR', value="1,3335.82원", delta='11.44원')

