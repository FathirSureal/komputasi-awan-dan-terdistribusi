# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4: Tidak terdapat kendala

## Skenario 1: Start normal
- Leader yang terpilih: Node 5
- Log/observasi: Node start hampir bersamaan, jadi node 1, 2, dan 3 sempat menjadi leader sementara (mengirim ELECTION, tidak ada OK, lalu broadcast COORDINATOR). Node 4 mengirim ELECTION ke node 5, menerima OK, lalu menunggu COORDINATOR. Node 5 tidak punya peer ber-ID lebih besar, sehingga tidak ada OK dalam ELECTION_TIMEOUT (2 detik), lalu menyatakan diri leader dan broadcast COORDINATOR. Node 1-4 mencatat "Leader sekarang: node 5". Log node 5 sempat berakhir di "Leader sekarang: node 3" karena COORDINATOR dari node 3 datang terlambat dan menimpa leader_id, tetapi node 1-4 tetap sepakat leader = node 5.

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: Node 4
- Berapa lama waktu sampai leader baru terdeteksi: sekitar 2-5 detik (perkiraan dari parameter kode). Deteksi leader mati maksimal 3 detik (interval PING di monitor_leader), lalu node 4 menunggu ELECTION_TIMEOUT 2 detik tanpa OK dari node 5, kemudian menyatakan diri leader dan broadcast COORDINATOR. Node 1-3 mencatat "Leader sekarang: node 4".
  
## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 18 Oktober 2026 | Claude | Bagaimanakah aku run 5 promt tersebut (python3 src/node.py --id 1 --port 5001 --peers 5002,5003,5004,5005, python3 src/node.py --id 2 --port 5002 --peers 5001,5003,5004,5005, python3 src/node.py --id 3 --port 5003 --peers 5001,5002,5004,5005, python3 src/node.py --id 4 --port 5004 --peers 5001,5002,5003,5005, python3 src/node.py --id 5 --port 5005 --peers 5001,5002,5003,5004) secara bersamaan. | Ai memberikan script perintah untuk menjalankan 5 node secara bersamaan melalui powershell terminal | Kami menggunakan perintah tersebut untuk menjalankan test agar dapat menunjukan proses berjalan konsisten hampir bersamaan. |
