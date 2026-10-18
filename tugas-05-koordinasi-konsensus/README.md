# Tugas 5 (Pekan 5) — Koordinasi & Konsensus

**Materi terkait:** Physical/Logical Clock, Election Algorithm (Bully/Raft).

## Studi Kasus

Terjadi konflik urutan waktu pada pesanan FoodGo (dua server mencatat urutan pesanan berbeda karena jam tidak sinkron), dan sistem membutuhkan satu **"Node Leader"** untuk mengelola antrean pesanan pusat agar tidak terjadi konflik pemrosesan ganda.

## Tugas Kelompok

Implementasikan simulasi **Bully Algorithm** untuk memilih leader di antara **5 node virtual** yang berjalan sebagai 5 proses Python terpisah di laptop yang sama (tiap node = satu proses di port berbeda, komunikasi lewat TCP socket di `localhost`).

Skeleton yang disediakan (`src/node.py`) sudah menangani bagian **infrastruktur jaringan** (membuka socket, menerima & mengirim pesan antar node) — bagian **algoritma Bully sendiri sengaja dikosongkan** (`# TODO`), karena itu inti pembelajaran tugas ini.

### Aturan Bully Algorithm yang harus diimplementasikan

1. Node yang mendeteksi leader tidak merespons (atau saat start pertama kali) mengirim pesan `ELECTION` ke semua node dengan ID **lebih besar** darinya.
2. Jika ada node ber-ID lebih besar yang merespons `OK`, node yang memulai election **berhenti mencalonkan diri** dan menunggu pesan `COORDINATOR`.
3. Jika **tidak ada** node ber-ID lebih besar yang merespons dalam batas waktu tertentu, node tersebut menjadi leader dan mem-broadcast `COORDINATOR` ke semua node lain.
4. Semua node mencatat siapa leader saat ini.

### Cara Menjalankan

Buka 5 terminal terpisah (satu per node):
```bash
python3 src/node.py --id 1 --port 5001 --peers 5002,5003,5004,5005
python3 src/node.py --id 2 --port 5002 --peers 5001,5003,5004,5005
python3 src/node.py --id 3 --port 5003 --peers 5001,5002,5004,5005
python3 src/node.py --id 4 --port 5004 --peers 5001,5002,5003,5005
python3 src/node.py --id 5 --port 5005 --peers 5001,5002,5003,5004
```

### Skenario Wajib Diuji & Dicatat

1. **Start normal**: nyalakan node 1–5 hampir bersamaan, catat siapa yang terpilih jadi leader (harusnya node ber-ID tertinggi, yaitu node 5).
2. **Leader mati**: matikan (Ctrl+C) proses node leader (node 5), amati node lain mendeteksi leader hilang dan memicu election baru. Catat leader baru yang terpilih (harusnya node 4).
3. Simpan log terminal (screenshot atau `> log_nodeX.txt` redirect) dari kedua skenario ke folder `bukti/`.

## Analisis Hasil Pengujian

| Skenario | Leader terpilih | Sesuai harapan | Waktu sampai leader baru |
|---|---|---|---|
| 1. Start normal (node 1-5 hampir bersamaan) | Node 5 | Ya (menurut node 1-4) | - |
| 2. Leader (node 5) dimatikan | Node 4 | Ya | sekitar 2-5 detik (estimasi dari parameter kode) |

Hasil kedua skenario sesuai prinsip Bully Algorithm: leader selalu node ber-ID tertinggi yang masih hidup.

### Skenario 1: Start normal

**Mengapa node 1, 2, dan 3 sempat menjadi leader sementara?**

Setiap node menunggu 1 detik setelah start, lalu menjalankan `start_election()`. Karena node tidak start tepat bersamaan, node ber-ID lebih tinggi sering belum membuka port saat ELECTION dikirim, sehingga `send_message` gagal (koneksi ditolak). Dari sudut pandang node pengirim, semua node yang lebih tinggi sedang mati. Tidak ada `OK` dalam `ELECTION_TIMEOUT` (2 detik), maka sesuai aturan 3 node tersebut menyatakan diri leader dan mem-broadcast `COORDINATOR`.

**Mengapa akhirnya node 5 yang menang?**
- Node 4 mengirim ELECTION ke node 5 yang sudah hidup, menerima `OK`, lalu berhenti mencalonkan diri (aturan 2).
- Node 5 tidak punya peer ber-ID lebih tinggi, sehingga tidak ada `OK` yang masuk. Setelah timeout 2 detik, node 5 menjadi leader dan mem-broadcast `COORDINATOR` ke semua peer (aturan 3).
- Pada node 1-4, `COORDINATOR` dari node 5 menimpa catatan leader sebelumnya, sehingga semuanya mencatat "Leader sekarang: node 5".

**Catatan : leader di node 5 tidak konsisten.**
Pada log node 5, catatan leader terakhir adalah node 3. `COORDINATOR` dari node 3 (yang sempat jadi leader sementara) datang terlambat, setelah node 5 mengumumkan dirinya, dan menimpa `leader_id` node 5. Kondisi ini tidak pulih sendiri: `monitor_leader` di node 5 hanya mengecek PING ke node 3, dan karena node 3 masih hidup, node 5 tidak memicu election baru. Jadi aturan 4 ("semua node mencatat siapa leader saat ini") belum terpenuhi sepenuhnya: node 1-4 menganggap node 5 leader, sedangkan node 5 menganggap node 3 leader (Keterbatasan).

### Skenario 2: Leader dimatikan

Urutan kejadian setelah node 5 dimatikan (`Ctrl+C`):

1. **Deteksi.** Tiap node menjalankan `monitor_leader` dengan interval 3 detik. PING ke node 5 gagal karena koneksi ditolak. Karena siklus monitor tiap node tidak sinkron, node yang pertama mendeteksi memicu election, sehingga deteksi memakan 0-3 detik.
2. **Election.** Node yang mendeteksi mengirim ELECTION ke node yang lebih tinggi. Node 1-3 akan mendapat `OK` dari node lebih tinggi yang masih hidup, lalu node tersebut membalas `OK` dan menjalankan election sendiri, berantai sampai node 4.
3. **Node 4 menang.** ELECTION dari node 4 ke node 5 gagal dan tidak ada `OK` dalam 2 detik. Node 4 menyatakan diri leader dan mem-broadcast `COORDINATOR`.
4. **Konvergensi.** Node 1-3 mencatat "Leader sekarang: node 4".

Estimasi total: deteksi (0-3 detik) ditambah `ELECTION_TIMEOUT` (2 detik), yaitu sekitar 2-5 detik. Angka ini diturunkan dari parameter kode, bukan hasil pengukuran.
### Kesimpulan

- Bully Algorithm berhasil memilih node ber-ID tertinggi yang hidup sebagai leader, baik saat start awal maupun setelah leader gagal.
- Untuk kasus FoodGo, satu leader yang mengelola antrean pesanan pusat bisa digantikan otomatis dalam hitungan detik tanpa campur tangan manual, sehingga antrean tidak berhenti lama saat leader mati.

### Keterbatasan 

1. **`COORDINATOR` dari node ber-ID lebih rendah bisa menimpa leader yang benar** (temuan pada Skenario 1). Untuk FoodGo ini agak berisiko, karena dua node bisa sama-sama merasa tahu siapa leader-nya dengan jawaban berbeda, padahal tujuan sistem adalah mencegah pemrosesan ganda.
2. **Election bisa berjalan bersamaan dalam satu node** (misalnya saat banyak node mendeteksi leader mati sekaligus), padahal `ok_event` dipakai bersama. Secara teori ini bisa membuat sebuah node sempat mengumumkan diri leader walau ada node lebih tinggi yang hidup. Pada pengujian ini hal tersebut tidak dicatat sebagai masalah.

## Struktur Submission

```
tugas-05-koordinasi-konsensus/
├── README.md      # Analisis: kenapa perlu leader, kenapa Bully (vs Raft), hasil 2 skenario
├── JURNAL.md
├── src/
│   └── node.py
└── bukti/          # Log/screenshot skenario start normal & leader mati
```

## Rubrik Penilaian (Tugas 5)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Implementasi Bully Algorithm benar | 35% | Election, OK, COORDINATOR message bekerja sesuai aturan algoritma |
| Bukti skenario leader mati → re-election | 30% | Log jelas menunjukkan leader baru terpilih otomatis |
| Analisis (kenapa perlu leader, trade-off Bully vs Raft) | 20% | Dikaitkan ke masalah urutan pesanan di skenario FoodGo |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI tentang gambaran umum algoritma election; **tidak boleh** meminta AI menuliskan isi `# TODO` di `src/node.py` (logika `on_message`, `start_election`, `declare_leader`, `monitor_leader`). Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- `README.md` wajib menjelaskan kenapa Bully Algorithm selalu memilih node ber-ID tertinggi yang masih hidup, dan apa kelemahannya dibanding algoritma lain (mis. jumlah pesan yang dikirim saat election, single point of failure sebelum leader baru terpilih) — bukan sekadar definisi generik.
