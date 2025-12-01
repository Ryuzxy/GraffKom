def cek_jawaban(pilihan, soal):
    """Cek apakah jawaban benar"""
    return pilihan == soal.jawaban_benar


def hitung_skor(waktu_sisa, level, streak):
    """Hitung skor berdasarkan berbagai faktor"""
    base_score = level["poin"]
    time_bonus = max(0, int(waktu_sisa * 0.5))
    streak_bonus = streak * 2 if streak > 0 else 0

    total = base_score + time_bonus + streak_bonus
    return total