# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): - (tidak ada, hanya kebingungan konsepsual)
- Cara memperbaikinya: ...

## Skenario join/leave

Kondisi awal: ring berisi empat node dan tiga kurir sudah terdaftar.

| Node | id | | Kurir | hash | Disimpan di node |
|---|---|---|---|---|---|
| node-bandung-1 | 40 | | kurir-002 | 28 | 40 |
| node-jakarta-2 | 102 | | kurir-001 | 50 | 102 |
| node-surabaya-1 | 136 | | kurir-003 | 132 | 136 |
| node-jakarta-1 | 177 | | | | |

* **Hasil sebelum & sesudah node baru bergabung:**

  Skenario: `node-medan-1` (id=123) bergabung ke ring.

  - **Sebelum:** urutan ring 40 → 102 → 136 → 177. `kurir-001` (hash=50) ditangani node 102.
  - **Proses:** `join()` mencari successor lama dari id 123, yaitu node 136 (node berikutnya searah jarum jam). Node 123 kemudian mengambil alih key yang hash-nya jatuh di antara node sebelumnya (102) dan dirinya sendiri (123), yaitu hash 103 sampai 123.
  - **Sesudah:** urutan ring 40 → 102 → 123 → 136 → 177. Tidak ada key yang berpindah, karena `kurir-003` (hash=132) lebih besar dari 123 sehingga masih menjadi tanggung jawab node 136. Hal ini terlihat dari log dan lookup:

    ```text
    [JOIN] Node 'node-medan-1' (id=123) bergabung, alamat 10.0.0.5
          (tidak ada key milik successor lama id=136 yang berpindah)
    [LOOKUP] 'kurir-001' (hash=50) -> node penanggung jawab id=102 (10.0.0.2)
    kurir-001 -> 192.168.1.10
    ```

  - Node yang bergabung hanya mengambil key pada rentang tanggung jawabnya. Pada skenario ini rentangnya (hash 103 sampai 123) tidak berisi kurir mana pun, jadi mapping tidak berubah dan lookup tetap berhasil.

* **Hasil sebelum & sesudah node keluar:**

  Skenario: `node-jakarta-2` (id=102) keluar dari ring.

  - **Sebelum:** urutan ring 40 → 102 → 123 → 136 → 177. `kurir-001` (hash=50) ditangani node 102.
  - **Proses:** `leave()` mencatat key yang dipegang node 102 (hanya `kurir-001`), menghapus node 102 dari ring, lalu mencari successor baru untuk key tersebut, yaitu node 123.
  - **Sesudah:** urutan ring 40 → 123 → 136 → 177. `kurir-001` kini ditangani node 123 (`node-medan-1`), sedangkan `kurir-002` (node 40) dan `kurir-003` (node 136) tidak berubah:

    ```text
    [LEAVE] Node 'node-jakarta-2' (id=102) keluar dari ring
          key 'kurir-001' (hash=50, ip=192.168.1.10) berpindah dari node id=102 ke successor baru id=123
    [LOOKUP] 'kurir-001' (hash=50) -> node penanggung jawab id=123 (10.0.0.5)
    kurir-001 -> 192.168.1.10
    [LOOKUP] 'kurir-002' (hash=28) -> node penanggung jawab id=40 (10.0.0.3)
    kurir-002 -> 192.168.1.11
    ```

  - Tanggung jawab node yang keluar diserahkan ke successor-nya. IP `kurir-001` tetap ketemu (`192.168.1.10`), yang berubah hanya node penanggung jawabnya, dari node 102 menjadi node 123. Mapping milik node lain tidak terpengaruh.

* **Hubungan kedua skenario:** `node-medan-1` yang tadinya tidak mengambil key apa pun saat bergabung justru menjadi penerus `kurir-001` ketika `node-jakarta-2` keluar.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 1 November 2026 | Claude AI | dari instruksi ini (Skenario dan penugasan), Apa yang akan ku lakukan, dan bagaimana step pengerjaan nya | Claude memberikan point card apa saja yang perlu dilakukan | kami mengerjakan dengan bantuan arahan Claude |
