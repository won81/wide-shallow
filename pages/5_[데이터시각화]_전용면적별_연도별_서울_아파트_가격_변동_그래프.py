import altair as alt
import datetime
import pandas as pd
import requests
import streamlit as st
import xml.etree.ElementTree as ET
import utils.Lawd as LD
import utils.PublicApi as PA

st.set_page_config(layout="wide")

st.write('### [데이터시각화] 전용면적별 연도별 서울 아파트 가격 변동 그래프')
st.write('check out this [link](https://wide-shallow.tistory.com/entry/%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%8B%9C%EA%B0%81%ED%99%94-%EC%A0%84%EC%9A%A9%EB%A9%B4%EC%A0%81%EB%B3%84-%EC%97%B0%EB%8F%84%EB%B3%84-%EC%84%9C%EC%9A%B8-%EC%95%84%ED%8C%8C%ED%8A%B8-%EA%B0%80%EA%B2%A9-%EB%B3%80%EB%8F%99-%EA%B7%B8%EB%9E%98%ED%94%84)')

lawd = LD.Lawd()
pa = PA.PublicApi()
main_category = '서울특별시'
sub_category = ''
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] 

if 'deals' not in st.session_state:
    st.session_state.deals = []

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


category = lawd.extract_category()

with st.container():
    service_key = st.text_input('Service Key', value=pa.get_service_key(), type='password')
    if not pa.is_existed_service_key() and not service_key:
        st.warning('Please set the service key for public api first')


    col1, col2 = st.columns(2)
    with col1:
        sub_category = st.selectbox(
            '시/군/구',
            ('시/군/구', ) + tuple(sorted(category[main_category])))

    with col2:
        contract_date = st.text_input('계약년도', '2015')

    search = st.button('조회하기')
    if search:
        st.session_state.deals = []
        location_code = lawd.get_lawd_code(main_category + ' ' + sub_category)
        for month in range(1, 13):
            request = pa.make_request(location_code, contract_date + '{:02d}'.format(month), service_key)
            res = requests.get(request)
            st.session_state.deals.extend(get_items(res))

with st.container():
    if st.session_state.deals:
        df = pd.DataFrame(st.session_state.deals)

        df['월'] = df['월'].astype(int)
        df['거래금액'].replace(',','', regex=True, inplace=True)
        df['거래금액'] = df['거래금액'].astype(int)
        df['전용면적'] = df['전용면적'].astype(float)
 
        col1, col2, col3 = st.columns(3)
        with col1:
            beopjeongdong = st.selectbox(
                '법정동',
                tuple(sorted(list(set(df['법정동'].values.tolist())))))

        with col2:
            apartment = st.selectbox(
                '아파트',
                tuple(sorted(list(set(df[df['법정동'] == beopjeongdong]['아파트'].values.tolist())))))

        with col3:
            area = st.selectbox(
                '전용면적',
                tuple(sorted(list(set(df[(df['법정동'] == beopjeongdong) & (df['아파트'] == apartment)]['전용면적'].values.tolist())))))

        df_selected = df[(df['법정동'] == beopjeongdong) & (df['아파트'] == apartment) & (df['전용면적'] == float(area))]
        chart = (
            alt.Chart(df_selected)
            .mark_circle(size = 40)
            .encode(
                x=alt.X('월:N', scale=alt.Scale(domain=months)),
                y=alt.Y('거래금액:Q', scale=alt.Scale(domain=[0, df_selected['거래금액'].max() + 10000]))
            )
        )
        final_chart = chart + chart.transform_regression('월','거래금액').mark_line() 
        st.altair_chart(final_chart, use_container_width=True)

