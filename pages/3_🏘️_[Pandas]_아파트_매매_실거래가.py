import datetime
import pandas as pd
import requests
import streamlit as st
import xml.etree.ElementTree as ET
import utils.Lawd as LD
import utils.PublicApi as PA

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

st.write('### [Pandas] 아파트 매매 실거래가')
st.write('check out this [link]()')

lawd = LD.Lawd()
pa = PA.PublicApi()
main_category = ''
sub_category = ''
items = []

if not pa.is_existed_service_key():
  st.warning('Please set the service key for public api')
  st.stop()

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

exist_or_not = st.radio('폐지여부', options = ['존재', '폐지'])
category = lawd.extract_category(exist_or_not)

with st.container():
    def update():
        st.session_state['name'] = 'name'

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
        location_code = lawd.get_lawd_code(exist_or_not, main_category + ' ' + sub_category)
        request = pa.make_request(location_code, contract_date)
        res = requests.get(request)
        items = get_items(res)

with st.container():
    if items:
        df = pd.DataFrame(items)
        st.dataframe(df, use_container_width=True)

