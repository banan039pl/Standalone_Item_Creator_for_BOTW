import os
import sys
from shutil import copyfile
import oead
import win32gui

from files_manage import get_def_path, dir_to_list, get_endianness, get_res, get_file_path
from sarc_class import Sarc_file
from Actorinfo import create_hash, get_arr_index


class ShopData:
    def __init__(self, pack_name, shop, items):
        self.items = items
        self.shop = shop
        self.pack_name = pack_name
        self.data = Sarc_file(self.init_oven())
        if self.data.file is not None:
            self.bshop = self.do_actorlink()

    def init_oven(self):
        path = get_file_path(f'Actor\\Pack\\{self.shop}.sbactorpack')
        if not os.path.exists(f'cache\\{self.shop}.sbactorpack'):
            if not os.path.exists(path):
                win32gui.MessageBox(0, f'Cannot find file: \n {path}', "Error", 0)
                return None
            copyfile(path, f'cache\\{self.shop}.sbactorpack')
        return f'cache\\{self.shop}.sbactorpack'

    def do_actorlink(self):
        pio = get_raw_data(self.data.data_sarc, f'Actor/ActorLink/{self.shop}.bxml')

        pio.objects['LinkTarget'].params['ActorNameJpn'] = 'asdf'
        return str(pio.objects['LinkTarget'].params['ShopDataUser'])

        # update_sarc(pio, self.data, old_name, new_name)

    def get_pio_object(self, pio):
        try:
            return str(pio.objects['Header'].params['Table01'])
        except:
            print('Didnt work')
            available = ['Ancient', 'Normal']
            for ob in available:
                if ob in pio.objects:
                    return ob
            return ''

    def do_shopdata(self):
        old_name = f'Actor/ShopData/{self.bshop}.bshop'
        new_name = f'Actor/ShopData/{self.bshop}.bshop'
        pio = get_raw_data(self.data.data_sarc, old_name)
        table = self.get_pio_object(pio)
        # actors = dir_to_list(f'{self.pack_name}\\content\\Actor\\Pack')
        # iter = int(pio.objects[table].params['ColumnNum'].v) + 2
        iter = int(pio.objects[table].params['ColumnNum'].v)
        size = 0
        # items = []
        # for w in self.data_json['Weapons']: items.append(w)
        # for a in self.data_json['Armors']: items.append(a)

        for w in self.items:
            size += 1
            n = int_to_3digits(iter + size)
            pio.objects[table].params[f'ItemSort{n}'] = iter + size - 1
            pio.objects[table].params[f'ItemName{n}'] = oead.FixedSafeString64(w)
            if 'Npc_DressFairy' in self.shop:
                pio.objects[table].params[f'ItemNum{n}'] = 0
            else:
                pio.objects[table].params[f'ItemNum{n}'] = 1
            pio.objects[table].params[f'ItemAdjustPrice{n}'] = 0
            pio.objects[table].params[f'ItemLookGetFlg{n}'] = False
            pio.objects[table].params[f'ItemAmount{n}'] = 0

        pio.objects[table].params['ColumnNum'] = size + iter
        update_sarc(pio, self.data, old_name, new_name)

    def create_shop(self):
        if self.data.file is not None:
            if self.shop == 'Npc_AncientAssistant003':
                self.do_shop_grante()
            else:
                self.do_shopdata()
            # self.do_actorinfo()

            actorpack = f'{self.pack_name}\\content\\Actor\\Pack\\{self.shop}.sbactorpack'
            with open(actorpack, 'wb') as f:
                f.write(oead.yaz0.compress(self.data.data_writer.write()[1]))

    def get_all_tables(self, pio):
        tab = []
        for i, elem in enumerate(pio.objects['Header'].params):
            if i > 0: tab.append(str(pio.objects['Header'].params[elem]))
        return tab

    def do_shop_grante(self):
        old_name = new_name = f'Actor/ShopData/{self.bshop}.bshop'
        pio = get_raw_data(self.data.data_sarc, old_name)
        tabs = self.get_all_tables(pio)
        for table in tabs:
            iter = int(pio.objects[table].params['ColumnNum'].v)
            size = 0

            for w in self.items:
                size += 1
                n = int_to_3digits(iter + size)
                pio.objects[table].params[f'ItemSort{n}'] = iter + size - 1
                pio.objects[table].params[f'ItemName{n}'] = oead.FixedSafeString64(w)
                pio.objects[table].params[f'ItemNum{n}'] = 1
                pio.objects[table].params[f'ItemAdjustPrice{n}'] = 0
                pio.objects[table].params[f'ItemLookGetFlg{n}'] = False
                pio.objects[table].params[f'ItemAmount{n}'] = 0

            pio.objects[table].params['ColumnNum'] = size + iter
            update_sarc(pio, self.data, old_name, new_name)


def int_to_3digits(n):
    res = str(n)
    while len(res) != 3:
        res = '0' + res
    return res


def get_raw_data(data_sarc, file):
    data = data_sarc.get_file(file).data.tobytes()
    pio = oead.aamp.ParameterIO.from_binary(data)
    return pio


def update_sarc(pio, data, old_name, new_name):
    if old_name in data.data_writer.files:
        if old_name != new_name:
            del data.data_writer.files[old_name]
    data.data_writer.files[new_name] = oead.aamp.ParameterIO.to_binary(pio)


def create_shops(pack_name, data):
    shops = get_res('shops')
    def_shop = ''
    for key, item in shops.items():
        def_shop = item
        break

    res = {}
    for elem, item in data['Weapons'].items():
        shop = item.get('shop', def_shop)
        if shop not in res:
            res[shop] = []
        res[shop].append(elem)

    for elem, item in data['Armors'].items():
        shop = item.get('shop', def_shop)
        if shop not in res:
            res[shop] = []
        res[shop].append(elem)
    for shop in [s for s in res if s != 'None']:
        shopdata = ShopData(pack_name, shop, list(res[shop]))
        shopdata.create_shop()
