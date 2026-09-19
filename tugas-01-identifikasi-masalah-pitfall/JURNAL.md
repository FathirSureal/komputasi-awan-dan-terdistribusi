# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## 18 September 2026 12:25 - 16:45 [Offline meet]
- Peserta: Fathir Al Farih & Muhammad Kelvin Firmansyah
- Poin diskusi: First meet serta analisis skenario dan soal Tugas 1 : mengkaji problem yang disajikan dalam persoalan skenario FoodGo, menggunakan AI dan research sederhana di web untuk mencari materi dan konteks untuk pengerjaan soal Tugas.
- Perbedaan pendapat (jika ada): Perbedaan beberapa pitfall yang ingin di singgung dalam tugas.

## 19 September 2026 12:10 - [Online meet via Discord]
- Peserta: Fathir Al Farih & Muhammad Kelvin Firmansyah
- Poin diskusi: Second meet serta analisis skenario dan soal Tugas 1 : Push pengerjaan tugas yang sudah dikerjakan dan revisi 
- Perbedaan pendapat (jika ada): -

## Review Silang
- [Nama] mengomentari analisis [Nama lain]: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 18 Septembber | - Google Gemini - Claude | 1. [Gemini] Berikan aku penjelasan tentang pitfall dalam materi awal komputasi awan dan sistem terdistribusi dengan base refrensi "Fallacies of Distributed Computing (referensi: "the network is reliable", "latency is zero", "bandwidth is infinite", "the network is secure", "topology doesn't change", "there is one administrator", "transport cost is zero", "the network is homogeneous") DAN/ATAU masalah desain sistem terdistribusi lain yang relevan (mis. single point of failure karena arsitektur monolitik).", 2. [Claude] Berikan contoh skenario yang mengandung pittfall dan implikasi technical ke sistem, | 1. [Gemini] Banyak pemula sering keliru karena menganggap jaringan komputer itu sempurna, padahal 8 Fallacies of Distributed Computing mengingatkan bahwa jaringan sebenarnya rawan putus, memiliki latensi, terbatas kapasitasnya, tidak otomatis aman, dan perangkatnya beragam. Jika Anda merancang sistem dengan asumsi yang salah ini, siap-siap saja menghadapi masalah yang bikin pusing: mulai dari Single Point of Failure yang membuat seluruh aplikasi mati hanya karena satu komponen down, efek domino cascading failure yang bikin eror merembet ke mana-mana, data antar-server yang tidak sinkron, hingga sistem yang macet akibat komponen terlalu terikat erat (tight coupling). Parahnya lagi, saat semua masalah ini terjadi, Anda bakal kesulitan melacak sumber masalahnya karena minimnya pemantauan terpusat (lack of observability)., 2. [Claude] Rantai singkatnya: Cache stampede → DB overload → timeout → retry storm → cascading failure → outage luas, dan di sepanjang jalur itu muncul double charge, stok phantom, dan overselling yang meninggalkan kekacauan data dan keuangan setelah sistem pulih. | Kami melakukan analisis dengan bantuan penjelasan AI menggunakan materi PPT dan artikel dari search google untuk memahami skenario dari FoodGo mengenai apa itu pitfalls dan apa yang bisa disebut dengan pitfalls serta contoh permasalahan yang ditimbulkan dan apa solusi yang cocok untuk masalah-masalah tersebut. |
