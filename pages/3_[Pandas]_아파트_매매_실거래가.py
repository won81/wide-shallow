import datetime
import pandas as pd
import requests
import streamlit as st
import xml.etree.ElementTree as ET
import utils.Lawd as LD
import utils.PublicApi as PA

st.set_page_config(layout="wide")

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

st.write('### [Pandas] 아파트 매매 실거래가')
st.write('check out this [link](https://wide-shallow.tistory.com/entry/Pandas-%EC%95%84%ED%8C%8C%ED%8A%B8-%EB%A7%A4%EB%A7%A4-%EC%8B%A4%EA%B1%B0%EB%9E%98%EA%B0%80)')

lawd = LD.Lawd()
pa = PA.PublicApi()
main_category = ''
sub_category = ''
items = []

def get_items(response):
    root = ET.fromstring(response.content)
    item_list = []
    for child in root.find('body').find('items'):
        elements = child.findall('*')
        data = {}
        for element in elements:
            tag = element.tag.strip()
            text = element.text.strip()
            # print tag, text
            data[tag] = text
        item_list.append(data)
    return item_list

with st.container():
    service_key = st.text_input('Service Key', value=pa.get_service_key(), type='password')
    if not pa.is_existed_service_key() and not service_key:
        st.warning('Please set the service key for public api first')

    exist_or_not = st.radio('폐지여부', options = ['존재', '폐지'])
    category = lawd.extract_category(exist_or_not)

    col1, col2, col3 = st.columns(3)
    with col1:
        main_category = st.selectbox(
            '시/도',
            tuple(category.keys())) 

    with col2:
        sub_category = st.selectbox(
            '시/군/구',
            ('시/군/구', ) + tuple(sorted(category[main_category])))

    with col3:
        contract_date = st.text_input('계약년월', '201512')

    search = st.button('조회하기')

    if search:
        location_code = lawd.get_lawd_code(main_category + ' ' + sub_category, exist_or_not)
        request = pa.make_request(location_code, contract_date, service_key)
        res = requests.get(request)
        items = get_items(res)

with st.container():
    if items:
        df = pd.DataFrame(items)
        st.dataframe(df, use_container_width=True)

