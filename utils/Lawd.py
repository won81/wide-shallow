import pandas as pd

class Lawd:
    def __init__(self):
        self.raw_data = pd.read_csv('./data/lawd_cd_raw_data.txt', sep = '\t', encoding = 'cp949')
        self.raw_data['법정동코드'] = self.raw_data['법정동코드'].apply(str)
        self.category = dict()

    def _extract_category(self, area):
        try:
            first, remain = area.split(' ', 1)
        except ValueError:
            return area, ''
        return first, remain

    def extract_category(self, exist = '존재'):
        self.category.clear()
        self.category['시/도'] = tuple()
        for area_name in self.raw_data[self.raw_data['폐지여부'] == exist]['법정동명']:
            main, remain = self._extract_category(area_name)
            if not remain:
                continue
            sub, remain = self._extract_category(remain)
            if main not in self.category:
                self.category[main] = set()
            self.category[main].add(sub)
        return self.category

    def get_lawd(self, main, sub, exist = '존재'):
        is_data_existed = self.raw_data['폐지여부'] == exist
        searched = ''
        if main != '시/도':
            searched = main
        if sub != '시/군/구':
            searched += ' ' + sub
        is_searched = self.raw_data['법정동명'].str.contains(searched)
        return self.raw_data[is_data_existed & is_searched]

    def get_lawd_code(self, lawd, exist = '존재'):
        is_data_existed = self.raw_data['폐지여부'] == exist
        is_searched = self.raw_data['법정동명'] == lawd 
        return self.raw_data[is_data_existed & is_searched].법정동코드.tolist()[0][0:5]

