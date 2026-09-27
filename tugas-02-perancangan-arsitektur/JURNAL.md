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
| ... | ... | ... | ... | ... |
