import streamlit as st
import pandas as pd
import utils.Lawd as LD
import utils.PublicApi as PA

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

st.write('### [Pandas] 법정동코드 조회하기')
st.write('check out this [link](https://wide-shallow.tistory.com/entry/Pandas-%EB%B2%95%EC%A0%95%EB%8F%99%EC%BD%94%EB%93%9C-%EC%A1%B0%ED%9A%8C%ED%95%98%EA%B8%B0)')

lawd = LD.Lawd()
main_category = ''
sub_category = ''

exist_or_not = st.radio('폐지여부', options = ['존재', '폐지'])
category = lawd.extract_category(exist_or_not)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        main_category = st.selectbox(
            '시/도',
            tuple(category.keys()))

    with col2:
        sub_category = st.selectbox(
            '시/군/구',
            ('시/군/구', ) + tuple(sorted(category[main_category])))

with st.container():
    searched = lawd.get_lawd(exist_or_not, main_category, sub_category)
    st.dataframe(searched, use_container_width = True)

