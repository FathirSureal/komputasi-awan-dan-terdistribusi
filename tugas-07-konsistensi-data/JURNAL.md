# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi

- **Argumen yang dipertimbangkan:**
  - **Eventual Consistency:** latensi rendah dan availability tinggi, cocok untuk data yang toleran selisih sementara seperti jumlah like. Untuk saldo e-wallet kurang aman: selama jeda replikasi, Bandung masih mengembalikan saldo lama, sehingga pelanggan bisa mengira top-up gagal, top-up dua kali, atau transaksinya ditolak karena saldo tampak kurang.
  - **Sequential Consistency:** semua replika melihat urutan operasi yang sama, jadi paling aman untuk data keuangan. Kekurangannya butuh koordinasi antar replika sehingga latensi naik dan availability turun, padahal masalah di kasus ini bukan urutan global.
  - **Client-Centric (Read-Your-Writes):** menjamin pelanggan yang baru menulis selalu melihat hasil tulisannya sendiri. Biayanya jauh lebih murah dari Sequential, dan client lain tetap bisa membaca dari replika terdekat.

- **Kesimpulan akhir & alasan:**
  Eventual Consistency saja tidak cukup, tetapi Sequential Consistency penuh berlebihan. Dipilih **Eventual Consistency yang diperkuat Read-Your-Writes**. Alasannya, bug yang terjadi adalah pelanggan tidak melihat top-up miliknya sendiri, dan itu persis yang diselesaikan RYW, tanpa mengorbankan latensi dan availability seperti pada Sequential Consistency.

## Simulasi (jika dikerjakan)

- **Hasil skenario naif vs Read-Your-Writes:**
  - **Skenario naif:** Jakarta WRITE saldo user1 = 50000 (versi 1), tetapi pembacaan dari Bandung menghasilkan **0.0** karena replikasi masih tertunda. Ini bug inconsistent read. Bandung baru menjadi 50000 (versi 1) setelah delay.
  - **Skenario Read-Your-Writes:** Jakarta WRITE saldo user1 = 70000 (versi 2), dan pembacaan dari Bandung menghasilkan **70000.0** karena client membawa versi terakhir yang ia tulis, sehingga data yang lebih lama tidak dipakai. Bandung ikut 70000 (versi 2) setelah replikasi selesai.
  - **Kesimpulan:** tanpa RYW pelanggan bisa melihat saldo lama walau top-up berhasil, sedangkan dengan RYW pelanggan selalu melihat saldo terbarunya sendiri sehingga bug teratasi.
## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
