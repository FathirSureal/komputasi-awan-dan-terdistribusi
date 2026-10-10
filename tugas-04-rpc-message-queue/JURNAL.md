# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- [keduanya], alasan:
  - [Jalur A: RPC]: Operasi cek saldo dan proses pembayaran antara modul Pesanan dan modul Pembayaran hasilnya dibutuhkan seketika. Modul Pesanan harus tahu saldo cukup atau tidak, dan pembayaran berhasil atau gagal, sebelum bisa melanjutkan pesanan. Karena itu pola sinkron (request-response) pada RPC paling cocok. RPC juga membuat pemanggilan fungsi di modul lain terasa seperti fungsi lokal (`proxy.cek_saldo("user1")`) dan hasilnya langsung bisa dipakai.

  - [Jalur B: ]:

## Kendala teknis
- Error saat setup (mis. koneksi RabbitMQ ditolak, port bentrok): - (tidak ada kendala)

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
- Hasil yang diamati: Consumer (modul Kurir) dimatikan terlebih dahulu, kemudian publisher (modul Pembayaran) dijalankan untuk mengirim event `pembayaran_berhasil`. Hasilnya, publisher tetap dapat mengirim pesan tanpa error dan tanpa harus menunggu respons dari consumer. Hal ini menunjukkan bahwa modul Pembayaran tetap responsif meskipun modul Kurir sedang tidak aktif. Pesan yang dikirim juga tidak hilang karena disimpan sementara oleh broker RabbitMQ di dalam antrean, yang dapat dilihat melalui kolom Ready pada dashboard. Ketika consumer kembali dijalankan, seluruh pesan yang tertunda diterima dan diproses hingga jumlah pesan dalam antrean kembali menjadi 0. Hasil pengujian ini menunjukkan bahwa komunikasi berjalan secara asinkron dan decoupled, sehingga publisher dan consumer tidak harus aktif secara bersamaan. Dengan demikian, komunikasi antar modul pada FoodGo menjadi lebih andal karena gangguan pada satu modul tidak langsung menghambat proses pada modul lainnya.
## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
