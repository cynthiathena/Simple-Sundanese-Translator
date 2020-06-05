import nltk
import re

#mengembalikan array of array of dictionary
def translate_dict(filename): 
    my_dict = [[dict() for i in range (26)] for j in range (4)]

    f = open(filename, "r")
    idx = 0
    for x in f:
        idx += 1
        key = ""
        value = ""
        samadengan = False 
        for i in range(len(x.strip())) :
            if x[i] == " " :
                if x[i+1] == "=" or x[i-1] == "=":
                    continue
            elif x[i] == "=" :
                samadengan = True
                continue
            
            if (not samadengan):
                key+=x[i]
            else :
                value+=x[i]

        #jumlah kata dari key
        length = len(nltk.tokenize.word_tokenize(key)) - 1
        if key in my_dict[length][ord(x.strip()[0])-97] :
            #semua kata ada di index yang berdasarkan abjad, dan berdasarkan jumlah kata
            my_dict[length][ord(x.strip()[0])-97][key].append(value)
        else :
            my_dict[length][ord(x.strip()[0])-97].setdefault(key,[])
            my_dict[length][ord(x.strip()[0])-97][key].append(value)

    return my_dict

def translate_words(dictionary, kalimat, tipe, algoritma) :

    #menambahkan "teh"
    if tipe == "Bahasa Indonesia" :
        if "saya" in kalimat :
            idx = kalimat.index("saya")
            if (idx != len(kalimat)-1) :
                kalimat = kalimat[:(idx+1)] + ["teh"] + kalimat[(idx+1):]
        if "kamu" in kalimat :
            idx = kalimat.index("kamu")
            if (idx != len(kalimat)-1) :
                kalimat = kalimat[:(idx+1)] + ["teh"] + kalimat[(idx+1):]
        if "dia" in kalimat :
            idx = kalimat.index("dia")
            if (idx != len(kalimat)-1) :
                kalimat = kalimat[:(idx+1)] + ["teh"] + kalimat[(idx+1):]

    kalimat_hasil = []

    # mencari hasil translate
    i = 0
    while i < len(kalimat) : 
        kata_search = ""
        found = False
        awal = sameCase(kalimat[i][0])

        if ord(awal) >= 97 and ord(awal) <= 122 :
            #dicari dari kata yang berjumlah 4
            panjang_kata = 4

            while (not found) and (panjang_kata > 0) :
                kata_search = ""
                for count in range (panjang_kata) :
                    if (i+count) < len(kalimat):
                        idx = i+count
                        kata_search += sameCase(kalimat[idx])
                        if count != panjang_kata - 1 :
                            kata_search += " "
                for j in dictionary[panjang_kata-1][ord(awal) - 97] :
                    if algoritma == 'kmp' :
                        if (kmp(kata_search,j) != -1) and kmp(j,kata_search) != -1 and not found:
                            kalimat_hasil.append(dictionary[panjang_kata-1][ord(awal) - 97][j][0])
                            found = True 
                            break 
                    elif algoritma == 'bm' :
                        if (bm(kata_search,j) != -1) and bm(j,kata_search) != -1 and not found:
                            kalimat_hasil.append(dictionary[panjang_kata-1][ord(awal) - 97][j][0])
                            found = True 
                            break
                    elif algoritma == 'regex' :
                        if (regex(kata_search,j) != -1) and regex(j,kata_search) != -1 and not found:
                            kalimat_hasil.append(dictionary[panjang_kata-1][ord(awal) - 97][j][0])
                            found = True 
                            break
                if not found :
                    panjang_kata -= 1

            # jika tidak ketemu yang sama, maka masukkan kata asli
            if (not found) :
                kalimat_hasil.append(kalimat[i])
                i+=1
            else :
                i += panjang_kata
        else :
            kalimat_hasil.append(kalimat[i])
            i+=1

    # meghapus "teh" dari bahasa sunda-bahasa indonesia
    if tipe == "Bahasa Sunda" :
        for kata in kalimat_hasil :
            if sameCase(kata) == "teh" :
                kalimat_hasil.remove(kata)

    return kalimat_hasil

#FUNGSI ALGORITMA
#KMP
def borderFunc(pattern) :
    temp = [0 for i in range (len(pattern))]

    i = 0
    j = 1
    size = len(pattern)

    while (j<size) :
        #jjika terjadi mismatch
        if (pattern[i] != pattern[j]) : 
            #jika i pada tengah pattern, maka i akan kembali mengecek dengan 
            #indeks adalah nilai pada karakter sebelumnya
            if (i > 0) : 
                i = temp[i-1]
            #jika i pada awal pattern, maka lanjutkan j 
            else :
                j+=1
        #jika match
        else : 
            #nilai dari karakter pada j adalah i ditambah 1
            temp[j] = i+1
            i+=1
            j+=1
    return temp

def kmp(text, pattern) :
    i = 0
    j = 0
    size_text = len(text)
    size_pattern = len(pattern) 
    b = borderFunc(pattern)

    found = False
    result = -1
    while (i < size_text) and (not found):
        if (text[i] == pattern[j]) :
            if (j == size_pattern - 1) :
                result = i - size_pattern + 1
                found = True
            i+=1
            j+=1
        elif (j > 0) : #jika terjadi mismatch
            j = b[j-1]
        else : #j == 0
            i += 1
    
    return result
    
#fungsi last occurence
def lo(pattern) :
    #membuat array untuk semua alphabet
    lastOccur = [-1 for i in range(128)]

    idx = len(pattern) - 1
    while (idx >= 0) :
        #jika alphabet muncul pada pattern
        if lastOccur[ord(pattern[idx])] == -1 :
            lastOccur[ord(pattern[idx])] = idx
        idx -= 1
    return lastOccur 

#algoritma boyer moore   
def bm(text, pattern) :
    size_text = len(text)
    size_pattern = len(pattern)

    i = size_pattern - 1
    
    last = lo(pattern)
    res = -1
    found = False
    if (size_text >= size_pattern) :
        j = i
        while (i < size_text) and (not found) :
            if pattern[j] == text[i] : #match
                #match hingga awal karakter pada pattern
                if (j == 0) :
                    res = i
                    found = True
                #match belum sampai akhir
                else :
                    j-=1 
                    i-=1
            else : #terjadi mismatch, character jump technique
                #kasus pertama (saat last occurence ada di kiri j) 
                #kasus ketiga saat tidak ada pada pattern sehingga last = -1
                if (last[ord(text[i])] < j) :
                    i = i + size_pattern - (last[ord(text[i])] + 1)
                #kasus kedua 
                elif (last[ord(text[i])] > j) :
                    i = i + size_pattern - j
                j = size_pattern - 1
        
    return res

#REGEX
def regex(text,pattern) :
    #array untuk kata yang match
    x = re.findall(pattern, text) 

    if (len(x) == 0) : #jika terjadi mismatch
        return -1
    else :
        return 0   

#menganggap semua karakter merupakan huruf kecil
def sameCase(inp) :
    res = ""
    for i in range (len(inp)) :
        res = res + inp[i].lower()
    return res

#mengembalikan string dari hasil terjemahan
def run(tipe, inp, algoritma) :

    dict_indo = translate_dict("indonesia.txt")
    dict_sunda = translate_dict("sunda.txt")
    kalimat = nltk.tokenize.word_tokenize(inp) #array untuk kalimat input dipisahkan berdasarkan spasi

    res = [] #array hasil terjemahan
    if tipe == "Bahasa Sunda" :
        res = translate_words(dict_sunda, kalimat, tipe, algoritma)
    elif tipe == "Bahasa Indonesia" :
        res = translate_words(dict_indo, kalimat, tipe, algoritma)

    result = ""
    for k in res :
        result += k
        result += " "

    return result