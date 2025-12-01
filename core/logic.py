def cek_jawaban(pilihan, soal):
    """Cek apakah jawaban benar"""
    return pilihan == soal.jawaban_benar


def hitung_skor(waktu_sisa, level, streak):
    """Hitung skor berdasarkan berbagai faktor"""
    base_score = level["poin"]
    time_bonus = int(waktu_sisa * 0.5)
    streak_bonus = streak * 2
    return base_score + time_bonus + streak_bonus