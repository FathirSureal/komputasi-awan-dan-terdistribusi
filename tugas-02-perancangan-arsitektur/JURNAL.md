# Jurnal Proses — Tugas 2

## 27 September 2026

- **Opsi arsitektur yang dipertimbangkan:** SOA murni, Publish-Subscribe murni, dan kombinasi SOA + Publish-Subscribe.
- **Kenapa akhirnya pilih kombinasi SOA + Pub-Sub:** Merujuk pada hasil Tugas 1, akar masalah FoodGo adalah arsitektur monolitik yang menjadi Single Point of Failure. SOA dipilih sebagai gaya utama untuk memisahkan sistem berdasarkan kapabilitas bisnis (Order, Payment, Katalog Resto, Kurir/Notifikasi) agar tiap service dapat dikembangkan dan di-deploy secara independen. Publish-Subscribe ditambahkan sebagai pola komunikasi pendukung khusus untuk proses notifikasi (resto & kurir) yang tidak membutuhkan respons langsung, sehingga Service Pesanan tidak perlu menunggu atau bergantung pada kecepatan service lain saat mendistribusikan event. Komunikasi yang membutuhkan kepastian jawaban (validasi stok, pembuatan order, pembayaran) tetap dipertahankan sinkron, dilengkapi timeout, circuit breaker, dan retry sebagai mekanisme resiliensi sesuai temuan pitfall Latency is Zero dan Network is Always Reliable dari Tugas 1.

- **Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa):**
  *(menyusul — akan diisi setelah revisi diagram versi 2 selesai didiskusikan/disepakati kelompok)*

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 27 September 2026 | Chat GPT AI | Berikan aku contoh bagaimana 4 komponen berikut dan interaksinya: modul Pesanan, modul Pembayaran, modul Kurir/Notifikasi, modul Katalog Resto (dan message broker/API gateway) bekerja dalam sebuah aplikasi | Dalam aplikasi FoodGo, modul Pesanan, Pembayaran, Kurir/Notifikasi dan Katalog Resto bekerja sebagai service yang memiliki fungsi masing-masing tetapi tetap saling berinteraksi. Pengguna terlebih dahulu melihat menu melalui Modul Katalog Resto, kemudian ketika melakukan pemesanan, request diteruskan melalui API Gateway ke Modul Pesanan. Setelah pesanan dibuat, Modul Pembayaran memproses transaksi. Jika pembayaran berhasil, Modul Pesanan mengirimkan event seperti OrderPaid melalui Message Broker. Event tersebut kemudian diterima oleh Modul Kurir untuk mengatur pengiriman dan Modul Notifikasi untuk memberikan informasi kepada pengguna. Dengan pola ini, setiap modul dapat bekerja secara terpisah dan komunikasi antarservice menjadi lebih terstruktur sehingga gangguan atau perubahan pada satu modul tidak harus langsung mengganggu modul lainnya. | Kami mencoba memahami bagaimana komponen-komponen tersebut bekerja dan mencoba merancang sensible architecture berdasarkan kebutuhan pada skenario FoodGo dengan dasar analisis yang telah dilakukan pada Tugas 1 dan instruksi tambahan pada Tugas 2. |
