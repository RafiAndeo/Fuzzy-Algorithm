import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#membership function
kriteriaHarga = {
    'mahal'   : [6.00, 8.00, 10.00, 10.00 ], 
    'sedang'   : [ 3.00, 5.00, 6.00, 7.00 ], 
    'murah'   : [ 0.00,  0.00, 3.00, 5.00 ], 
}

kriteriaServis = {
    'baik'   : [ 60.00, 80.00, 100.00, 100.00],
    'menengah'   : [ 20.00,  55.00,  55.00, 80.00],
    'buruk'   : [ 00.00,  00.00,  25.00,  45.00],
}

kelayakan = {'layak':70, 'tidaklayak':30, 'kuranglayak':50}

#function inferensi
aturan = {
    ('mahal', 'baik') : 'kuranglayak',
    ('mahal', 'menengah') : 'tidaklayak',
    ('mahal', 'buruk') : 'tidaklayak',
    ('sedang', 'baik') : 'layak',
    ('sedang', 'menengah') : 'kuranglayak',
    ('sedang', 'buruk') : 'tidaklayak',
    ('murah', 'baik') : 'layak',
    ('murah', 'menengah') : 'layak',
    ('murah', 'buruk') : 'tidaklayak'
}

def inference(bil, aturan):
    h = {}
    for i, j in bil[0].items():
        for o, p in bil[1].items():
            a = (i, o)
            minimal = min(j, p)
            hasil = h.get(aturan[a], 0)
            h[aturan[a]] = max(minimal, hasil)
    return h

#function fuzzyfikasi
def count(bil, batas):
    if bil < batas[0] or bil > batas[3]:
        return 0
    elif bil >= batas[1] and bil <= batas[2]:
        return 1
    elif bil >= batas[0] and bil < batas[1]:
        return (bil - batas[0]) / (batas[1] - batas[0])
    elif bil >= batas[2] and bil < batas[3]: 
        return -1 * (bil - batas[3]) / (batas[3] - batas[2])
    return 0

def membershipCount(bil, membership):
    h = {}
    for i in membership:
        h[i] = count(bil, membership[i])
    return h

def fuzzyfication(bil, listMembership):
    h = []
    for i in range(len(listMembership)):
        h.append(membershipCount(bil[i], listMembership[i]))
    return h

#function defuzzifikasi
def defuzzification(bil, membership):
    x = 0
    y = 0.000000001
    for i in membership:
        x = x + bil[i] * membership[i]
        y = y + bil[i]
        output = x/y
    return output

#function membaca data dari file
df = pd.read_excel('bengkel.xlsx')
id = df['id'].values.tolist()
df = df[['harga', 'servis']]
data = df.values
data_servis = df['servis'].values.tolist()
data_harga = df['harga'].values.tolist()

#program utama
nilai = []
for i in data:
    bil_fuzzyfication = fuzzyfication(i, [kriteriaHarga, kriteriaServis])
    bil_inference = inference(bil_fuzzyfication, aturan)
    bil_defuzzification = defuzzification(bil_inference, kelayakan)
    nilai.append(bil_defuzzification)

defuzAkhir = []
id = []
servis = []
harga = []
for p in range(len(nilai)):
    if len(defuzAkhir) < 10:
        if np.any(data_servis[p] > 80):
            defuzAkhir.append(nilai[p])
            servis.append(data_servis[p])
            harga.append(data_harga[p])
            id.append(p + 1)
    else:
        q = 0
        minimal = 0
        while q < len(defuzAkhir):
            if np.any(defuzAkhir[q] < defuzAkhir[minimal]):
                minimal = q
            q = q + 1
        if np.any(defuzAkhir[minimal] < nilai[p]):
            defuzAkhir[minimal] = nilai[p]
            id[minimal] = p + 1
id.sort()

#function gambar membership function
def plot_linguistik(batas, warna, label = '', min = 0, max = 1):
    nilai = [0, 1, 1, 0]
    plt.plot( (min, batas[0]), (0,0), warna )
    for i in range(len(batas)-1):
        plt.plot((batas[i], batas[i + 1]), (nilai[i], nilai[i + 1]), warna)
    plt.plot((batas[-1], max), (0,0), warna, label = label)

def plot_membership( membership, min=0, max=1):
    warna = ['k', 'm', 'c', 'c', 'm', 'y', 'k'] 
    i=0
    for l in membership :
        plot_linguistik(membership[l], warna[i], l, min = min, max = max)
        i = i + 1
    plt.legend(loc = 3)
    plt.show()

plot_membership(kriteriaHarga)
plot_membership(kriteriaServis)

Peringkat = pd.DataFrame(defuzAkhir, id, columns=['Output Defuzzification'])
Peringkat.to_excel('Peringkat.xlsx')