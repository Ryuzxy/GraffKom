import random
from .soal import Soal

def generate_soal(bentuk_list, warna_list):
    """Generate soal baru"""
    bentuk = random.choice(bentuk_list)
    warna_name, warna_rgb = random.choice(list(warna_list.items()))
    return Soal(bentuk, warna_rgb, warna_name)

def generate_opsi(soal, bentuk_list, warna_list, jumlah=4):
    """Generate opsi jawaban (termasuk jawaban benar)"""
    opsi = [soal.jawaban_benar]
    
    while len(opsi) < jumlah:
        b = random.choice(bentuk_list)
        warna_name = random.choice(list(warna_list.keys()))
        kandidat = (b, warna_name)
        
        if kandidat not in opsi:
            opsi.append(kandidat)
    
    random.shuffle(opsi)
    return opsi

def generate_for_level(level_config, bentuk_list, warna_list):
    """Generate soal berdasarkan level"""
    soal = generate_soal(bentuk_list, warna_list)
    opsi = generate_opsi(
        soal, 
        bentuk_list, 
        warna_list, 
        jumlah=level_config["opsi"]
    )
    return soal, opsi