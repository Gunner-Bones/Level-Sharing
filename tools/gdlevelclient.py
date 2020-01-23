import base64
import gzip
import os
import random
import struct
import time
import xml.etree.ElementTree as EleTree
import zlib

import tools.clientinput as ci
# GD Level Manager API by Sputnix

SAVE_FILE = "CCLocalLevels.dat"
SAVE_PATH = os.getenv("localappdata") + "\\GeometryDash\\"

# ENCRYPTION TOOLS


def xor(data, key):
    res = []
    for i in data:
        res.append(i ^ key)
    return bytearray(res).decode()


def b64decrypt(encoded_data):
    while len(encoded_data) % 4 != 0:
        encoded_data += "="
    byte_encoded = base64.b64decode(encoded_data)
    return byte_encoded


def decrypt(ls):
    fin = ls.replace('-', '+').replace('_', '/').replace("\0", "")
    fin = b64decrypt(fin)
    fin = gzip.decompress(fin)
    return fin


def encrypt(dls):
    fin = gzip.compress(dls)
    fin = base64.b64encode(fin)
    fin = fin.decode("utf-8").replace('+', '-').replace('/', '_')
    fin = 'H4sIAAAAAAAAC' + fin[13:]
    return fin

# GAME SAVE


def open_file(path):
    fr = open(path, "rb")
    data = fr.read()
    fr.close()
    return data


def gs_decrypt():
    while True:
        try:
            data = open_file(SAVE_PATH + SAVE_FILE)
            break
        except FileNotFoundError:
            pass
        time.sleep(1)
    res = xor(data, 11)
    fin = zlib.decompress(base64.b64decode(res.replace('-', '+').replace('_', '/').encode())[10:], -zlib.MAX_WBITS)
    return fin


def gs_encrypt(data):
    compressed_data = zlib.compress(data)
    crc32 = struct.pack('I', zlib.crc32(data))
    data_size = struct.pack('I', len(data))
    encrypted = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x0b' + compressed_data[2:-4] + crc32 + data_size
    encoded = base64.b64encode(encrypted).decode().replace('+', '-').replace('/', '_').encode()
    fin = Xor(encoded, 11).encode()
    try:
        fw = open(fPath + save, "wb")
    except FileNotFoundError:
        # print("Failed to write", save, "!")
        pass
    else:
        fw.write(fin)
        fw.close()
        # print("Done!")


GS_DICT_LENGTH = {'4': 'XL', '3': 'Long', '2': 'Medium', '1': 'Short', '0': 'Tiny'}


class GDLevel:
    def __init__(self, name, desc=None, length=None, data=None):
        self.name = name
        self.desc = desc
        self.length = length
        self.data = data


class GameSave:
    def __init__(self):
        self.gs = gs_decrypt()
        self.status = True
        tree = ET.ElementTree(ET.fromstring(gs))
        self.root = tree.getroot()
        self.tl = None
        client_tl_name = None
        client_tl_desc = None
        client_tl_length = None
        client_tl_data = None
        for i in range(len(self.root[0][1][3])):
            if self.root[0][1][3][i].text == 'k2':
                client_tl_name = self.root[0][1][3][i + 1].text
            elif self.root[0][1][3][i].text == 'k3':
                client_tl_desc = base64.b64decode(self.root[0][1][3][i + 1].text)
            elif self.root[0][1][3][i].text == 'kCEK':
                client_tl_length = GS_DICT_LENGTH[self.root[0][1][3][i + 1].text]
            if self.root[0][1][3][i].text == 'k4':
                client_tl_data = decrypt(self.root[0][1][3][i + 1].text)
        if client_tl_name:
            self.tl = GDLevel(name=client_tl_name, desc=client_tl_desc, length=client_tl_length, data=client_tl_data)

    def top_level(self):
        return self.tl

    def load(self, encrypt_data):
        if ci.process_exists('Geometry Dash.exe'):
            return False
        for i in range(len(self.root[0][1][3])):
            if root[0][1][3][i].text == 'k4':
                root[0][1][3][i + 1].text = encrypt_data
        gs_encrypt(EleTree.tostring(self.root, encoding='utf-8', method='xml'))
        return True

    def save(self):
        return self.top_level().data
