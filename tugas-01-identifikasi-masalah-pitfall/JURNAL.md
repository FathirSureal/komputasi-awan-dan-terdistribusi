# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## 18 September 2026 12:25 - 16:45 [Offline meet]
- Peserta: Fathir Al Farih & Muhammad Kelvin Firmansyah
- Poin diskusi: First meet serta analisis skenario dan soal Tugas 1 : mengkaji problem yang disajikan dalam persoalan skenario FoodGo, menggunakan AI dan research sederhana di web untuk mencari materi dan konteks untuk pengerjaan soal Tugas.
- Perbedaan pendapat (jika ada): Perbedaan beberapa pitfall yang ingin di singgung dalam tugas, lalu menulis hasil analisis dalam VScode cloning repository.

## 19 September 2026 12:10 - 14:28 [Online meet via Discord]
- Peserta: Fathir Al Farih & Muhammad Kelvin Firmansyah
- Poin diskusi: Second meet serta analisis skenario dan soal Tugas 1 :
  - Push pengerjaan tugas yang sudah dikerjakan dari VScode ke repository github dan revisi analisis pitfall nomor #3 yang dirasa kurang tepat, melakukan review silang pekerjaan masing masing.
  - Pembuatan kesimpulan untuk tugas 1.
  - Modifikasi kontribusi dalam pembuatan analisis.
  - Melakukan Review Silang analisis yang sudah di buat
- Perbedaan pendapat (jika ada): -

## Review Silang
- Fathir Al Farih mengomentari analisis Muhammad Kelvin Firmansyah:
  -  Pitfall #1 "Latency Is Zero" : 
     - Saya merasa sudah cukup benar untuk konsepsi permasalahan pitfall, analisis sudah menghubungkan asumsi latency is zero dengan kondisi nyata pada FoodGo. Bagian dampak juga cukup jelas karena menjelaskan bagaimana request yang menunggu tanpa batas dapat menghabiskan thread atau bandwidth hingga menyebabkan server tidak mampu menerima request baru. Solusi berupa timeout dan circuit breaker juga relevan berdasarkan materi untuk mencegah kegagalan merambat ke modul fungsi lainya. 

       Namun, saya merasa ada yang kurang tepat pada bagian “Kenapa ini keliru”. Latency is zero tidak hanya berarti developer tidak menyediakan timeout, tetapi merupakan asumsi bahwa komunikasi antar service membutuhkan waktu "0 ms" atau selalu berlangsung sangat cepat dan konsisten.

  - Pitfall #3 "Single point of failure - Desain arsitektur monolitik" :
     - Sama dengan pitfall #1, analisis yang dilakukan sudah benar untuk penjelasan identifikasi masalah utama, yaitu seluruh modul bergantung pada satu server dan satu proses monolitik, serta penjelasan bahwa masalahnya bukan hanya server tunggal, tetapi tidak adanya isolasi antar modul untuk menghindari permasalahan SPOF (Single point of failure).
       
       Namun, dalam analisis terdapat sedikit kekeliruan pada istilah SPOF (Single Point of Failure). SPOF lebih tepat merujuk pada komponen yang ketika gagal dapat menyebabkan keseluruhan sistem atau layanan penting ikut gagal. Sementara penjelasan tentang lonjakan beban salah satu modul yang menghabiskan CPU/memori modul fitur lain lebih tepat disebut sebagai masalah resource contention atau lack of isolation

- Muhammad Kelvin Firmansyah mengomentari analisis Fathir Al Farih: 
  - Pitfall #2 "Network is always reliable" :
    - Saya merasa sudah cukup bagus untuk konsepsi permasalahan pitfall, analisis sudah menghubungkan asumsi network is always reliable dengan kondisi nyata pada FoodGo, dan analogi kendaraan yang tidak pernah mengalami gangguan teknis selama perjalanan cukup membantu memahami kenapa asumsi ini tidak realistis. Bagian dampak juga jelas karena menjelaskan bagaimana kegagalan sesaat langsung dianggap gagal total tanpa retry. Trade-off retry dan fallback juga dijelaskan dengan baik karena dipecah per fitur, dengan sisi positif dan negatif masing-masing dijabarkan secara jelas sehingga konsekuensinya mudah dipahami.

      Namun, saya merasa ada yang kurang tepat pada bagian "Kenapa ini keliru". Di situ disebutkan bentuk kegagalan jaringan mencakup "keterlambatan respons akibat kepadatan lalu lintas data" sebagai bagian dari pitfall network reliability. Padahal keterlambatan respons (latency yang melonjak saat beban tinggi) itu lebih tepat masuk ke pitfall "Latency is Zero" yang saya bahas, sedangkan network reliability harusnya fokus ke kegagalan pengiriman itu sendiri (koneksi putus, packet loss, server tidak terjangkau), bukan soal cepat-lambatnya respons.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 18 September | - Google Gemini<br>- Claude | **1. [Gemini]**<br>Berikan aku penjelasan tentang *pitfall* dalam materi awal komputasi awan dan sistem terdistribusi dengan base referensi "Fallacies of Distributed Computing" (*the network is reliable*, *latency is zero*, *bandwidth is infinite*, *the network is secure*, *topology doesn't change*, *there is one administrator*, *transport cost is zero*, *the network is homogeneous*) DAN/ATAU masalah desain sistem terdistribusi lain yang relevan (mis. *single point of failure* karena arsitektur monolitik).<br><br>**2. [Claude]**<br>Berikan contoh skenario yang mengandung *pitfall* beserta implikasi teknisnya ke sistem. | **1. [Gemini]**<br>Banyak pemula keliru menganggap jaringan komputer itu sempurna, padahal 8 Fallacies of Distributed Computing mengingatkan bahwa jaringan rawan putus, memiliki latensi, terbatas kapasitasnya, tidak otomatis aman, dan perangkatnya beragam. Jika sistem dirancang dengan asumsi yang salah ini, masalah yang muncul antara lain:<br>- *Single Point of Failure*: satu komponen down membuat seluruh aplikasi mati<br>- *Cascading failure*: error merembet ke komponen lain<br>- Data antar-server tidak sinkron<br>- Sistem macet akibat *tight coupling*<br>- Sulit melacak sumber masalah karena minim pemantauan terpusat (*lack of observability*)<br><br>**2. [Claude]**<br>Rantai kegagalan: *cache stampede* → DB overload → timeout → *retry storm* → *cascading failure* → outage luas. Di sepanjang jalur ini muncul *double charge*, stok *phantom*, dan *overselling* yang meninggalkan kekacauan data dan keuangan setelah sistem pulih. | Kami menganalisis skenario FoodGo dengan bantuan penjelasan AI, materi PPT, dan artikel dari pencarian Google. Analisis ini digunakan untuk memahami apa itu *pitfall*, apa saja yang termasuk *pitfall*, contoh permasalahan yang ditimbulkan, serta solusi yang cocok untuk masing-masing masalah. |
|19 September| Tidak Memakai AI |---|---|---|
