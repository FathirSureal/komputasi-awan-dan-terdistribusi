# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** Kelompok 4

| Nama | NIM | Kontribusi |
|---|---|---|
| Fathir Al Farih | 103072400002 | Network is always reliable & Kesimpulan |
| Muhammad Kelvin Firmansyah | 103072400096 | Latency is Zero & Masalah desain sistem - Arsitektur Monolitik |

## Pitfall 1: Latency is Zero — ditulis oleh Muhammad Kelvin Firmansyah

**Bukti di skenario:** "tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu)...".

**Kenapa ini keliru:** Asumsi bahwa komunikasi antar service itu instan (latency nol) membuat developer tidak berpikir skenario "bagaimana jika lawan bicara lambat merespons". Padahal latency itu nyata dan bisa melonjak drastis saat beban tinggi, service pembayaran yang biasanya cepat bisa menjadi sangat lambat saat load spike.

**Dampak ke FoodGo:** Modul pesanan memanggil modul pembayaran secara sinkron dan menunggu tanpa batas waktu. Saat trafik naik (jam makan siang/promo), modul pembayaran melambat, bukan mati, tetapi karena tidak ada timeout, setiap request yang kena antre di sana tetap menahan satu slot thread/koneksi di modul pesanan tanpa batas. Jika ini terjadi berkali-kali secara bersamaan, seluruh pool thread/koneksi modul pesanan habis dipakai untuk menunggu, akibatnya server menjadi tidak bisa menerima request baru, dan berujung crash total atau perlu restart manual, persis gejala yang dilaporkan tim engineering FoodGo.

**Solusi desain awal:** Set timeout yang jelas di semua pemanggilan antar service, ditambah circuit breaker: jika modul pembayaran sudah terlihat melambat/gagal berkali-kali secara beruntun, circuit breaker akan "membuka" (menghentikan pengiriman request baru sementara, fail fast) daripada terus menunggu dan ikut menghabiskan resource modul pesanan. Setelah jeda waktu tertentu, circuit breaker mencoba lagi (half-open), jika modul pembayaran sudah pulih, kirim request normal kembali, namun jika masih bermasalah, tutup kembali akses sementara.

**Trade-off:** Timeout yang terlalu pendek dapat membuat request yang sebenarnya masih valid (hanya agak lambat, belum tentu gagal) dianggap gagal, sehingga user experience terlihat lebih sering error padahal transaksi sebenarnya bisa berhasil jika diberi waktu sedikit lebih lama. Sebaliknya, timeout yang terlalu panjang tidak banyak membantu karena resource tetap tertahan dalam waktu lama. Nilai timeout perlu disesuaikan (tuning) berdasarkan data respons aktual modul pembayaran, bukan ditentukan secara sembarang.

---

## Pitfall 2: "Network is always reliable" — ditulis oleh Fathir Al Farih
 
**Bukti di skenario:** "Tim menemukan bahwa kode mereka menulis asumsi seperti # network is always reliable, no need for retry...".

**Kenapa ini keliru:** Asumsi "the network is always reliable" merupakan salah satu pitfall dalam pengembangan sistem terdistribusi. Kesalahan ini terjadi ketika seorang programmer merancang komunikasi antar-service dengan asumsi bahwa lingkungan jaringan bersifat stabil dan terkendali sepenuhnya, tanpa mempertimbangkan karakteristik jaringan yang sesungguhnya (in real life condition).

Dalam kondisi nyata, kegagalan jaringan adalah sesuatu yang pasti akan terjadi pada skala dan kondisi tertentu. Bentuk kegagalan tersebut dapat berupa terputusnya koneksi, hilangnya sebagian paket data (packet loss), ketidaktersediaan server tujuan (server down), maupun keterlambatan respons akibat kepadatan lalu lintas data. Menganggap komunikasi antar-service akan selalu berhasil sama saja dengan mengasumsikan bahwa kendaraan tidak akan pernah mengalami gangguan teknis selama perjalanan, yakni sebuah asumsi yang tidak realistis dan tidak dapat dijadikan dasar perancangan sistem yang andal.

Implikasi praktikal dari asumsi ini adalah minimnya mekanisme penanganan kegagalan dalam kode, seperti tidak adanya fitur retry dan fallback saat komunikasi antar-service gagal. Membuat sistem menjadi rapuh (fragile) terhadap gangguan jaringan sekecil apa pun, dan kegagalan pada satu komponen berpotensi menjalar serta memengaruhi keseluruhan sistem.

**Dampak ke FoodGo:** Salah satu dampak ke sistem FoodGo adalah, request gagal total meski gangguannya hanya berlangsung dalam waktu yang sangat singkat. Karena tidak ada fitur retry dan fallback, transaksi user dianggap gagal meskipun sebenarnya bisa berhasil jika dicoba ulang sesaat kemudian. User harus mengulang proses checkout dari awal, menciptakan pengalaman penggunaan aplikasi yang buruk dan memiliki potensi kehilangan pelanggan.

**Solusi desain awal:** Penambahan fitur retry dan fallback pada sistem FoodGo.

**Trade-off:** 
- **Fitur retry**. 
  - **Sisi postif:** menyelesaikan masalah kegagalan total ketika terjadi network error dan memberikan fitur "quality of life" untuk user, mengurangi pengalaman buruk ketika menggunakan sistem bagi user.
  - **Sisi negatifnya:** bila terjadi banyak kegagalan secara bersamaan dan retry terus-menerus dapat membebani server dengan request berulang.
- **Fitur fallback.**
  - **Sisi positif:** menjaga sistem tetap berjalan  ketika komponen utama gagal, misalnya dengan menyajikan data dari cache, respons default, atau layanan cadangan. User tetap bisa memakai fitur inti dan tidak melihat error total. Fallback juga mencegah kegagalan satu komponen merembet ke komponen lain (cascading failure).
  - **Sisi negatif:** data yang ditampilkan bisa kedaluwarsa (stale) atau tidak konsisten dengan kondisi sebenarnya, dan fitur yang tersedia terbatas. Fallback juga menambah kompleksitas dan biaya (infrastruktur cadangan dan jalur kode tambahan). Jalur fallback yang jarang dipakai dan jarang diuji bisa ikut gagal saat dibutuhkan, dan kegagalan komponen utama bisa tersamarkan jika tidak ada monitoring yang memadai.

--- 
## Pitfall 3: Single point of failure - Desain arsitektur monolitik — ditulis oleh Muhammad Kelvin Firmansyah 

**Bukti di skenario:** "satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama...".

**Kenapa ini keliru:** : Menempatkan seluruh fungsi penting pada satu server atau satu proses membuat modul-modul yang memiliki karakteristik beban berbeda (pesanan, pembayaran, notifikasi kurir) berbagi resource (CPU, memori) yang sama tanpa batas pemisah. Akibatnya, lonjakan beban pada satu modul dapat menghabiskan resource yang seharusnya tersedia untuk modul lain, meskipun modul tersebut tidak bermasalah. Masalahnya bukan sekadar "satu server", tapi tidak adanya isolasi resource antar modul yang beban kerjanya jauh berbeda.

**Dampak ke FoodGo:** Lonjakan load di modul notifikasi kurir (misalnya) bisa menghabiskan resource server yang juga dipakai oleh modul pesanan dan pembayaran, meskipun dua modul itu tidak bermasalah. Akibatnya seluruh sistem down secara bersamaan, tidak hanya salah satu fitur.

**Solusi desain awal:** Memisahkan modul menjadi beberapa service, yaitu dipisahkan menjadi Order Service, Payment Service dan Notification Service, kemudian menjalankan masing-masing service pada instance (server)yang berbeda. Gunakan load balancer untuk mendistribusikan trafik dan menyediakan redundancy sehingga kegagalan satu instance tidak langsung menghentikan seluruh sistem.

**Trade-off:** Memisahkan sistem menjadi beberapa service menambah kompleksitas operasional dan biaya. Komunikasi yang sebelumnya berupa pemanggilan fungsi di dalam satu proses kini menjadi request melalui jaringan antar service, sehingga rentan terhadap masalah jaringan (berkaitan dengan pitfall network reliability dan timeout). Selain itu, dibutuhkan biaya tambahan untuk menjalankan beberapa instance server beserta load balancer, serta usaha tambahan untuk monitoring dan deployment tiap service secara terpisah. Bagi tim kecil seperti FoodGo, kompleksitas ini perlu diimbangi dengan manfaat skalabilitas yang diperoleh, bukan langsung memecah sistem menjadi banyak service kecil sekaligus.

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]

Kesimpulan dari analisis skenario Tugas 1 adalah, sistem didesain tanpa konsiderasi kondisi asli lapangan yang tidak ideal, seperti latency yang tidak pernah 0 dan jaringan yang tidak selalu andal. Hal ini menyebabkan desain mengalami pitfall dan kurangnya fitur untuk menjaga kestabilan sistem FoodGo. Sehingga solusi dari kami adalah memberikan beberapa fitur yang memastikan sistem tetap andal meski digunakan pada kondisi yang tidak ideal, contohnya, menambahkan set timeout dan circuit breaker untuk mengatasi pitfall "latency is zero", serta penambahan fitur retry dan fallback untuk pitfall "network is always reliable".

Tak hanya itu, kami menyimpulkan desain arsitektur sistem kurang cocok untuk tipe aplikasi FoodGo. Sistem berbentuk monolith yang menggabungkan semua modul fungsi menjadi satu sistem yang saling berhubungan, menyebabkan bila ada satu saja kesalahan sistem, maka permasalahan tersebut akan menjalar ke modul fungsi yang lain meski secara logika tidak terhubung secara langsung.

Oleh karena itu berdasarkan penemuan kami, Akar masalah FoodGo adalah arsitektur monolit yang menjadi SPOF (Single point of failure), Solusinya sistem FoodGo menggunakan arsitektur yang merupakan kombinasi SOA (dipecah per kapabilitas bisnis) dan Publish-Subscribe (komunikasi asinkron via broker), dengan Layered sebagai struktur internal tiap service dan pola resiliensi (timeout, retry, circuit breaker) pada pemanggilan sinkron. Sementara tipe arsitektur sistem peer-to-Peer tidak cocok karena FoodGo membutuhkan kontrol dan konsistensi terpusat.
