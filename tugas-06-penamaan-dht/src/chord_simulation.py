"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)

Memetakan ID Kurir (identitas tetap) -> alamat IP terkini, tanpa server pusat.
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
        # key kurir (hasil hash) -> (kurir_id, ip_kurir)
        self.data: dict[int, tuple[str, str]] = {}
        # Tambahan untuk simulasi: key kurir (hash) -> node_id yang SAAT INI memegang data.
        # Dipakai agar perpindahan tanggung jawab antar node bisa dicatat dan ditampilkan.
        self.holder: dict[int, int] = {}
        # node_id -> nama node (hanya untuk log yang mudah dibaca)
        self.names: dict[int, str] = {}

    # ---------- util tampilan ----------
    def _label(self, node_id: int) -> str:
        return f"{self.names.get(node_id, '?')}(id={node_id})"

    def show_ring(self):
        print("Ring (urut berdasarkan hash):")
        for nid in sorted(self.nodes):
            held = [self.data[k][0] + f"(h={k})" for k, h in self.holder.items() if h == nid]
            print(f"  {self._label(nid):28s} ip={self.nodes[nid]:10s} memegang: {held or '-'}")

    # ---------- operasi topologi ----------
    def join(self, node_name: str, node_ip: str):
        """Tambahkan node baru ke ring. Pindahkan data yang seharusnya
        menjadi tanggung jawab node baru ini dari successor lamanya."""
        node_id = hash_id(node_name)
        if node_id in self.nodes:
            print(f"[JOIN] Gagal: id={node_id} sudah dipakai node {self._label(node_id)} (tabrakan hash)")
            return

        # Successor LAMA dicari sebelum node baru dimasukkan ke self.nodes
        old_successor = self.find_successor(node_id) if self.nodes else None

        # Tambahkan node ke ring
        self.nodes[node_id] = node_ip
        self.names[node_id] = node_name
        print(f"[JOIN] Node '{node_name}' (id={node_id}) bergabung, alamat {node_ip}", end="")
        print(f", successor lama = {self._label(old_successor)}" if old_successor is not None else " (ring kosong)")

        # Key yang kini jatuh ke node baru diambil alih dari successor lama
        for key_hash in sorted(self.data):
            if self.holder.get(key_hash) == old_successor and self.find_successor(key_hash) == node_id:
                kurir_id = self.data[key_hash][0]
                self.holder[key_hash] = node_id
                print(f"       -> key {kurir_id} (h={key_hash}) pindah: "
                      f"{self._label(old_successor)} => {self._label(node_id)}")

    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring. Data yang dipegangnya berpindah ke successor-nya."""
        node_id = hash_id(node_name)
        if node_id not in self.nodes:
            print(f"[LEAVE] Node '{node_name}' tidak ada di ring")
            return

        label = self._label(node_id)
        del self.nodes[node_id]
        print(f"[LEAVE] Node '{node_name}' (id={node_id}) keluar dari ring")

        orphaned = [k for k, h in self.holder.items() if h == node_id]
        if not self.nodes:
            for k in orphaned:
                del self.holder[k]
            print("       -> ring kosong, semua data hilang")
        else:
            for key_hash in sorted(orphaned):
                new_owner = self.find_successor(key_hash)
                self.holder[key_hash] = new_owner
                print(f"       -> key {self.data[key_hash][0]} (h={key_hash}) pindah: "
                      f"{label} => {self._label(new_owner)}")
        self.names.pop(node_id, None)

    # ---------- inti Chord ----------
    def find_successor(self, key_hash: int) -> int:
        """Node_id terkecil yang >= key_hash; jika tidak ada, wrap-around
        ke node_id terkecil di ring."""
        if not self.nodes:
            raise RuntimeError("Ring kosong, tidak ada successor")
        candidates = [n for n in self.nodes if n >= key_hash]
        return min(candidates) if candidates else min(self.nodes)

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        key_hash = hash_id(kurir_id)
        node_id = self.find_successor(key_hash)
        self.data[key_hash] = (kurir_id, ip_kurir)
        self.holder[key_hash] = node_id
        print(f"[REGISTER] {kurir_id} (h={key_hash}) -> {ip_kurir}, disimpan di {self._label(node_id)}")

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        key_hash = hash_id(kurir_id)
        node_id = self.find_successor(key_hash)
        entry = self.data.get(key_hash)
        if entry and entry[0] == kurir_id and self.holder.get(key_hash) == node_id:
            return f"{entry[1]}  [dilayani {self._label(node_id)}]"
        return None


def main():
    ring = ChordRing()

    print("--- 4 node bergabung ---")
    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-jakarta-2", "10.0.0.2")
    ring.join("node-bandung-1", "10.0.0.3")
    ring.join("node-surabaya-1", "10.0.0.4")

    print("\n--- Daftarkan kurir ---")
    ring.register_kurir("kurir-001", "192.168.1.10")
    ring.register_kurir("kurir-002", "192.168.1.11")
    ring.register_kurir("kurir-003", "192.168.1.12")
    print()
    ring.show_ring()

    print("\n--- Lookup sebelum perubahan topologi ---")
    for k in ("kurir-001", "kurir-002", "kurir-003"):
        print(f"{k} ->", ring.lookup(k))

    print("\n--- Node baru bergabung ---")
    ring.join("node-semarang-1", "10.0.0.5")
    for k in ("kurir-001", "kurir-002", "kurir-003"):
        print(f"{k} ->", ring.lookup(k))
    print()
    ring.show_ring()

    print("\n--- Sebuah node keluar ---")
    ring.leave("node-surabaya-1")
    for k in ("kurir-001", "kurir-002", "kurir-003"):
        print(f"{k} ->", ring.lookup(k))
    print()
    ring.show_ring()

    print("\n--- Kurir pindah jaringan (IP berubah) ---")
    ring.register_kurir("kurir-001", "172.16.5.77")
    print("kurir-001 ->", ring.lookup("kurir-001"))


if __name__ == "__main__":
    main()
