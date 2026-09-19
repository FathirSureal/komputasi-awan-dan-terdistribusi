# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** Kelompok 4

| Nama | NIM | Kontribusi |
|---|---|---|
| Fathir Al Farih | 103072400002 | Network is always reliable & Masalah desain sistem - Arsitektur Monolitik |
| Muhammad Kelvin Firmansyah | 103072400096 | Latency is Zero & Masalah desain sistem - Arsitektur Monolitik |

## Pitfall 1: Latency is Zero — ditulis oleh Muhammad Kelvin Firmansyah

**Bukti di skenario:** "tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu)...".

**Kenapa ini keliru:** Asumsi bahwa komunikasi antar service itu instan (latency nol) membuat developer tidak berpikir skenario "bagaimana jika lawan bicara lambat merespons". Padahal latency itu nyata dan bisa melonjak drastis saat beban tinggi, service pembayaran yang biasanya cepat bisa menjadi sangat lambat saat load spike.

**Dampak ke FoodGo:** Modul pesanan memanggil modul pembayaran secara sinkron dan menunggu tanpa batas waktu. Saat trafik naik (jam makan siang/promo), modul pembayaran melambat, bukan mati, tetapi karena tidak ada timeout, setiap request yang kena antre di sana tetap menahan satu slot thread/koneksi di modul pesanan tanpa batas. Jika ini terjadi berkali-kali secara bersamaan, seluruh pool thread/koneksi modul pesanan habis dipakai untuk menunggu, akibatnya server menjadi tidak bisa menerima request baru, dan berujung crash total atau perlu restart manual, persis gejala yang dilaporkan tim engineering FoodGo.

**Solusi desain awal:** Set timeout yang jelas di semua pemanggilan antar service, ditambah circuit breaker: jika modul pembayaran sudah terlihat melambat/gagal berkali-kali secara beruntun, circuit breaker akan "membuka" (menghentikan pengiriman request baru sementara, fail fast) daripada terus menunggu dan ikut menghabiskan resource modul pesanan. Setelah jeda waktu tertentu, circuit breaker mencoba lagi (half-open); jika modul pembayaran sudah pulih, kirim request normal kembali; jika masih bermasalah, tutup kembali akses sementara.

**Trade-off:** Timeout yang terlalu pendek bisa membuat request yang sebenarnya masih valid (hanya agak lambat, belum tentu gagal) malah dianggap gagal, user experience terlihat lebih sering error padahal transaksinya sebenarnya bisa sukses jika diberi waktu sedikit lebih lama. Sebaliknya, timeout yang terlalu panjang tidak banyak membantu karena resource tetap tertahan lama. Nilai timeout perlu disesuaikan (tuning) berdasarkan data respons aktual modul pembayaran, bukan angka sembarang.

---

## Pitfall 2: "Network is always reliable" — ditulis oleh Fathir Al Farih
 
**Bukti di skenario:** "Tim menemukan bahwa kode mereka menulis asumsi seperti # network is always reliable, no need for retry...".

**Kenapa ini keliru:** Asumsi "the network is always reliable" merupakan salah satu pitfall dalam pengembangan sistem terdistribusi. Kesalahan ini terjadi ketika seorang programmer merancang komunikasi antar-service dengan asumsi bahwa lingkungan jaringan bersifat stabil dan terkendali sepenuhnya, tanpa mempertimbangkan karakteristik jaringan yang sesungguhnya (in real life condition).

Dalam kondisi nyata, kegagalan jaringan adalah sesuatu yang pasti akan terjadi pada skala dan kondisi tertentu. Bentuk kegagalan tersebut dapat berupa terputusnya koneksi, hilangnya sebagian paket data (packet loss), ketidaktersediaan server tujuan (server down), maupun keterlambatan respons akibat kepadatan lalu lintas data. Menganggap komunikasi antar-service akan selalu berhasil sama saja dengan mengasumsikan bahwa kendaraan tidak akan pernah mengalami gangguan teknis selama perjalanan, yakni sebuah asumsi yang tidak realistis dan tidak dapat dijadikan dasar perancangan sistem yang andal.

Implikasi praktikal dari asumsi ini adalah minimnya mekanisme penanganan kegagalan dalam kode, seperti tidak adanya fitur retry saat komunikasi antar-service gagal. Membuat sistem menjadi rapuh (fragile) terhadap gangguan jaringan sekecil apa pun, dan kegagalan pada satu komponen berpotensi menjalar serta memengaruhi keseluruhan sistem.

**Dampak ke FoodGo:** Salah satu dampak ke sistem FoodGo adalah, request gagal total meski gangguannya hanya berlangsung dalam waktu yang sangat singkat. Karena tidak ada fitur retry, transaksi user dianggap gagal meskipun sebenarnya bisa berhasil jika dicoba ulang sesaat kemudian. User harus mengulang proses checkout dari awal, menciptakan pengalaman buruk dan memiliki potensi kehilangan pelanggan.

**Solusi desain awal:** Penambahan fitur retry pada sistem FoodGo.

**Trade-off:** - Fitur retry. Sisi postif : menyelesaikan masalah kegagalan total ketika terjadi network error dan memberikan fitur "quality of life" untuk user, mengurangi pengalaman buruk ketika menggunakan sistem bagi user. Sisi negatifnya : bila terjadi banyak kegagalan secara bersamaan dan retry terus-menerus dapat membebani server dengan request berulang.

--- 
## Pitfall 3: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
