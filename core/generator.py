import random
from .soal import Soal

def generate_soal(bentuk_list, warna_list):
    """Generate soal baru dengan validasi"""
    if not bentuk_list or not warna_list:
        raise ValueError("bentuk_list atau warna_list kosong!")
    
    bentuk = random.choice(bentuk_list)
    warna_name, warna_rgb = random.choice(list(warna_list.items()))
    
    soal = Soal(bentuk, warna_rgb, warna_name)
    print(f"DEBUG: Generated soal - Bentuk: {bentuk}, Warna: {warna_name}")
    return soal

def generate_opsi(soal, bentuk_list, warna_list, jumlah=4):
    """Generate opsi jawaban (termasuk jawaban benar)"""
    if not soal or not bentuk_list or not warna_list:
        raise ValueError("Invalid parameters untuk generate_opsi")
    
    opsi = [soal.jawaban_benar]
    attempts = 0
    max_attempts = 100
    
    while len(opsi) < jumlah and attempts < max_attempts:
        b = random.choice(bentuk_list)
        warna_name = random.choice(list(warna_list.keys()))
        kandidat = (b, warna_name)
        
        if kandidat not in opsi:
            opsi.append(kandidat)
        
        attempts += 1
    
    if len(opsi) < jumlah:
        print(f"Warning: Hanya bisa generate {len(opsi)} opsi dari {jumlah} yang diminta")
    
    random.shuffle(opsi)
    print(f"DEBUG: Generated {len(opsi)} options")
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