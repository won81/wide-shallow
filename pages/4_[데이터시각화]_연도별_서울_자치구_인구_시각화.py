import folium as f
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_folium import st_folium

st.write('### [데이터시각화] 연도별 서울 자치구 인구 시각화')
st.write('check out this [link](https://wide-shallow.tistory.com/entry/%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%8B%9C%EA%B0%81%ED%99%94-%EC%84%9C%EC%9A%B8-%EC%9E%90%EC%B9%98%EA%B5%AC-%EC%9D%B8%EA%B5%AC-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%8B%9C%EA%B0%81%ED%99%94%ED%95%98%EA%B8%B0)')


df = pd.read_csv('data/population_seoul_20230829.csv')
df.drop(df.index[[0,1]], inplace=True)

years = sorted(list(df.columns.values)[2:], reverse=True)
geo_data = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json'
center = [37.541, 126.986]

with st.container():
    year = st.selectbox(
            '검색년도',
            tuple(years))

    df[year] = df[year].astype(np.int64)
    m = f.Map(location=center, zoom_start=11)
    f.Choropleth(
        geo_data=geo_data,
        data=df,
        columns=('동별(2)', year),
        key_on='feature.properties.name',
        fill_color='BuPu',
        legend_name='인구수',
    ).add_to(m)
    st_data = st_folium(m, use_container_width=True)
