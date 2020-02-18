

class Fuzzy:
    def __init__(self):
        super().__init__()

    def fuzzifikasi(self, paramA, paramB):
        """
        fuzzifikasi : pengubahan nilai dari parameter input kedalam himpunan fuzzy.
        """
        self.beat = paramA
        self.oks = paramB
        #membership rendah, Normal, Tinggi Hbeat
        if (self.beat<=90):
            self.Hlow = 1
            self.HNorm = 0
        if (self.beat>=90) and (self.beat<=130):
            self.Hlow = (130-self.beat)/40
            self.HNorm = (self.beat-90)/40
        if (self.beat>=130):
            self.Hlow = 0
        if (self.beat>=130) and (self.beat<=170):
            self.HNorm = (170-self.beat)/40
        if (self.beat<=130):
            self.HHigh = 0
        if (self.beat>=130) and (self.beat<=200):
            self.HHigh = (self.beat-130)/70
            self.HNorm = 0
        if (self.beat>=200):
            self.HHigh =1

        #membership rendah, tinggi Oksigen
        if (self.oks<=60):
            self.ORen = 1
            self.OTing =0
        if (self.oks>=60) and (self.oks<=100):
            self.ORen = (100-self.oks)/40
            self.OTing = (self.oks - 60)/40
        if (self.oks>=100):
            self.ORen = 0
            self.OTing =1
        self.Inferensi()

    def Inferensi(self):
        """
        inferensi digunakan untuk mencari nilai predikat yg nantinya akan digunakan untuk mencari output.
        digunakan fungsi min untuk mencari predikat dari masing-masing rule. selain itu p1, p2, dst. juga 
        menunjukkan rule yg digunakan rule 1 = p1 yaitu if detak jantung rendah dan SpO rendah then conseq[0]
        """
        p1 = min([self.Hlow, self.ORen])
        p2 = min([self.Hlow, self.OTing])
        p3 = min([self.HNorm, self.ORen])
        p4 = min([self.HNorm, self.OTing])
        p5 = min([self.HHigh, self.ORen])
        p6 = min([self.HHigh, self.OTing])
        self.predikat = [p1,p2,p3,p4,p5,p6]
        self.DFuzz()

    def DFuzz(self):
        """Rule Base dibuat dengan 3 keadaan yaitu Normal, perlu penanganan, dan Kritis dengan nilai masing-masing
        Normal: 30, perlu penanganan: 60, kritis: 100. conseq merupakan variable array dari nilai tiap-tiap rule 
        secara berurutan. conseq =[60,10,....] menandakan bahwa pada rule 1 then atau output bernilai 60 atau perlu
        penganan.
        """
        conseq = [60, 10, 60, 10, 10, 100]
        self.anteseden = 0
        self.sumant = 0
        for i in range(len(conseq)):
            self.anteseden += (self.predikat[i]*conseq[i])
            self.sumant += (self.predikat[i])
        outFuz = self.anteseden / self.sumant
        if (outFuz <= 30) :
            self.keputusan = 'Normal'
        elif(outFuz > 30)and(outFuz<=60):
            self.keputusan = 'Perlu Penanganan'
        elif(outFuz>60)and(outFuz<=100):
            self.keputusan = 'Kritis'
