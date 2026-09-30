# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat:
  - Versi polos (`processed_count += 1`): selalu 100 di setiap percobaan (5 kali run: 100, 100, 100, 100, 100).
  - Versi tiga langkah (baca, jeda, tulis): di bawah 100 dan berbeda tiap run (6 kali run: 79, 84, 75, 79, 82, 84).
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri):
  - Mekanisme: `processed_count += 1` sebenarnya tiga langkah: baca nilai, tambah 1, tulis balik. Kalau dua thread membaca nilai yang sama sebelum salah satunya menulis, satu update hilang. Misalnya counter bernilai 5, thread A dan B sama-sama membaca 5, lalu keduanya menulis 6, jadi dua pesanan diproses tapi counter cuma naik satu.
  - Versi polos: hasilnya tetap 100 karena operasinya sangat singkat dan thread jarang berpindah tepat di tengahnya, jadi race condition tidak terlihat. Ini bukan berarti kodenya aman, karena `+= 1` tetap bukan operasi atomik.
  - Versi tiga langkah: kami menulis increment secara eksplisit menjadi `temp = processed_count`, `time.sleep(0.0001)`, lalu `processed_count = temp + 1`. Selama sebuah thread tidur di jeda itu, thread lain sempat membaca nilai yang belum diperbarui, sehingga sebagian update tertimpa dan total akhir kurang dari 100. Jeda ini hanya untuk memperlebar peluang race condition, bukan untuk membuat program terlihat konkuren.

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: Selalu 100 di setiap percobaan (5 kali run: 100, 100, 100, 100, 100). Increment dibungkus `with lock:` sehingga hanya satu thread yang mengubah counter sekali waktu, jadi tidak ada update yang hilang.

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: Tidak terdapat kendala selama proses `docker build`/`docker run`.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 30 September 2026 | Claude | Cara melengkapi Dockerfile, membuat image, dan menjalankan container; serta error Docker Desktop (virtualisasi) dan `failed to read dockerfile` | Penjelasan fungsi tiap bagian Dockerfile, urutan `docker build` dan `docker run`, dan saran mengecek WSL2/virtualisasi serta lokasi file | Kami menulis Dockerfile sendiri, menjalankan build dan run di laptop, lalu mencatat error dan perbaikannya di bagian Kendala Docker |
| 30 September 2026 | GPT | Kenapa hasil `processed_count` sama (selalu 100) baik tanpa lock maupun dengan lock | Penjelasan bahwa `+= 1` terdiri dari baca, tambah, tulis, tapi terlalu singkat sehingga race condition jarang muncul, dan ide memecah increment dengan jeda kecil untuk memperlihatkannya | Kami menjalankan sendiri percobaan tanpa dan dengan lock, lalu menulis penjelasan di JURNAL.md dengan kata-kata sendiri berdasarkan hasil run kami |
