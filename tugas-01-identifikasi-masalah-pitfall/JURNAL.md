# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## 18 September 2026 12:25 - 16:45 [Offline meet]
- Peserta: Fathir Al Farih & Muhammad Kelvin Firmansyah
- Poin diskusi: First meet serta analisis skenario dan soal Tugas 1 : mengkaji problem yang disajikan dalam persoalan skenario FoodGo, menggunakan AI dan research sederhana di web untuk mencari materi dan konteks untuk pengerjaan soal Tugas.
- Perbedaan pendapat (jika ada): Perbedaan beberapa pitfall yang ingin di singgung dalam tugas.

## 19 September 2026 12:10 - [Online meet via Discord]
- Peserta: Fathir Al Farih & Muhammad Kelvin Firmansyah
- Poin diskusi: Second meet serta analisis skenario dan soal Tugas 1 : Push pengerjaan tugas yang sudah dikerjakan ke repository github dan revisi analisis pitfall nomor #3 yang dirasa kurang tepat
- Perbedaan pendapat (jika ada): -

## Review Silang
- [Nama] mengomentari analisis [Nama lain]: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 18 September | - Google Gemini<br>- Claude | **1. [Gemini]**<br>Berikan aku penjelasan tentang *pitfall* dalam materi awal komputasi awan dan sistem terdistribusi dengan base referensi "Fallacies of Distributed Computing" (*the network is reliable*, *latency is zero*, *bandwidth is infinite*, *the network is secure*, *topology doesn't change*, *there is one administrator*, *transport cost is zero*, *the network is homogeneous*) DAN/ATAU masalah desain sistem terdistribusi lain yang relevan (mis. *single point of failure* karena arsitektur monolitik).<br><br>**2. [Claude]**<br>Berikan contoh skenario yang mengandung *pitfall* beserta implikasi teknisnya ke sistem. | **1. [Gemini]**<br>Banyak pemula keliru menganggap jaringan komputer itu sempurna, padahal 8 Fallacies of Distributed Computing mengingatkan bahwa jaringan rawan putus, memiliki latensi, terbatas kapasitasnya, tidak otomatis aman, dan perangkatnya beragam. Jika sistem dirancang dengan asumsi yang salah ini, masalah yang muncul antara lain:<br>- *Single Point of Failure*: satu komponen down membuat seluruh aplikasi mati<br>- *Cascading failure*: error merembet ke komponen lain<br>- Data antar-server tidak sinkron<br>- Sistem macet akibat *tight coupling*<br>- Sulit melacak sumber masalah karena minim pemantauan terpusat (*lack of observability*)<br><br>**2. [Claude]**<br>Rantai kegagalan: *cache stampede* → DB overload → timeout → *retry storm* → *cascading failure* → outage luas. Di sepanjang jalur ini muncul *double charge*, stok *phantom*, dan *overselling* yang meninggalkan kekacauan data dan keuangan setelah sistem pulih. | Kami menganalisis skenario FoodGo dengan bantuan penjelasan AI, materi PPT, dan artikel dari pencarian Google. Analisis ini digunakan untuk memahami apa itu *pitfall*, apa saja yang termasuk *pitfall*, contoh permasalahan yang ditimbulkan, serta solusi yang cocok untuk masing-masing masalah. |
|19 September| Tidak Memakai AI |---|---|---|
