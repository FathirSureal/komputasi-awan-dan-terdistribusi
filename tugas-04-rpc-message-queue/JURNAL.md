# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- [keduanya], alasan:
  - [Jalur A: RPC]: Operasi cek saldo dan proses pembayaran antara modul Pesanan dan modul Pembayaran hasilnya dibutuhkan seketika. Modul Pesanan harus tahu saldo cukup atau tidak, dan pembayaran berhasil atau gagal, sebelum bisa melanjutkan pesanan. Karena itu pola sinkron (request-response) pada RPC paling cocok. RPC juga membuat pemanggilan fungsi di modul lain terasa seperti fungsi lokal (`proxy.cek_saldo("user1")`) dan hasilnya langsung bisa dipakai.

  - [Jalur B: ]:

## Kendala teknis
- Error saat setup (mis. koneksi RabbitMQ ditolak, port bentrok): ...

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
- Hasil yang diamati: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
