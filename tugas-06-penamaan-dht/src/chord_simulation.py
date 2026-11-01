"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)

Fungsi hashing & struktur data ring sudah disediakan.
Lengkapi TODO untuk lookup(), join(), dan leave().
"""

import hashlib

M_BITS = 8               # ruang identifier 0..255 (disederhanakan dari Chord asli yang pakai 160-bit)
RING_SIZE = 2 ** M_BITS


def hash_id(key: str) -> int:
    """Hash string (ID node atau ID kurir) ke ruang identifier 0..RING_SIZE-1."""
    digest = hashlib.sha1(key.encode()).digest()
    return int.from_bytes(digest, "big") % RING_SIZE


class ChordRing:
    def __init__(self):
        # node_id (hasil hash) -> alamat IP node tersebut
        self.nodes: dict[int, str] = {}
        # key kurir (hasil hash) -> IP kurir yang disimpan node yang bertanggung jawab
        self.data: dict[int, tuple[str, str]] = {}  # hash -> (kurir_id, ip_kurir)

    def join(self, node_name: str, node_ip: str):
        """Tambahkan node baru ke ring. Pindahkan data yang seharusnya
        menjadi tanggung jawab node baru ini dari successor lamanya."""
        node_id = hash_id(node_name)

        # Guard: dua nama berbeda bisa menghasilkan hash sama di ruang 8-bit (collision)
        if node_id in self.nodes:
            print(f"[JOIN] Node '{node_name}' GAGAL bergabung: id={node_id} sudah dipakai node lain")
            return

        # TODO 1: tambahkan node_id -> node_ip ke self.nodes.
        self.nodes[node_id] = node_ip
        print(f"[JOIN] Node '{node_name}' (id={node_id}) bergabung, alamat {node_ip}")

        # TODO 2: cari successor LAMA dari node_id ini (successor sebelum node
        # baru bergabung, gunakan find_successor() dengan node_id INI dikecualikan
        # dulu dari self.nodes saat mencari).
        # kecualikan node baru sementara
        del self.nodes[node_id]                       
        successor_lama = self.find_successor(node_id) if self.nodes else None
        # kembalikan node baru ke ring
        self.nodes[node_id] = node_ip                 

        # TODO 3: pindahkan semua key di self.data yang seharusnya menjadi
        # tanggung jawab node baru (key dengan hash <= node_id, tapi masih
        # dipegang oleh successor lama) ke bawah tanggung jawab node baru.
        # (Untuk simulasi sederhana, cukup print log siapa mengambil alih apa -
        # tidak perlu benar-benar memindahkan struktur data kompleks.)
        if successor_lama is None:
            print("      (ring baru berisi satu node, tidak ada data yang dipindahkan)")
            return

        dipindah = 0
        for key_hash, (kurir_id, ip_kurir) in sorted(self.data.items()):
            # Dengan node baru sudah ada di ring, key yang successor-nya sekarang
            # adalah node_id (padahal sebelumnya dipegang successor lama) = key yang diambil alih.
            # find_successor() sudah menangani wrap-around, jadi kasus ring melingkar ikut tercakup.
            if self.find_successor(key_hash) == node_id:
                print(f"      key '{kurir_id}' (hash={key_hash}, ip={ip_kurir}) "
                      f"diambil alih node id={node_id} dari successor lama id={successor_lama}")
                dipindah += 1
        if dipindah == 0:
            print(f"      (tidak ada key milik successor lama id={successor_lama} yang berpindah)")

    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring. Data yang dipegangnya harus
        berpindah ke successor-nya."""
        node_id = hash_id(node_name)

        if node_id not in self.nodes:
            print(f"[LEAVE] Node '{node_name}' (id={node_id}) tidak ada di ring")
            return

        # Catat dulu key yang dipegang node ini, selagi node masih ada di ring
        key_dipegang = sorted(k for k in self.data if self.find_successor(k) == node_id)

        # TODO 4: hapus node_id dari self.nodes.
        del self.nodes[node_id]
        print(f"[LEAVE] Node '{node_name}' (id={node_id}) keluar dari ring")

        # TODO 5: cari successor BARU untuk tiap key yang tadinya dipegang
        # node ini, pindahkan ke successor tersebut.
        if not self.nodes:
            print("      PERINGATAN: ring kosong, data tidak punya penanggung jawab lagi")
            return

        for key_hash in key_dipegang:
            kurir_id, ip_kurir = self.data[key_hash]
            successor_baru = self.find_successor(key_hash)
            print(f"      key '{kurir_id}' (hash={key_hash}, ip={ip_kurir}) "
                  f"berpindah dari node id={node_id} ke successor baru id={successor_baru}")
        if not key_dipegang:
            print("      (node ini tidak memegang key apa pun)")

    def find_successor(self, key_hash: int) -> int:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash
        (successor menurut aturan Chord). Jika tidak ada, wrap-around
        ke node dengan hash terkecil di ring (karena ring melingkar)."""
        # TODO 6: implementasikan logika successor di atas menggunakan
        # self.nodes.keys(). Kembalikan node_id (bukan IP).
        if not self.nodes:
            raise ValueError("Ring kosong: belum ada node yang bergabung")

        kandidat = [nid for nid in self.nodes.keys() if nid >= key_hash]
        if kandidat:
            return min(kandidat)
        return min(self.nodes.keys())  # wrap-around

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        key_hash = hash_id(kurir_id)
        # TODO 7: panggil find_successor(key_hash) untuk menentukan node
        # penanggung jawab, lalu simpan (kurir_id, ip_kurir) ke self.data[key_hash].
        node_id = self.find_successor(key_hash)
        self.data[key_hash] = (kurir_id, ip_kurir)
        print(f"[REGISTER] '{kurir_id}' (hash={key_hash}) -> {ip_kurir}, "
              f"disimpan di node id={node_id} ({self.nodes[node_id]})")

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        key_hash = hash_id(kurir_id)
        # TODO 8: gunakan find_successor(key_hash) untuk menemukan node
        # penanggung jawab, lalu kembalikan ip_kurir dari self.data jika ada.
        node_id = self.find_successor(key_hash)
        print(f"[LOOKUP] '{kurir_id}' (hash={key_hash}) -> node penanggung jawab "
              f"id={node_id} ({self.nodes[node_id]})")

        entry = self.data.get(key_hash)
        if entry is not None and entry[0] == kurir_id:
            return entry[1]
        return None


def main():
    ring = ChordRing()

    # Skenario awal: 4 node bergabung
    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-jakarta-2", "10.0.0.2")
    ring.join("node-bandung-1", "10.0.0.3")
    ring.join("node-surabaya-1", "10.0.0.4")

    # Daftarkan beberapa kurir
    ring.register_kurir("kurir-001", "192.168.1.10")
    ring.register_kurir("kurir-002", "192.168.1.11")
    ring.register_kurir("kurir-003", "192.168.1.12")

    print("\n--- Lookup sebelum perubahan topologi ---")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))

    print("\n--- Node baru bergabung ---")
    ring.join("node-medan-1", "10.0.0.5")
    print("kurir-001 ->", ring.lookup("kurir-001"))

    print("\n--- Sebuah node keluar ---")
    ring.leave("node-jakarta-2")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))


if __name__ == "__main__":
    main()
