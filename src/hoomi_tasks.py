"""
Hoomi AI Tasks - Task Definitions untuk Workflow
Sesuai TOR Hiliriset AI Agent Social Commerce dan Ride Fleet

Tasks dikelompokkan berdasarkan 3 proses bisnis utama:
1. Jual Beli Barang (Commerce)
2. Pengantaran Barang (Delivery)
3. Antar Jemput Penumpang (Ride)

Setiap task mengikuti struktur:
- Description: Instruksi detail untuk agent
- Expected Output: Format output yang diharapkan
- Agent: Agent yang bertanggung jawab
- Context: Dependencies dari task sebelumnya
- Human Input: Flag untuk HITL (Guardrails)
"""

from textwrap import dedent
from crewai import Task


class HoomiTasks():
    """
    Factory class untuk membuat Tasks sesuai workflow Hoomi.
    
    Mengimplementasikan 3 proses bisnis utama sesuai TOR Section C:
    1. Jual Beli Barang
    2. Pengantaran Barang  
    3. Antar Jemput Penumpang
    """
    
    # ==========================================
    # PROSES BISNIS 1: JUAL BELI BARANG
    # Sesuai TOR Section C - Jual Beli Barang
    # ==========================================
    
    def search_product_task(self, agent, product_query: str, user_location: str = None):
        """
        Task 1: Pencarian Barang Jualan
        
        Sesuai TOR:
        - Pengguna dapat mencari barang melalui AI agent
        - Pengguna memilih barang yang ditampilkan
        - Sistem melakukan pengecekan stok sebelum mengirimkan respon
        
        Args:
            agent: Storefront Agent yang akan mengeksekusi
            product_query: Kata kunci produk yang dicari user
            user_location: Lokasi user untuk filtering merchant terdekat (optional)
        
        Returns:
            Task: Task configuration untuk product search
        """
        return Task(
            description=dedent(f"""\
                User ingin membeli produk: "{product_query}"
                {f"Lokasi user: {user_location}" if user_location else ""}
                
                TUGAS ANDA:
                1. Gunakan tool 'search_product' untuk mencari produk di katalog Hoomi
                   - Gunakan query yang sesuai dengan permintaan user
                   - Pertimbangkan kategori yang relevan (food/goods)
                
                2. Untuk setiap produk yang ditemukan:
                   - Gunakan tool 'check_stock' untuk validasi ketersediaan
                   - Pastikan stok tersedia sebelum merekomendasikan
                
                3. Berikan rekomendasi produk terbaik berdasarkan:
                   - Rating merchant
                   - Jarak dari user (jika lokasi tersedia)
                   - Harga kompetitif
                   - Ketersediaan stok
                
                4. Tampilkan minimal 2-3 pilihan produk (jika tersedia)
                   dengan informasi lengkap
                
                PENTING: 
                - Hanya rekomendasikan produk yang stoknya available
                - Urutkan berdasarkan recommendation score
                - Berikan informasi yang jelas dan mudah dipahami"""),
            
            expected_output=dedent("""\
                Format output dalam JSON atau text yang user-friendly:
                
                ```
                HASIL PENCARIAN: "{product_query}"
                
                1. [Nama Produk]
                   Merchant: [Nama Merchant] ⭐ [Rating]
                   Harga: Rp [Harga]
                   Jarak: [Jarak] km
                   Stok: Tersedia ([Jumlah] pcs)
                   
                2. [Produk alternatif...]
                
                REKOMENDASI TERBAIK: [Produk dengan score tertinggi]
                Alasan: [Penjelasan singkat]
                ```
                
                Berikan informasi yang lengkap dan mudah dipahami user."""),
            
            agent=agent,
            async_execution=False  # Sequential untuk data validation
        )
    
    def delivery_setup_task(self, agent, destination: str, product_info: str = None):
        """
        Task 2: Penentuan Pengiriman
        
        Sesuai TOR:
        - Pengguna memasukkan alamat tujuan (atau gunakan GPS)
        - Sistem menentukan jarak dari toko ke alamat tujuan
        - Menampilkan rute perjalanan dan harga
        
        Args:
            agent: Dispatch Agent yang akan mengeksekusi
            destination: Alamat tujuan pengiriman
            product_info: Info produk dari task sebelumnya (optional)
        
        Returns:
            Task: Task configuration untuk delivery setup
        """
        return Task(
            description=dedent(f"""\
                Setup pengiriman untuk order:
                {f"Produk: {product_info}" if product_info else ""}
                Tujuan: {destination}
                
                TUGAS ANDA:
                1. Dapatkan lokasi user saat ini:
                   - Gunakan tool 'get_user_location'
                   - ⚠️ PENTING: Tool ini memerlukan IZIN USER (HITL)!
                   - Jika user tidak approve, gunakan alamat manual
                
                2. Identifikasi lokasi merchant/toko:
                   - Gunakan info dari task sebelumnya (context)
                   - Atau estimate koordinat dari nama merchant
                
                3. Hitung rute pengiriman:
                   - Gunakan tool 'calculate_route' dengan koordinat pickup & destination
                   - Dapatkan estimasi jarak, waktu, dan biaya
                
                4. Cari driver terdekat:
                   - Gunakan tool 'find_driver' di lokasi merchant
                   - Pilih tipe kendaraan yang sesuai (motorcycle untuk jarak dekat)
                   - Dapatkan ETA driver untuk pickup
                
                5. Berikan summary lengkap:
                   - Rute perjalanan (dengan Google Maps link)
                   - Total jarak dan estimasi waktu
                   - Biaya pengiriman
                   - Info driver yang akan mengambil
                
                CATATAN KEAMANAN:
                - Tool 'get_user_location' akan meminta approval user
                - Jika ditolak, tanyakan alamat secara manual
                - Pastikan estimasi akurat dan realistis"""),
            
            expected_output=dedent("""\
                Format output lengkap untuk delivery setup:
                
                ```
                📍 DETAIL PENGIRIMAN
                
                Dari: [Nama Merchant/Toko]
                      [Alamat pickup]
                
                Ke:   [Alamat tujuan user]
                
                🗺️ RUTE & ESTIMASI:
                - Jarak: [X] km
                - Estimasi waktu: [Y] menit
                - Biaya pengiriman: Rp [Z]
                - Link Google Maps: [URL]
                - Kondisi traffic: [moderate/heavy/light]
                
                🚗 DRIVER TERDEKAT:
                - Nama: [Nama Driver]
                - Rating: ⭐ [Rating] ([Total trips] trips)
                - Kendaraan: [Tipe] - [Plat nomor]
                - Jarak dari pickup: [X] km
                - ETA untuk pickup: [Y] menit
                
                TOTAL BIAYA: Rp [Harga produk + Ongkir]
                ```
                
                Pastikan semua informasi lengkap dan akurat."""),
            
            agent=agent,
            context=[],  # Will be set di main.py dengan task sebelumnya
            human_input=True  # HITL untuk akses GPS (Sesuai TOR Guardrails)
        )
    
    def payment_task(self, agent, total_amount: int, recipient_id: str, description: str):
        """
        Task 3: Pembayaran
        
        Sesuai TOR:
        - Pembayaran melalui AI agent memerlukan Guardrails MCP Wallet
        - Agent harus meminta izin terlebih dahulu (HITL)
        - Sistem mengirim konfirmasi setelah pembayaran
        
        Args:
            agent: Merchant Agent yang akan mengeksekusi
            total_amount: Total pembayaran (produk + ongkir)
            recipient_id: ID merchant/driver penerima
            description: Deskripsi transaksi
        
        Returns:
            Task: Task configuration untuk payment processing
        """
        return Task(
            description=dedent(f"""\
                Proses pembayaran untuk transaksi:
                - Total Amount: Rp {total_amount:,}
                - Penerima: {recipient_id}
                - Deskripsi: {description}
                
                TUGAS ANDA:
                1. Validasi detail transaksi:
                   - Pastikan total amount sudah benar (produk + ongkir)
                   - Validasi recipient ID (merchant/driver)
                   - Cek deskripsi transaksi jelas
                
                2. Proses pembayaran via Hoomi Wallet:
                   - Gunakan tool 'pay_wallet' untuk eksekusi payment
                   - ⚠️ CRITICAL: Tool ini WAJIB meminta approval user (HITL)!
                   - Jelaskan detail transaksi dengan jelas ke user
                   - Tunggu konfirmasi approval sebelum proceed
                
                3. Handle smart contract:
                   - Payment akan diproses via Ethereum L2 BASE blockchain
                   - Dana akan di-escrow sampai delivery sukses
                   - Transaction hash akan di-generate untuk tracking
                
                4. Kirim konfirmasi ke semua pihak:
                   - Gunakan tool 'send_notification' untuk:
                     * Konfirmasi ke user (receipt)
                     * Notifikasi ke merchant (order baru)
                     * Alert ke driver (pickup ready)
                
                5. Berikan receipt lengkap:
                   - Transaction ID
                   - Timestamp
                   - Detail pembayaran
                   - Blockchain transaction hash
                   - Status: Pending/Success/Failed
                
                SECURITY NOTES:
                - NEVER proceed tanpa user approval
                - Validate semua data sebelum eksekusi
                - Log transaction untuk audit trail
                - Handle error dengan graceful fallback"""),
            
            expected_output=dedent("""\
                Format output untuk payment receipt:
                
                ```
                💳 KONFIRMASI PEMBAYARAN
                
                Status: [✅ BERHASIL / ⏳ PENDING / ❌ GAGAL]
                
                DETAIL TRANSAKSI:
                - Transaction ID: [TXN123ABC...]
                - Tanggal: [YYYY-MM-DD HH:mm:ss]
                - Metode: Hoomi Wallet (Blockchain)
                
                RINCIAN BIAYA:
                - Produk: Rp [X]
                - Ongkir: Rp [Y]
                - Gas Fee: Rp [Z]
                ─────────────────
                TOTAL: Rp [Total]
                
                Saldo Wallet: Rp [Saldo setelah transaksi]
                
                BLOCKCHAIN INFO:
                - Network: Ethereum L2 BASE
                - Tx Hash: 0x[hash...]
                - Escrow: Active (sampai delivery complete)
                
                STATUS NOTIFIKASI:
                ✅ User - Receipt sent
                ✅ Merchant - Order notification sent  
                ✅ Driver - Pickup alert sent
                
                Terima kasih telah menggunakan Hoomi! 🎉
                ```
                
                Berikan informasi yang lengkap dan transparan."""),
            
            agent=agent,
            context=[],  # Will be set di main.py
            human_input=True  # HITL WAJIB untuk payment (Sesuai TOR)
        )
    
    # ==========================================
    # PROSES BISNIS 2: PENGANTARAN BARANG
    # Sesuai TOR Section C - Pengantaran Barang
    # ==========================================
    
    def package_delivery_task(self, agent, pickup_address: str, destination_address: str, 
                             package_description: str = "Paket"):
        """
        Task untuk delivery package (non-commerce).
        User ingin mengirim paket dari A ke B tanpa shopping.
        
        Sesuai TOR:
        - User memasukkan alamat asal dan tujuan
        - Sistem calculate jarak dan harga
        - Tampilkan rute dan pilih driver
        
        Args:
            agent: Dispatch Agent
            pickup_address: Alamat penjemputan paket
            destination_address: Alamat tujuan pengiriman
            package_description: Deskripsi paket (optional)
        
        Returns:
            Task: Task configuration untuk package delivery
        """
        return Task(
            description=dedent(f"""\
                User ingin mengirim paket:
                - Dari: {pickup_address}
                - Ke: {destination_address}
                - Paket: {package_description}
                
                TUGAS ANDA:
                1. Konversi alamat ke koordinat GPS:
                   - Jika alamat pickup adalah "lokasi saat ini", gunakan 'get_user_location'
                   - Untuk alamat manual, estimate koordinat atau gunakan geocoding API
                
                2. Hitung rute dan estimasi:
                   - Gunakan tool 'calculate_route' dengan koordinat pickup & destination
                   - Dapatkan jarak, durasi, dan estimasi biaya
                
                3. Cari driver terdekat:
                   - Gunakan tool 'find_driver' di lokasi pickup
                   - Pilih tipe kendaraan sesuai ukuran paket
                   - Pertimbangkan: motor (paket kecil), mobil (paket sedang), van (paket besar)
                
                4. Berikan info lengkap:
                   - Detail rute dengan Google Maps link
                   - Breakdown biaya (base fare + per km)
                   - Info driver dan ETA pickup
                   - Estimasi total waktu delivery
                
                TIPS:
                - Untuk jarak < 5km, recommend motorcycle
                - Untuk jarak 5-15km, recommend car
                - Untuk jarak > 15km atau paket besar, recommend van"""),
            
            expected_output=dedent("""\
                ```
                📦 PENGIRIMAN PAKET
                
                DETAIL PAKET:
                Deskripsi: [Package description]
                
                RUTE PENGIRIMAN:
                📍 Pickup: [Alamat pickup]
                📍 Tujuan: [Alamat destination]
                
                🗺️ ESTIMASI PERJALANAN:
                - Jarak: [X] km
                - Durasi: [Y] menit
                - Biaya: Rp [Z]
                  (Base: Rp 5,000 + Rp 2,000/km)
                - Maps: [Google Maps URL]
                
                🚗 DRIVER YANG AKAN PICKUP:
                - Nama: [Driver name]
                - Rating: ⭐ [Rating]
                - Kendaraan: [Tipe kendaraan]
                - Plat: [Nomor plat]
                - Jarak ke pickup: [X] km
                - ETA pickup: [Y] menit
                
                ⏱️ TOTAL ESTIMASI: [Waktu total] menit
                💰 TOTAL BIAYA: Rp [Total]
                ```"""),
            
            agent=agent,
            human_input=False  # Tidak perlu HITL untuk calculation
        )
    
    # ==========================================
    # PROSES BISNIS 3: ANTAR JEMPUT PENUMPANG
    # Sesuai TOR Section C - Antar Jemput Penumpang
    # ==========================================
    
    def ride_booking_task(self, agent, pickup_location: str, destination: str, 
                         passenger_count: int = 1):
        """
        Task untuk booking ride (transportation).
        User ingin naik kendaraan dari A ke B.
        
        Sesuai TOR:
        - User memasukkan lokasi pickup dan tujuan
        - Sistem calculate jarak dan harga
        - Match dengan driver terdekat
        
        Args:
            agent: Dispatch Agent
            pickup_location: Lokasi penjemputan
            destination: Lokasi tujuan
            passenger_count: Jumlah penumpang (default 1)
        
        Returns:
            Task: Task configuration untuk ride booking
        """
        return Task(
            description=dedent(f"""\
                User ingin booking kendaraan:
                - Pickup: {pickup_location}
                - Tujuan: {destination}
                - Penumpang: {passenger_count} orang
                
                TUGAS ANDA:
                1. Dapatkan lokasi pickup:
                   - Jika "{pickup_location}" adalah "lokasi saya", gunakan 'get_user_location' (HITL!)
                   - Jika alamat spesifik, konversi ke koordinat
                
                2. Hitung rute perjalanan:
                   - Gunakan tool 'calculate_route' untuk estimasi
                   - Pertimbangkan kondisi traffic real-time
                   - Berikan estimasi waktu yang realistis
                
                3. Tentukan tipe kendaraan:
                   - Motorcycle: 1 penumpang, ekonomis
                   - Car: 1-4 penumpang, nyaman
                   - Van: 5+ penumpang atau banyak barang
                
                4. Cari driver terdekat:
                   - Gunakan tool 'find_driver' dengan tipe kendaraan yang sesuai
                   - Prioritas: rating tinggi, jarak dekat, ETA cepat
                
                5. Berikan booking confirmation:
                   - Detail perjalanan (rute, jarak, waktu)
                   - Estimasi biaya (transparan)
                   - Info driver lengkap (nama, plat, foto kendaraan)
                   - ETA driver ke lokasi pickup
                   - Estimasi total waktu sampai tujuan
                
                PRICING LOGIC:
                - Base fare: Rp 5,000
                - Per km: Rp 2,500 (motor) / Rp 3,500 (mobil)
                - Traffic surge: +20% jika heavy traffic"""),
            
            expected_output=dedent("""\
                ```
                🚗 BOOKING KENDARAAN
                
                DETAIL PERJALANAN:
                📍 Pickup: [Lokasi pickup]
                📍 Tujuan: [Lokasi destination]
                👥 Penumpang: [Jumlah] orang
                
                🗺️ RUTE PERJALANAN:
                - Jarak: [X] km
                - Estimasi waktu: [Y] menit
                - Kondisi traffic: [moderate/heavy/light]
                - Maps link: [Google Maps URL]
                
                💰 ESTIMASI BIAYA:
                - Base fare: Rp 5,000
                - Jarak ([X] km × Rp [rate]/km): Rp [Y]
                - Traffic surge: Rp [Z] (jika ada)
                ─────────────────────────
                TOTAL: Rp [Total]
                
                🚗 DRIVER ANDA:
                Nama: [Driver name]
                Rating: ⭐ [Rating] ([Total trips] trips)
                Kendaraan: [Merk] [Model] [Warna]
                Plat Nomor: [Nomor plat]
                
                📱 Kontak: [Phone number]
                
                ⏱️ WAKTU:
                - ETA driver ke pickup: [X] menit
                - Total perjalanan: [Y] menit
                - Perkiraan sampai: [HH:mm]
                
                STATUS: Mencari driver... ✅ Driver ditemukan!
                
                Driver sedang menuju lokasi Anda. 
                Anda akan menerima notifikasi saat driver tiba.
                ```"""),
            
            agent=agent,
            human_input=True  # HITL jika perlu GPS location
        )
    
    # ==========================================
    # HELPER TASKS
    # ==========================================
    
    def confirmation_task(self, agent, order_summary: str):
        """
        Task untuk final confirmation dan tracking setup.
        Digunakan setelah semua task selesai.
        
        Args:
            agent: Any agent (biasanya Storefront sebagai orchestrator)
            order_summary: Summary dari semua task sebelumnya
        
        Returns:
            Task: Task configuration untuk confirmation
        """
        return Task(
            description=dedent(f"""\
                Berikan konfirmasi final kepada user:
                {order_summary}
                
                TUGAS ANDA:
                1. Ringkas semua informasi dari task sebelumnya
                2. Berikan order tracking information
                3. Setup real-time tracking (jika delivery/ride)
                4. Kirim notifikasi confirmation ke user
                5. Berikan instruksi next steps
                
                Output harus user-friendly dan encouraging!"""),
            
            expected_output=dedent("""\
                ```
                ✅ PESANAN BERHASIL!
                
                [Summary dari semua proses]
                
                TRACKING:
                Order ID: [Order ID]
                Link tracking: [URL]
                
                NEXT STEPS:
                1. Driver akan pickup dalam [X] menit
                2. Anda akan menerima update real-time
                3. Estimasi sampai: [Waktu]
                
                Terima kasih telah menggunakan Hoomi! 🎉
                Ada pertanyaan? Chat dengan kami kapan saja.
                ```"""),
            
            agent=agent,
            context=[]  # Will include all previous tasks
        )