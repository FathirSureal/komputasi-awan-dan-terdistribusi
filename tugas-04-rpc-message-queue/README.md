# Tugas 4 (Pekan 4) — Komunikasi Antar Komponen

**Materi terkait:** Remote Procedure Call (RPC), Message-Oriented Middleware (MOM)/Message Queue.

## Studi Kasus

Modul **Pembayaran** dan modul **Pesanan** FoodGo harus berkomunikasi secara reliabel. Untuk beberapa operasi (mis. cek status saldo) respons dibutuhkan **seketika** (sinkron). Untuk operasi lain (mis. kirim notifikasi "pembayaran berhasil" ke modul kurir) sistem **tidak boleh menunggu** — modul pembayaran harus tetap responsif walau modul kurir sedang sibuk/down (asinkron).

## Pilihan Tugas

Kelompok **wajib memilih salah satu jalur** di bawah (boleh mengerjakan keduanya untuk nilai eksplorasi tambahan, tapi minimal satu harus selesai penuh dengan bukti jalan):

### Jalur A — RPC (Sinkron)

Skeleton di folder `rpc/` memakai `xmlrpc` — bagian dari Python standard library, **tidak perlu install apa pun**.

- `rpc/server.py`: mensimulasikan modul Pembayaran, expose fungsi `cek_saldo(user_id)` dan `proses_pembayaran(user_id, jumlah)` lewat RPC.
- `rpc/client.py`: mensimulasikan modul Pesanan yang memanggil fungsi RPC di atas dan menunggu hasilnya.

Jalankan (dua terminal terpisah, di laptop yang sama):
```bash
python3 rpc/server.py      # terminal 1
python3 rpc/client.py      # terminal 2
```

### Jalur B — Message Queue / MOM (Asinkron)

Skeleton di folder `mq/` memakai **RabbitMQ** yang dijalankan **lokal lewat Docker** (image resmi RabbitMQ, gratis, tidak perlu daftar akun apa pun) + library Python `pika`.

```bash
cd mq
docker compose up -d           # jalankan broker RabbitMQ lokal
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 consumer.py            # terminal 1: jalankan dulu consumer (modul kurir)
python3 publisher.py           # terminal 2: kirim event (modul pembayaran)
```

- `mq/publisher.py`: mensimulasikan modul Pembayaran yang mem-publish event `pembayaran_berhasil` tanpa menunggu balasan.
- `mq/consumer.py`: mensimulasikan modul Kurir/Notifikasi yang subscribe dan memproses event tersebut kapan pun siap.

Dashboard manajemen RabbitMQ (untuk lihat antrean secara visual) otomatis aktif di `http://localhost:15672` (login default `guest`/`guest`) — sertakan screenshot dashboard ini sebagai bukti tambahan.

## Tugas Kelompok

1. Lengkapi bagian `# TODO` di jalur yang dipilih.
2. Buktikan program benar-benar berjalan (screenshot 2 terminal berdampingan, atau video).
3. Untuk Jalur B, matikan dulu `consumer.py`, jalankan `publisher.py` beberapa kali, lalu nyalakan `consumer.py` — buktikan pesan **tetap diproses** (tidak hilang) karena antrean menyimpannya. Ini adalah inti pembelajaran *asynchronous decoupling*.
4. Tulis analisis: kenapa jalur ini (RPC atau MQ) cocok untuk skenario yang kalian pilih, dan apa yang terjadi jika dipakai untuk skenario yang salah (mis. RPC dipakai untuk notifikasi kurir → modul pembayaran ikut lambat kalau kurir down).

## Jalur yang dipilih
- [Jalur B: Message Queue], alasan: Notifikasi "pembayaran berhasil" ke modul Kurir tidak boleh membuat modul Pembayaran menunggu. Publisher cukup mengirim event ke antrean `pembayaran_berhasil` di RabbitMQ lalu langsung lanjut, sedangkan consumer (Kurir) mengambilnya saat sudah siap.

## Analisis

### Kenapa Message Queue cocok
Modul Pembayaran (`publisher.py`) mengirim event `pembayaran_berhasil` ke modul Kurir (`consumer.py`) lewat RabbitMQ. Alasan Message Queue cocok untuk skenario ini:

- **Pembayaran tetap responsif.** Publisher hanya menaruh pesan di antrean dengan `basic_publish` tanpa menunggu balasan, sehingga Kurir yang sibuk atau mati tidak menghambat Pembayaran.
- **Pesan tidak hilang.** Antrean dideklarasikan `durable=True` dan pesan dikirim dengan `delivery_mode=2` (persistent), jadi pesan tetap tersimpan di broker sampai consumer siap, bahkan jika RabbitMQ restart.
- **Pesan dihapus setelah selesai diproses.** Consumer memanggil `basic_ack` setelah pesan berhasil diproses, sehingga pesan yang belum selesai tidak hilang dari antrean.
- **Decoupling.** Publisher dan consumer tidak perlu aktif bersamaan. Pesan yang dikirim saat consumer mati tetap diterima ketika consumer dijalankan kembali.
- **Mudah dikembangkan.** Consumer dapat ditambah saat beban naik tanpa mengubah kode publisher.

### Jika dipakai untuk skenario yang salah
- **Message Queue untuk operasi yang butuh jawaban seketika** (mis. `cek_saldo`, `proses_pembayaran`): karena asinkron, modul Pesanan tidak langsung tahu saldo cukup atau pembayaran berhasil, dan harus menunggu balasan lewat antrean lain sehingga alurnya lebih rumit. RPC lebih tepat untuk kasus ini.
- **RPC untuk notifikasi ke Kurir:** modul Pembayaran harus menunggu balasan Kurir. Jika Kurir lambat, Pembayaran ikut lambat. Jika Kurir mati, panggilan gagal dan kegagalan itu merambat ke Pembayaran, serta notifikasi yang dikirim saat itu hilang karena tidak ada penyangga.

**Kesimpulan:** Message Queue untuk operasi yang boleh tertunda dan tidak boleh memblokir pengirim (notifikasi ke Kurir), RPC untuk operasi yang hasilnya dibutuhkan seketika (cek saldo, pembayaran).

## Struktur Submission

```
tugas-04-rpc-message-queue/
├── README.md      # Analisis: kenapa sinkron/asinkron, hasil uji "pesan tidak hilang"
├── JURNAL.md
├── rpc/            # Jalur A (jika dikerjakan)
├── mq/             # Jalur B (jika dikerjakan)
└── bukti/
```

## Rubrik Penilaian (Tugas 4)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Implementasi berjalan (minimal 1 jalur) | 35% | RPC call sukses dapat balasan, ATAU pesan MQ sukses dikonsumsi |
| Bukti *asynchronous decoupling* (khusus Jalur B) / bukti sinkron blocking (Jalur A) | 25% | Skenario consumer mati lalu nyala lagi (B), atau bukti client menunggu response (A) |
| Analisis pemilihan pola komunikasi | 25% | Justifikasi tepat berdasarkan kebutuhan sinkron vs asinkron di skenario |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya konsep umum RPC/message queue ke AI; **tidak boleh** meminta AI menuliskan isi `# TODO` di `rpc/server.py`, `rpc/client.py`, `mq/publisher.py`, atau `mq/consumer.py`. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- `JURNAL.md` wajib menjelaskan apa yang terjadi pada request RPC jika server mati di tengah proses (Jalur A), atau ke mana pesan "hilang sementara" tersimpan saat consumer mati (Jalur B) — jawaban generik/hafalan istilah tanpa mengaitkan ke hasil percobaan sendiri akan dinilai rendah.
