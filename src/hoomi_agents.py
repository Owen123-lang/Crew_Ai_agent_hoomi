"""
Hoomi AI Agents - Agent Definitions untuk Orchestrator
Sesuai TOR Hiliriset AI Agent Social Commerce dan Ride Fleet

Agents yang diimplementasikan:
1. Storefront Agent (Orchestrator) - Customer Service utama
2. Dispatch Agent - Fleet & Delivery Coordinator
3. Merchant Agent - Transaction & Merchant Manager
"""

from textwrap import dedent
from crewai import Agent, LLM
from hoomi_tools import (
    # Commerce Tools
    check_stock, search_product,
    # Fleet Tools
    calculate_route, find_driver,
    # HITL Tools
    pay_wallet, get_user_location,
    # Additional Tools
    track_delivery, send_notification
)
import os


class HoomiAgents():
    """
    Factory class untuk membuat AI Agents sesuai TOR Hoomi.
    
    Menggunakan Gemini sebagai LLM backend via CrewAI LLM wrapper.
    Setiap agent memiliki role, goal, backstory, dan tools spesifik.
    """
    
    def __init__(self):
        """
        Inisialisasi LLM configuration.
        Menggunakan Gemini 2.0 Flash Exp via litellm format.
        """
        # Gunakan CrewAI's LLM class dengan format litellm untuk Gemini
        self.llm = LLM(
            model="gemini/gemini-2.0-flash-exp",
            api_key=os.getenv("GOOGLE_API_KEY")
        )
    
    def storefront_agent(self):
        """
        STOREFRONT AGENT / CUSTOMER SERVICE (ORCHESTRATOR)
        
        Sesuai TOR D.1 - Storefront Agent/Customer Service:
        - Dapat meminta akses ke data penting atas izin pengguna
        - Melakukan channeling ke AI agent pembantu
        - Bertindak sebagai orchestrator utama
        
        Capabilities:
        - Mencari dan merekomendasikan produk
        - Mengecek ketersediaan stok
        - Berkoordinasi dengan Dispatch & Merchant Agent
        - Memberikan customer service yang ramah
        
        Returns:
            Agent: Storefront Agent dengan konfigurasi lengkap
        """
        return Agent(
            role='Storefront Specialist (Orchestrator)',
            goal='Membantu user mencari produk, mengecek ketersediaan stok, dan memberikan rekomendasi terbaik dengan customer service excellence',
            backstory=dedent("""\
                Anda adalah AI customer service Hoomi yang ramah, profesional, dan sangat membantu.
                Anda memiliki pengetahuan mendalam tentang semua produk di platform Hoomi,
                mulai dari makanan, barang kebutuhan, hingga layanan delivery dan ride.
                
                Anda dapat mengakses katalog produk secara real-time, mengecek stok merchant,
                dan memberikan rekomendasi yang dipersonalisasi berdasarkan preferensi user.
                
                Ketika user memerlukan layanan delivery atau ride, Anda akan berkoordinasi
                dengan Dispatch Agent untuk mengatur logistik dan Fleet Coordinator untuk
                mencari driver terdekat.
                
                Untuk transaksi pembayaran, Anda akan bekerja sama dengan Merchant Agent
                yang akan memproses payment dengan persetujuan user.
                
                Anda selalu mengutamakan kepuasan pelanggan dan memberikan informasi
                yang akurat, lengkap, dan mudah dipahami."""),
            tools=[
                search_product,      # Mencari produk di katalog
                check_stock,         # Cek ketersediaan stok
                send_notification    # Kirim notifikasi ke user
            ],
            llm=self.llm,
            verbose=True,
            allow_delegation=True,  # Dapat delegate task ke agent lain (PENTING untuk Orchestrator!)
            max_iter=15  # Max iterations untuk complex reasoning
        )
    
    def dispatch_agent(self):
        """
        DISPATCH AGENT - Fleet & Delivery Coordinator
        
        Sesuai TOR D.1 - Dispatch Agent:
        - Menghubungkan antara pengguna dengan rekanan driver
        - Melakukan pekerjaan pengantaran
        - Optimasi rute dan estimasi harga
        
        Capabilities:
        - Menghitung rute optimal menggunakan GNN
        - Estimasi waktu dan biaya pengiriman
        - Mencari driver terdekat yang available
        - Real-time tracking delivery
        - Mengakses GPS location (dengan izin user via HITL)
        
        Returns:
            Agent: Dispatch Agent dengan konfigurasi lengkap
        """
        return Agent(
            role='Fleet & Delivery Coordinator',
            goal='Mengoptimalkan logistik pengiriman dengan menghitung rute terbaik, estimasi biaya akurat, dan matching driver terdekat untuk memastikan pengiriman cepat dan efisien',
            backstory=dedent("""\
                Anda adalah koordinator armada Hoomi yang expert dalam manajemen logistik
                dan optimasi rute pengiriman. Anda memiliki akses ke sistem GPS real-time
                dan algoritma canggih untuk route optimization.
                
                Tugas utama Anda adalah:
                1. Menghitung rute tercepat dari pickup ke destination
                2. Memberikan estimasi waktu tempuh yang akurat
                3. Menghitung biaya pengiriman berdasarkan jarak dan kondisi traffic
                4. Mencari driver terdekat yang sedang available
                5. Memberikan update real-time tracking selama pengiriman
                
                Anda menggunakan teknologi Graph Neural Networks (GNN) untuk prediksi
                rute optimal dan reinforcement learning untuk driver matching.
                
                Anda selalu mempertimbangkan:
                - Jarak tempuh (distance)
                - Kondisi traffic real-time
                - Ketersediaan driver
                - Tipe kendaraan yang sesuai (motor/mobil/van)
                - Estimasi waktu yang realistis
                
                Anda bekerja sama dengan Storefront Agent untuk informasi pesanan
                dan Merchant Agent untuk konfirmasi pickup."""),
            tools=[
                calculate_route,     # Hitung rute & estimasi
                find_driver,         # Cari driver terdekat
                get_user_location,   # Get GPS (HITL required!)
                track_delivery,      # Real-time tracking
                send_notification    # Update status ke user
            ],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,  # Tidak perlu delegate, fokus ke logistik
            max_iter=10
        )
    
    def merchant_agent(self):
        """
        MERCHANT AGENT - Transaction & Merchant Manager
        
        Sesuai TOR D.1 - Merchant Agent:
        - Menghubungkan antara pengguna, driver, dan juga rekanan
        - Memproses pemesanan
        - Handle payment transaction (dengan HITL approval)
        
        Capabilities:
        - Validasi pesanan dan ketersediaan
        - Koordinasi dengan merchant untuk persiapan barang
        - Proses pembayaran via Hoomi Wallet (HITL)
        - Escrow management via smart contract
        - Konfirmasi transaksi ke semua pihak
        
        Returns:
            Agent: Merchant Agent dengan konfigurasi lengkap
        """
        return Agent(
            role='Merchant & Transaction Manager',
            goal='Memastikan transaksi berjalan lancar dengan memproses pesanan, koordinasi dengan merchant, dan handle pembayaran secure via blockchain smart contract',
            backstory=dedent("""\
                Anda adalah manajer merchant dan transaksi Hoomi yang bertanggung jawab
                atas kelancaran proses pemesanan dari awal hingga selesai.
                
                Anda berperan sebagai penghubung antara:
                - Customer (pembeli/pengguna)
                - Merchant (penjual/toko)
                - Driver (pengantar)
                
                Tugas utama Anda:
                1. Memvalidasi pesanan dan memastikan stok tersedia
                2. Mengirim konfirmasi pesanan ke merchant
                3. Memproses pembayaran melalui Hoomi Wallet dengan approval user
                4. Menggunakan smart contract di Ethereum L2 BASE untuk escrow
                5. Memastikan dana ditransfer ke merchant setelah delivery sukses
                6. Handle dispute atau komplain jika ada masalah
                
                Anda sangat memperhatikan keamanan transaksi:
                - WAJIB meminta approval user sebelum process payment (HITL)
                - Menggunakan blockchain untuk transparansi
                - Implementasi escrow untuk buyer protection
                - Validasi semua data transaksi
                
                Anda juga bertanggung jawab untuk:
                - Mengirim notifikasi status pesanan ke semua pihak
                - Koordinasi timing antara persiapan barang dan pickup driver
                - Memastikan satisfaction semua stakeholders
                
                Anda bekerja sama dengan Storefront Agent untuk detail pesanan
                dan Dispatch Agent untuk scheduling pickup/delivery."""),
            tools=[
                check_stock,         # Double-check stok sebelum payment
                pay_wallet,          # Process payment (HITL required!)
                send_notification,   # Konfirmasi ke merchant & user
                track_delivery       # Monitor delivery status
            ],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,  # Fokus ke transaction management
            max_iter=10
        )
    
    def get_all_agents(self):
        """
        Helper method untuk mendapatkan semua agents sekaligus.
        Berguna untuk setup Crew dengan cepat.
        
        Returns:
            tuple: (storefront_agent, dispatch_agent, merchant_agent)
        """
        return (
            self.storefront_agent(),
            self.dispatch_agent(),
            self.merchant_agent()
        )