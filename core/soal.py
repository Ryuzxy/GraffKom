class Soal:
    def __init__(self, bentuk, warna, warna_name):
        self.bentuk = bentuk
        self.warna = warna          # nilai RGB
        self.warna_name = warna_name  # nama warna (untuk jawaban)

    @property
    def jawaban_benar(self):
        return (self.bentuk, self.warna_name)
    
    def __str__(self):
        return f"{self.bentuk} {self.warna_name}"