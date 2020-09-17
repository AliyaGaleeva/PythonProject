import random
import string
import pandas as pd


# import nympy as np

def make_short_address(long_address, date_path):
    '''
    метод для генерирования короткого адреса
    :param long_address: длинный адрес
    :param date_path: таблица с ссылками
    :return: короткая ссылка
    '''
    urls = pd.read_csv(date_path, sep=",")
    urls = urls.set_index('long_addresses')
    # a = urls[long_address].any()
    if long_address in urls.index:
        return urls.loc[long_address].short_addresses

    n = int(len(long_address) / 4) + 1
    if n > 6:
        n = 6
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
    short_address = res

    while True:
        if urls.index[urls['short_addresses'] == short_address].any():
            short_address = short_address + "!"
        else:
            break

    # result = pd.concat([urls, ], ignore_index=True)
    urls.loc[str(long_address)] = short_address
    # urls = urls.append({'long_addresses': long_address, 'short_addresses': short_address}, ignore_index=True)
    urls.to_csv(date_path)
    return short_address
