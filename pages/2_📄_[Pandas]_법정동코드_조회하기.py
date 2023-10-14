import streamlit as st
import pandas as pd

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

st.write('### [Pandas] 법정동코드 조회하기')
st.write('check out this [link](https://wide-shallow.tistory.com/entry/Pandas-%EB%B2%95%EC%A0%95%EB%8F%99%EC%BD%94%EB%93%9C-%EC%A1%B0%ED%9A%8C%ED%95%98%EA%B8%B0)')

category = dict()
raw_data = pd.read_csv('./data/lawd_cd_raw_data.txt', sep = '\t', encoding = 'cp949')
raw_data['법정동코드'] = raw_data['법정동코드'].apply(str)

def extract_category(area):
    try:
        first, remain = area.split(' ', 1)
    except ValueError:
        return area, ''
    return first, remain

exist_or_not = st.radio('폐지여부', options = ['존재', '폐지'])
main_category = ''
sub_category = ''

category.clear()
category['시/도'] = tuple()
for area_name in raw_data[raw_data['폐지여부'] == exist_or_not]['법정동명']:
    main, remain = extract_category(area_name)
    if not remain:
        continue
    sub, remain = extract_category(remain)
    if main not in category:
        category[main] = set()
    category[main].add(sub)

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
    is_data_existed = raw_data['폐지여부'] == exist_or_not
    searched = ''
    if main_category != '시/도':
        searched = main_category
    if sub_category != '시/군/구':
        searched += ' ' + sub_category
    is_searched = raw_data['법정동명'].str.contains(searched)
    st.dataframe(raw_data[is_data_existed & is_searched], use_container_width = True)

