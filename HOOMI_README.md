# 🚀 Hoomi AI Agent Orchestrator

**Social Commerce & Ride Fleet Platform**  
Powered by CrewAI + Google Gemini 2.0

---

## 📋 Daftar Isi

- [Overview](#overview)
- [Arsitektur](#arsitektur)
- [Fitur Utama](#fitur-utama)
- [Prerequisites](#prerequisites)
- [Instalasi](#instalasi)
- [Konfigurasi](#konfigurasi)
- [Cara Penggunaan](#cara-penggunaan)
- [Struktur Project](#struktur-project)
- [Compliance dengan TOR](#compliance-dengan-tor)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)

---

## 🎯 Overview

Hoomi AI Agent Orchestrator adalah implementasi **CrewAI** untuk mengelola 3 proses bisnis utama:

1. **🛒 Jual Beli Barang (Commerce)** - Pesan makanan/barang + delivery
2. **📦 Pengantaran Barang (Delivery)** - Kirim paket point-to-point  
3. **🚗 Antar Jemput Penumpang (Ride)** - Booking transportation

### Sesuai TOR Hiliriset

Proyek ini mengikuti **Terms of Reference (TOR) Hiliriset AI Agent Social Commerce dan Ride Fleet Ver0.2**, dengan implementasi:

✅ **Hierarchical Process** - Manager LLM sebagai orchestrator  
✅ **3 AI Agents** - Storefront, Dispatch, Merchant  
✅ **MCP Tools** - Internal & External tool integration  
✅ **Guardrails HITL** - Human-in-the-Loop untuk data sensitif  
✅ **Blockchain Ready** - Persiapan integrasi Ethereum L2 BASE  

---

## 🏗️ Arsitektur

```
┌─────────────────────────────────────────────────────────────┐
│                   USER INPUT (Mobile App)                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│          HOOMI AI ORCHESTRATOR (Hierarchical Process)        │
│                  Manager LLM: Gemini 2.0                     │
└─────┬──────────────────┬────────────────────┬───────────────┘
      │                  │                    │
      ▼                  ▼                    ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│  STOREFRONT  │  │   DISPATCH   │  │    MERCHANT      │
│    AGENT     │  │    AGENT     │  │     AGENT        │
│              │  │              │  │                  │
│ • Search     │  │ • Route      │  │ • Payment (HITL) │
│ • Stock      │  │ • Driver     │  │ • Transaction    │
│ • Recommend  │  │ • GPS (HITL) │  │ • Escrow         │
└──────┬───────┘  └──────┬───────┘  └────────┬─────────┘
       │                 │                   │
       └────────┬────────┴─────────┬─────────┘
                │                  │
                ▼                  ▼
    ┌─────────────────┐  ┌──────────────────┐
    │   MCP TOOLS     │  │   GUARDRAILS     │
    │                 │  │   (HITL)         │
    │ • Commerce      │  │                  │
    │ • Fleet         │  │ • Wallet Access  │
    │ • IoT           │  │ • GPS Access     │
    │ • Notification  │  │ • Data Privacy   │
    └─────────────────┘  └──────────────────┘
```

---

## ✨ Fitur Utama

### 1. Multi-Agent Collaboration

- **Storefront Agent** - Customer service & product search
- **Dispatch Agent** - Logistics & fleet management
- **Merchant Agent** - Transaction & payment handling

### 2. Human-in-the-Loop (HITL) Security

Akses yang **WAJIB** memerlukan persetujuan user:
- ✅ Wallet/Payment (`pay_wallet` tool)
- ✅ GPS Location (`get_user_location` tool)
- ✅ Personal Data
- ✅ IoT Devices

### 3. Intelligent Routing

- GNN-based route optimization
- Real-time traffic consideration
- Driver matching algorithm
- ETA prediction

### 4. Dynamic Response Rendering

Tools menghasilkan structured output:
- Text (generative + data binding)
- Maps (2D route visualization)
- Images (product photos, delivery proof)
- Rich tables (price breakdown)

---

## 📦 Prerequisites

- **Python** >= 3.10
- **pip** package manager
- **Google API Key** (untuk Gemini 2.0)
- **Git** (optional, untuk clone repository)

---

## 🚀 Instalasi

### 1. Clone Repository (atau download files)

```bash
git clone <repository-url>
cd CrewAI_Agent-boilerplate_dari_proyek_Meeting_Prep
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies utama:**
- `crewai==0.28.8`
- `crewai-tools==0.1.6`
- `langchain-google-genai==1.0.1`
- `python-dotenv==1.0.0`

### 3. Verify Installation

```bash
python -c "import crewai; print(crewai.__version__)"
# Expected output: 0.28.8
```

---

## ⚙️ Konfigurasi

### 1. Setup Environment Variables

Buat file `.env` di root directory:

```bash
# Google Gemini API Key (REQUIRED)
GOOGLE_API_KEY=AIzaSyB4GqxVrlv2eq6kmrFrhpoZGlMd6lxnATM

# Optional: LangChain Tracing (untuk debugging)
LANGCHAIN_API_KEY=your_langchain_key_here
LANGCHAIN_TRACING_V2=true
```

### 2. Verify API Key

```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key:', os.getenv('GOOGLE_API_KEY')[:20] + '...')"
```

---

## 🎮 Cara Penggunaan

### Menjalankan Orchestrator

```bash
cd src
python hoomi_main.py
```

### Workflow Interaktif

1. **Pilih Layanan**
   ```
   1. 🛒 Jual Beli Barang
   2. 📦 Pengantaran Barang  
   3. 🚗 Antar Jemput Penumpang
   ```

2. **Input Data**
   - Produk/Paket/Tujuan
   - Alamat pengiriman
   - Jumlah penumpang (untuk ride)

3. **Approve HITL Requests**
   - Ketik `yes` untuk approve GPS access
   - Ketik `yes` untuk approve payment
   - Ketik `no` untuk reject (akan fallback ke alternatif)

4. **Review Results**
   - Detail transaksi
   - Estimasi waktu & biaya
   - Driver information
   - Tracking link

### Contoh Session: Jual Beli Barang

```
📦 Apa yang ingin Anda beli? nasi goreng
📍 Alamat pengiriman: Jl. Sudirman No. 123, Jakarta

⏳ Agents sedang bekerja...

[Storefront Agent] Searching for "nasi goreng"...
✅ Found 2 products

[Dispatch Agent] Requesting GPS access...
❓ Allow GPS access? (yes/no): yes
✅ GPS approved

[Dispatch Agent] Calculating route...
✅ Route calculated: 5.2 km, 18 min

[Merchant Agent] Processing payment...
❓ Approve payment Rp 50,000? (yes/no): yes
✅ Payment successful!

✅ HASIL AKHIR:
Order ID: ORD123456
Status: Confirmed
Driver: Budi Santoso (⭐ 4.8)
ETA Delivery: 18 minutes
```

---

## 📁 Struktur Project

```
CrewAI_Agent-boilerplate_dari_proyek_Meeting_Prep/
│
├── .env                          # Environment variables (API keys)
├── requirements.txt              # Python dependencies
├── HOOMI_README.md              # Documentation (this file)
│
├── TOR - Hiliriset AI Agent...pdf  # Terms of Reference
│
└── src/
    ├── hoomi_main.py            # 🚀 Main orchestrator entry point
    ├── hoomi_agents.py          # 🤖 Agent definitions (3 agents)
    ├── hoomi_tasks.py           # 📋 Task definitions (workflows)
    └── hoomi_tools.py           # 🔧 MCP Tools (8 custom tools)
```

### File Descriptions

| File | Purpose | Key Components |
|------|---------|----------------|
| **hoomi_main.py** | Entry point, UI, orchestration | `scenario_commerce()`, `scenario_delivery()`, `scenario_ride()` |
| **hoomi_agents.py** | Agent factory | `storefront_agent()`, `dispatch_agent()`, `merchant_agent()` |
| **hoomi_tasks.py** | Task factory | `search_product_task()`, `delivery_setup_task()`, `payment_task()` |
| **hoomi_tools.py** | Custom tools/MCP | `@tool` decorators, HITL implementations |

---

## ✅ Compliance dengan TOR

### TOR Section A: Peran dan Tanggung Jawab

| Tim | Requirement | Status | Implementation |
|-----|-------------|--------|----------------|
| **Tim UI** | Pengembangan MCP untuk channeling | ✅ | [`hoomi_agents.py`](src/hoomi_agents.py) - `allow_delegation=True` |
| | Implementasi Guardrails HITL | ✅ | [`hoomi_tools.py`](src/hoomi_tools.py) - `pay_wallet`, `get_user_location` |
| | Optimasi kinerja MCP | ✅ | CrewAI's built-in optimization |
| | Pengembangan workflow AI | ✅ | [`hoomi_tasks.py`](src/hoomi_tasks.py) - 3 business processes |
| | Chain-of-thought prompting | ✅ | Task `description` dengan step-by-step reasoning |

### TOR Section B: Teknologi

| Component | TOR Requirement | Implementation |
|-----------|----------------|----------------|
| **AI Orchestration** | Strands/LangGraph/**CrewAI** | ✅ CrewAI 0.28.8 |
| **LLM** | AWS Bedrock / Gemini | ✅ Gemini 2.0 Flash Exp |
| **Process** | Hierarchical | ✅ `Process.hierarchical` |
| **Guardrails** | HITL for sensitive data | ✅ `human_input=True` on tasks |
| **Vector DB** | pgvector (future) | 🔄 Prepared for RAG |
| **Blockchain** | Ethereum L2 BASE | 🔄 Smart contract ready |

### TOR Section C: Proses Bisnis

| Business Process | Status | Implementation |
|-----------------|--------|----------------|
| 1. Jual Beli Barang | ✅ | `scenario_commerce()` |
| 2. Pengantaran Barang | ✅ | `scenario_delivery()` |
| 3. Antar Jemput Penumpang | ✅ | `scenario_ride()` |

### TOR Section D: Indikator Capaian

| Indicator | Target | Current Status |
|-----------|--------|----------------|
| Success rate integrasi | ≥95% | ✅ Architecture ready |
| Akurasi rekomendasi | ≥70% | 🔄 Perlu training data |
| Error estimasi harga | <5% | 🔄 Perlu tuning |
| Concurrent users | 1000+ | 🔄 Scaling ready (AWS) |
| Latency | <500ms | 🔄 Optimization needed |

**Legend:**  
✅ Implemented | 🔄 Prepared/Partial | ❌ Not implemented

---

## 🐛 Troubleshooting

### Issue: API Key Not Found

```
❌ ERROR: GOOGLE_API_KEY tidak ditemukan!
```

**Solution:**
```bash
# Pastikan file .env ada dan berisi:
GOOGLE_API_KEY=your_actual_key_here

# Verify:
cat .env | grep GOOGLE_API_KEY
```

### Issue: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'crewai'
```

**Solution:**
```bash
pip install -r requirements.txt

# Jika error persist:
pip install --upgrade pip
pip install crewai==0.28.8
```

### Issue: Human Input Not Working

```
Tool pay_wallet tidak meminta approval
```

**Solution:**  
Pastikan task memiliki `human_input=True`:

```python
task = tasks.payment_task(...)
task.human_input = True  # Explicitly set
```

### Issue: Slow Response Time

**Solution:**
1. Gunakan Gemini Flash (bukan Pro): `gemini/gemini-2.0-flash-exp`
2. Reduce `max_iter` di agents
3. Simplify task descriptions
4. Cache responses (future enhancement)

---

## 🗺️ Roadmap

### Phase 1: MVP (Current) ✅
- [x] Core agents implementation
- [x] 3 business processes
- [x] HITL guardrails
- [x] Basic tools (MCP)

### Phase 2: Integration 🔄
- [ ] Hoomi API integration (Commerce, Fleet, Wallet)
- [ ] Google Maps API (real geolocation)
- [ ] Real payment gateway
- [ ] Database (PostgreSQL + pgvector)

### Phase 3: AI Enhancement 📊
- [ ] RAG for product recommendations
- [ ] GNN for route optimization
- [ ] Collaborative filtering
- [ ] Sentiment analysis (reviews)

### Phase 4: Blockchain 🔗
- [ ] Smart contract deployment (Ethereum L2 BASE)
- [ ] Escrow mechanism
- [ ] Transaction tracking
- [ ] Audit trail

### Phase 5: Production 🚀
- [ ] AWS deployment (ECS/EKS)
- [ ] WebSocket for real-time tracking
- [ ] Monitoring & alerting
- [ ] Load testing (1000+ users)
- [ ] Security audit

---

## 📚 Resources

### Documentation
- [CrewAI Documentation](https://docs.crewai.com/)
- [Google Gemini API](https://ai.google.dev/docs)
- [LangChain Google GenAI](https://python.langchain.com/docs/integrations/llms/google_ai)

### TOR Reference
- TOR Document: `TOR - Hiliriset AI Agent Social Commerce dan Ride Fleet.Ver02.pdf`
- Section B.1: Platform dan Infrastruktur
- Section C: Spesifikasi Alur dan Proses Bisnis
- Section D: Indikator Capaian

### Related Projects
- AWS Bedrock Agents
- LangGraph Multi-Agent Systems
- Ethereum L2 BASE Documentation

---

## 👥 Team & Support

**Developer:** Tim Universitas Indonesia  
**Platform:** Hoomi Indonesia  
**Framework:** CrewAI + Google Gemini

**Contact:**
- 📧 Email: support@hoomi.id
- 📱 WhatsApp: +62-xxx-xxxx-xxxx
- 🌐 Website: https://hoomi.id

---

## 📄 License

Proprietary - Hoomi Indonesia © 2024

**Note:** Proyek ini dikembangkan sesuai TOR Hiliriset dan merupakan bagian dari program kemitraan Tim Hoomi dengan Universitas Indonesia.

---

## 🙏 Acknowledgments

- **CrewAI Team** - Untuk framework yang powerful
- **Google** - Untuk Gemini 2.0 API
- **Tim Hoomi** - Untuk vision dan requirements
- **Tim UI** - Untuk kolaborasi development

---

**Happy Coding! 🚀**

*Last Updated: 2024-01-15*