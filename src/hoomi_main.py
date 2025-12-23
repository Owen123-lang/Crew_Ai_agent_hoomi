"""
Hoomi AI Agent Orchestrator - Main Entry Point
Sesuai TOR Hiliriset AI Agent Social Commerce dan Ride Fleet

Implementasi Hierarchical Process dengan Manager LLM sebagai orchestrator.
Mendukung 3 proses bisnis utama:
1. Jual Beli Barang (Commerce)
2. Pengantaran Barang (Delivery)  
3. Antar Jemput Penumpang (Ride)

Menggunakan CrewAI dengan:
- Process: Hierarchical (Manager-based orchestration)
- Guardrails: Human-in-the-Loop (HITL) untuk data sensitif
- Agents: Storefront (Orchestrator), Dispatch, Merchant
"""

from dotenv import load_dotenv
from crewai import Crew, Process, LLM
from hoomi_tasks import HoomiTasks
from hoomi_agents import HoomiAgents
import os
import sys


def print_header():
    """Print aplikasi header dengan styling."""
    print("\n" + "=" * 60)
    print("🚀 HOOMI AI AGENT ORCHESTRATOR")
    print("   Social Commerce & Ride Fleet Platform")
    print("   Powered by CrewAI + Gemini 2.0")
    print("=" * 60 + "\n")


def print_menu():
    """Print menu pilihan layanan."""
    print("📋 PILIH LAYANAN HOOMI:")
    print("-" * 60)
    print("1. 🛒 Jual Beli Barang (Commerce)")
    print("   → Pesan makanan/barang dari merchant + delivery")
    print()
    print("2. 📦 Pengantaran Barang (Delivery)")
    print("   → Kirim paket dari lokasi A ke B")
    print()
    print("3. 🚗 Antar Jemput Penumpang (Ride)")
    print("   → Booking kendaraan untuk perjalanan")
    print()
    print("0. ❌ Keluar")
    print("-" * 60)


def scenario_commerce():
    """
    SKENARIO 1: JUAL BELI BARANG
    
    Workflow:
    1. Search & Select Product (Storefront Agent)
    2. Setup Delivery Route (Dispatch Agent) - HITL for GPS
    3. Process Payment (Merchant Agent) - HITL for Wallet
    
    Returns:
        tuple: (agents_list, tasks_list) atau None jika dibatalkan
    """
    print("\n" + "=" * 60)
    print("🛒 JUAL BELI BARANG")
    print("=" * 60)
    
    # Input dari user
    product = input("\n📦 Apa yang ingin Anda beli? ")
    if not product.strip():
        print("❌ Input tidak valid!")
        return None
    
    destination = input("📍 Alamat pengiriman (atau ketik 'lokasi saya'): ")
    if not destination.strip():
        print("❌ Alamat tidak boleh kosong!")
        return None
    
    # Inisialisasi agents dan tasks
    agents = HoomiAgents()
    tasks = HoomiTasks()
    
    # Create agents
    storefront = agents.storefront_agent()
    dispatch = agents.dispatch_agent()
    merchant = agents.merchant_agent()
    
    # Create tasks dengan workflow sequential
    print("\n⚙️  Menyiapkan AI agents...")
    
    # Task 1: Search product (Storefront Agent)
    task1 = tasks.search_product_task(
        agent=storefront,
        product_query=product,
        user_location=destination if destination.lower() != "lokasi saya" else None
    )
    
    # Task 2: Setup delivery (Dispatch Agent) - HITL for GPS
    task2 = tasks.delivery_setup_task(
        agent=dispatch,
        destination=destination,
        product_info=product
    )
    task2.context = [task1]  # Butuh info produk dari task1
    
    # Task 3: Process payment (Merchant Agent) - HITL for Wallet
    # Estimasi total (akan di-update setelah task1 & task2)
    estimated_total = 50000  # Placeholder
    task3 = tasks.payment_task(
        agent=merchant,
        total_amount=estimated_total,
        recipient_id="MERCHANT_TBD",
        description=f"Pembelian {product} + Delivery"
    )
    task3.context = [task1, task2]  # Butuh info produk + delivery
    
    print("✅ Setup selesai!\n")
    
    return (
        [storefront, dispatch, merchant],
        [task1, task2, task3]
    )


def scenario_delivery():
    """
    SKENARIO 2: PENGANTARAN BARANG
    
    Workflow:
    1. Calculate Route & Find Driver (Dispatch Agent)
    2. Process Payment (Merchant Agent) - HITL for Wallet
    
    Returns:
        tuple: (agents_list, tasks_list) atau None jika dibatalkan
    """
    print("\n" + "=" * 60)
    print("📦 PENGANTARAN BARANG")
    print("=" * 60)
    
    # Input dari user
    pickup = input("\n📦 Alamat penjemputan (atau ketik 'lokasi saya'): ")
    if not pickup.strip():
        print("❌ Alamat pickup tidak boleh kosong!")
        return None
    
    destination = input("📍 Alamat tujuan: ")
    if not destination.strip():
        print("❌ Alamat tujuan tidak boleh kosong!")
        return None
    
    package_desc = input("📋 Deskripsi paket (optional, tekan Enter untuk skip): ")
    if not package_desc.strip():
        package_desc = "Paket"
    
    # Inisialisasi agents dan tasks
    agents = HoomiAgents()
    tasks = HoomiTasks()
    
    # Create agents (tidak perlu Storefront untuk pure delivery)
    dispatch = agents.dispatch_agent()
    merchant = agents.merchant_agent()
    
    print("\n⚙️  Menyiapkan AI agents...")
    
    # Task 1: Package delivery calculation
    task1 = tasks.package_delivery_task(
        agent=dispatch,
        pickup_address=pickup,
        destination_address=destination,
        package_description=package_desc
    )
    
    # Task 2: Process payment - HITL for Wallet
    estimated_cost = 25000  # Placeholder
    task2 = tasks.payment_task(
        agent=merchant,
        total_amount=estimated_cost,
        recipient_id="DELIVERY_SERVICE",
        description=f"Pengiriman {package_desc}"
    )
    task2.context = [task1]  # Butuh info biaya dari task1
    
    print("✅ Setup selesai!\n")
    
    return (
        [dispatch, merchant],
        [task1, task2]
    )


def scenario_ride():
    """
    SKENARIO 3: ANTAR JEMPUT PENUMPANG
    
    Workflow:
    1. Book Ride & Find Driver (Dispatch Agent) - HITL for GPS
    2. Process Payment (Merchant Agent) - HITL for Wallet
    
    Returns:
        tuple: (agents_list, tasks_list) atau None jika dibatalkan
    """
    print("\n" + "=" * 60)
    print("🚗 ANTAR JEMPUT PENUMPANG")
    print("=" * 60)
    
    # Input dari user
    pickup = input("\n🚗 Lokasi penjemputan (atau ketik 'lokasi saya'): ")
    if not pickup.strip():
        print("❌ Lokasi pickup tidak boleh kosong!")
        return None
    
    destination = input("📍 Tujuan: ")
    if not destination.strip():
        print("❌ Tujuan tidak boleh kosong!")
        return None
    
    try:
        passenger_count = input("👥 Jumlah penumpang (default 1): ")
        passenger_count = int(passenger_count) if passenger_count.strip() else 1
        if passenger_count < 1 or passenger_count > 10:
            print("❌ Jumlah penumpang tidak valid (1-10)!")
            return None
    except ValueError:
        print("❌ Input harus berupa angka!")
        return None
    
    # Inisialisasi agents dan tasks
    agents = HoomiAgents()
    tasks = HoomiTasks()
    
    # Create agents
    dispatch = agents.dispatch_agent()
    merchant = agents.merchant_agent()
    
    print("\n⚙️  Menyiapkan AI agents...")
    
    # Task 1: Ride booking - HITL for GPS
    task1 = tasks.ride_booking_task(
        agent=dispatch,
        pickup_location=pickup,
        destination=destination,
        passenger_count=passenger_count
    )
    
    # Task 2: Process payment - HITL for Wallet
    estimated_fare = 35000  # Placeholder
    task2 = tasks.payment_task(
        agent=merchant,
        total_amount=estimated_fare,
        recipient_id="RIDE_SERVICE",
        description=f"Perjalanan untuk {passenger_count} penumpang"
    )
    task2.context = [task1]  # Butuh info biaya dari task1
    
    print("✅ Setup selesai!\n")
    
    return (
        [dispatch, merchant],
        [task1, task2]
    )


def create_orchestrator_crew(agents_list, tasks_list):
    """
    Buat Crew dengan Hierarchical Process (Orchestrator Mode).
    
    Sesuai TOR B.1:
    - Menggunakan Process.hierarchical
    - Manager LLM sebagai "otak" orchestrator
    - Auto-delegation antar agents
    
    Args:
        agents_list: List of agents
        tasks_list: List of tasks
    
    Returns:
        Crew: Configured crew dengan hierarchical process
    """
    # Setup Manager LLM untuk Hierarchical Process
    manager_llm = LLM(
        model="gemini/gemini-2.0-flash-exp",
        api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7  # Lebih kreatif untuk orchestration
    )
    
    # Create Crew dengan Hierarchical Process
    crew = Crew(
        agents=agents_list,
        tasks=tasks_list,
        process=Process.hierarchical,  # Mode Orchestrator (TOR B.1)
        manager_llm=manager_llm,       # Manager sebagai "otak"
        verbose=True,                  # Untuk debugging
        memory=True,                   # Ingat context antar tasks
        full_output=True               # Return detailed output
    )
    
    return crew


def main():
    """Main entry point untuk Hoomi AI Agent Orchestrator."""
    # Load environment variables
    load_dotenv()
    
    # Validasi API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ ERROR: GOOGLE_API_KEY tidak ditemukan!")
        print("📝 Pastikan file .env berisi: GOOGLE_API_KEY=your_key_here")
        sys.exit(1)
    
    # Print header
    print_header()
    
    # Main loop
    while True:
        # Print menu
        print_menu()
        
        # Get user choice
        choice = input("Pilihan Anda (0-3): ").strip()
        
        # Exit
        if choice == "0":
            print("\n👋 Terima kasih telah menggunakan Hoomi!")
            print("=" * 60 + "\n")
            break
        
        # Process choice
        scenario_result = None
        
        if choice == "1":
            scenario_result = scenario_commerce()
        elif choice == "2":
            scenario_result = scenario_delivery()
        elif choice == "3":
            scenario_result = scenario_ride()
        else:
            print("\n❌ Pilihan tidak valid! Silakan pilih 0-3.\n")
            continue
        
        # Jika user cancel (scenario_result = None)
        if scenario_result is None:
            print("\n🔄 Kembali ke menu utama...\n")
            continue
        
        # Unpack agents dan tasks
        agents_list, tasks_list = scenario_result
        
        # Create orchestrator crew
        print("🤖 Memulai AI Agent Orchestrator...")
        print("=" * 60)
        
        try:
            crew = create_orchestrator_crew(agents_list, tasks_list)
            
            # Execute the crew
            print("\n⏳ Agents sedang bekerja...\n")
            print("💡 CATATAN:")
            print("   - Tool dengan HITL akan meminta approval Anda")
            print("   - Ketik 'yes' untuk approve, atau 'no' untuk reject")
            print("   - Anda akan diminta input saat diperlukan\n")
            print("-" * 60 + "\n")
            
            result = crew.kickoff()
            
            # Display result
            print("\n" + "=" * 60)
            print("✅ HASIL AKHIR")
            print("=" * 60)
            print(result)
            print("=" * 60)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Proses dibatalkan oleh user.")
            print("🔄 Kembali ke menu utama...\n")
            continue
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            print("🔄 Kembali ke menu utama...\n")
            continue
        
        # Ask if continue
        print("\n" + "-" * 60)
        continue_choice = input("Ingin menggunakan layanan lain? (y/n): ").strip().lower()
        if continue_choice != 'y':
            print("\n👋 Terima kasih telah menggunakan Hoomi!")
            print("=" * 60 + "\n")
            break
        
        print("\n")  # Spacing untuk menu berikutnya


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program dihentikan. Terima kasih!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {str(e)}")
        sys.exit(1)