from django.test import TestCase
import pandas as pd
# Create your tests here.
from django.urls import reverse

from polls.make_short import make_short_address


class MakeShortAddressFunctionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # добавление данных в таблицу
        test_data = pd.DataFrame([['aaaaaaaa', 'aa'], ['bbbb', 'bb']],
                                 columns=['long_addresses', 'short_addresses'])
        test_data = test_data.set_index('long_addresses')
        test_data.to_csv("test_data.csv")

    def test_new_string_is_added_to_frame(self):
        # проверить добавилась ли новая строка
        make_short_address('ccccc', "test_data.csv")
        res = pd.read_csv("test_data.csv", sep=",")
        res = res.set_index('long_addresses')
        flag = False
        if 'ccccc' in res.index:
            flag = True
        self.assertEquals(True, flag)

    def test_old_string_is_not_added_to_frame(self):
        # проверить, что существующая строка не будет добавлена второй раз
        make_short_address('ccccc', "test_data.csv")
        make_short_address('ccccc', "test_data.csv")
        res = pd.read_csv("test_data.csv", sep=",")
        res = res.set_index('long_addresses')
        flag = True
        if res[res.index == 'ccccc'].transform(len)[0] > 1:
            flag = False
        self.assertEquals(True, flag)

    def test_old_string_give_old_variant(self):
        # проверить, что существующий адрес не даст новую короткую ссылку
        make_short_address('bbbb', "test_data.csv")
        res = pd.read_csv("test_data.csv", sep=",")
        res = res.set_index('long_addresses')
        flag = False
        if res[res.index == 'bbbb'].short_addresses[0] == 'bb':
            flag = True
        self.assertEquals(True, flag)
