class Otus():
    rotu:"Olio"
    sanoo: "Ärripurri"

    def otusSanoo(self):
        return self.sanoo

    def __repr__(self):
        return f"{self.rotu} ja sanon {self.sanoo}"

def listGoThrew(list):
    i = 1
    for sana in list:
        print(f"Minä olen {i}. paikalla listalla, olen {sana}")
        i = i + 1
    
def main():
    otus1 = Otus()
    otus1.rotu = "Kissa"
    otus1.sanoo = "Miau!"
    otus2 = Otus()
    otus2.rotu = "Koira"
    otus2.sanoo = "Hauhau, vufvuff!"
    lista = [otus1, otus2]
    listGoThrew(lista)

if __name__=="__main__":
    main()