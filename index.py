import index

# Database Kamus Sederhana Bahasa Bugis (10 kata sesuai soal)
KAMUS = {
    "manre": "makan",
    "tindro": "tidur",
    "monro": "tinggal",
    "magai": "kenapa",
    "madekka": "haus",
    "micai": "marah",
    "micawa": "ketawa",
    "massuro": "menyuruh",
    "madakka": "haus",
    "rempe": "lempar"
}

# Parameter Algoritma Genetika
UKURAN_POPULASI = 6
PROBABILITAS_CROSSOVER = 0.8
PROBABILITAS_MUTASI = 0.1
ALFABET = "abcdefghijklmnopqrstuvwxyz"

# Variabel Global (State Program)
populasi = []
fitness_scores = []
probabilitas_seleksi = []
interval_roulette = []
parents = []
offspring_crossover = []
offspring_mutasi = []
generasi_baru = []
target_kata = ""

def inisialisasi_populasi(target, ukuran=6):
    global populasi, target_kata
    target_kata = target.strip().lower()
    panjang = len(target_kata)
    
    if panjang == 0:
        return []
        
    populasi = []
    for _ in range(ukuran):
        # Membangkitkan kromosom acak sepanjang target kata
        individu = "".join(random.choice(ALFABET) for _ in range(panjang))
        populasi.append(individu)
    return populasi

def hitung_fitness():
    global fitness_scores
    fitness_scores = []
    panjang = len(target_kata)
    
    if panjang == 0:
        return []
        
    for individu in populasi:
        cocok = sum(1 for i in range(panjang) if i < len(individu) and individu[i] == target_kata[i])
        score = cocok / panjang
        fitness_scores.append(score)
    return fitness_scores

def seleksi_roulette():
    global probabilitas_seleksi, interval_roulette, parents
    parents = []
    
    if not fitness_scores:
        return []
        
    total_fitness = sum(fitness_scores)
    
    # Menghindari pembagian dengan nol jika semua fitness awal bernilai 0
    if total_fitness == 0:
        probabilitas_seleksi = [1 / len(populasi)] * len(populasi)
    else:
        probabilitas_seleksi = [f / total_fitness for f in fitness_scores]
    
    interval_roulette = []
    kumulatif = 0.0
    for p in probabilitas_seleksi:
        awal = kumulatif
        kumulatif += p
        interval_roulette.append((awal, kumulatif))
        
    for _ in range(len(populasi)):
        r = random.random()
        for idx, (awal, akhir) in enumerate(interval_roulette):
            if awal <= r <= akhir:
                parents.append(populasi[idx])
                break
        if len(parents) <= _: # Fallback safeguard
            parents.append(random.choice(populasi))
            
    return parents

def crossover():
    global offspring_crossover
    offspring_crossover = []
    panjang = len(target_kata)
    
    if not parents:
        return []
        
    for i in range(0, len(parents), 2):
        p1 = parents[i]
        p2 = parents[i+1] if i+1 < len(parents) else parents[0]
        
        if random.random() < PROBABILITAS_CROSSOVER and panjang > 1:
            titik_potong = random.randint(1, panjang - 1)
            c1 = p1[:titik_potong] + p2[titik_potong:]
            c2 = p2[:titik_potong] + p1[titik_potong:]
        else:
            c1, c2 = p1, p2
        offspring_crossover.extend([c1, c2])
        
    offspring_crossover = offspring_crossover[:len(populasi)]
    return offspring_crossover

def mutasi():
    global offspring_mutasi
    offspring_mutasi = []
    
    if not offspring_crossover:
        return []
        
    for individu in offspring_crossover:
        list_ind = list(individu)
        for i in range(len(list_ind)):
            if random.random() < PROBABILITAS_MUTASI:
                list_ind[i] = random.choice(ALFABET)
        offspring_mutasi.append("".join(list_ind))
    return offspring_mutasi

def main():
    global generasi_baru
    while True:
        print("\n==================================")
        print("=== KAMUS BAHASA DAERAH BUGIS ===")
        print("==================================")
        print("1. Tampilkan Kamus")
        print("2. Cari Kata")
        print("3. Jalankan Algoritma Genetika")
        print("4. Tampilkan Populasi")
        print("5. Hasil Fitness")
        print("6. Seleksi Roulette")
        print("7. Cross Over")
        print("8. Mutasi")
        print("9. Generasi Baru")
        print("10. Keluar")
        print("==================================")
        
        pilihan = input("Pilih menu (1-10): ").strip()
        
        if pilihan == "1":
            print("\n>>> DAFTAR KAMUS BAHASA BUGIS <<<")
            for idx, (kata, arti) in enumerate(KAMUS.items(), 1):
                print(f"{idx}. {kata:<10} = {arti}")
                
        elif pilihan == "2":
            print("\n>>> CARI KATA <<<")
            cari = input("Masukkan kata Bahasa Bugis: ").strip().lower()
            if cari in KAMUS:
                print(f"Hasil: '{cari}' berarti '{KAMUS[cari]}'")
            else:
                print("[!] Kata tidak ditemukan dalam database.")
                
        elif pilihan == "3":
            print("\n>>> JALANKAN ALGORITMA GENETIKA <<<")
            target = input("Masukkan kata target dari kamus: ").strip().lower()
            
            if not target:
                print("[!] Kata target tidak boleh kosong!")
                continue
                
            # Proses Eksekusi Berurutan Otomatis secara aman
            inisialisasi_populasi(target, UKURAN_POPULASI)
            hitung_fitness()
            seleksi_roulette()
            crossover()
            mutasi()
            generasi_baru = list(offspring_mutasi)
            
            print(f"\n[SUKSES] Generasi 1 Berhasil Diproses untuk kata '{target.upper()}'!")
            print("Sekarang Anda bisa menekan Menu 4 sampai 9 untuk melihat hasilnya.")
            
        elif pilihan == "4":
            if not populasi:
                print("\n[!] PERINGATAN: Silakan jalankan Menu 3 terlebih dahulu untuk membuat populasi!")
            else:
                print("\n>>> POPULASI AWAL GENERASI 1 <<<")
                for i, ind in enumerate(populasi, 1):
                    print(f"Individu {i}: {ind}")
                    
        elif pilihan == "5":
            if not fitness_scores:
                print("\n[!] PERINGATAN: Silakan jalankan Menu 3 terlebih dahulu!")
            else:
                print("\n>>> HASIL EVALUASI FITNESS <<<")
                print(f"Target Kata: {target_kata.upper()} (Panjang: {len(target_kata)} Gen)")
                for i, (ind, fit) in enumerate(zip(populasi, fitness_scores), 1):
                    print(f"Individu {i}: {ind:<6} -> Nilai Fitness: {fit:.2f}")
                    
        elif pilihan == "6":
            if not parents:
                print("\n[!] PERINGATAN: Silakan jalankan Menu 3 terlebih dahulu!")
            else:
                print("\n>>> SELEKSI ROULETTE WHEEL <<<")
                print(f"{'ID':<4} | {'Kromosom':<8} | {'Fitness':<7} | {'Probabilitas':<12} | {'Interval Kumulatif'}")
                print("-" * 60)
                for i, (ind, fit, prob, inter) in enumerate(zip(populasi, fitness_scores, probabilitas_seleksi, interval_roulette), 1):
                    print(f"I{i:<2} | {ind:<8} | {fit:<7.2f} | {prob:<12.4f} | {inter[0]:.2f} - {inter[1]:.2f}")
                print("\n>>> Hasil Orang Tua Terpilih (Parents):")
                for i, p in enumerate(parents, 1):
                    print(f"Parent {i}: {p}")
                    
        elif pilihan == "7":
            if not offspring_crossover:
                print("\n[!] PERINGATAN: Silakan jalankan Menu 3 terlebih dahulu!")
            else:
                print("\n>>> HASIL OPERATOR CROSSOVER (PINDAH SILANG) <<<")
                print(f"Probabilitas Crossover: {PROBABILITAS_CROSSOVER}")
                for i in range(0, len(parents), 2):
                    p1 = parents[i]
                    p2 = parents[i+1] if i+1 < len(parents) else parents[0]
                    c1 = offspring_crossover[i]
                    c2 = offspring_crossover[i+1] if i+1 < len(offspring_crossover) else offspring_crossover[0]
                    print(f"Pasangan {i//2 + 1}: {p1} x {p2} -> Anak 1: {c1} | Anak 2: {c2}")
                    
        elif pilihan == "8":
            if not offspring_mutasi:
                print("\n[!] PERINGATAN: Silakan jalankan Menu 3 terlebih dahulu!")
            else:
                print("\n>>> HASIL OPERATOR MUTASI <<<")
                print(f"Probabilitas Mutasi Gen: {PROBABILITAS_MUTASI}")
                for i, (sebelum, sesudah) in enumerate(zip(offspring_crossover, offspring_mutasi), 1):
                    print(f"Anak {i}: {sebelum} -> Sesudah Mutasi: {sesudah}")
                    
        elif pilihan == "9":
            if not generasi_baru:
                print("\n[!] PERINGATAN: Silakan jalankan Menu 3 terlebih dahulu!")
            else:
                print("\n>>> POPULASI GENERASI BARU (AKHIR SIKLUS GEN-1) <<<")
                for i, ind in enumerate(generasi_baru, 1):
                    print(f"Individu Baru {i}: {ind}")
                    
        elif pilihan == "10":
            print("\nProgram Keluar. Terima kasih!")
            break
        else:
            print("\n[!] Pilihan tidak valid. Ketik angka 1 sampai 10.")

if __name__ == '__main__':
    main()