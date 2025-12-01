class Soal:
    def __init__(self, bentuk, warna, warna_name):
        self.bentuk = bentuk
        self.warna = warna          
        self.warna_name = warna_name  

    @property
    def jawaban_benar(self):
        return (self.bentuk, self.warna_name)
    
    def __str__(self):
        return f"{self.bentuk} {self.warna_name}"