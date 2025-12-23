# CrewAI Meeting Preparation Assistant

![AI Crew Workflow](image.png)

Aplikasi AI Agent yang membantu Anda mempersiapkan meeting dengan lebih efektif menggunakan CrewAI framework. Sistem ini menggunakan multiple AI agents yang bekerja sama untuk melakukan research, analisis industri, dan menyusun strategi meeting.

## 📋 Fitur Utama

- **Research Specialist**: Melakukan riset mendalam tentang peserta meeting dan perusahaan mereka
- **Industry Analyst**: Menganalisis tren industri, tantangan, dan peluang
- **Meeting Strategy Advisor**: Mengembangkan talking points dan strategi meeting
- **Briefing Coordinator**: Menyusun dokumen briefing yang komprehensif

## 🏗️ Arsitektur Sistem

### Tasks & Agents Flow
![Tasks and Agents](image-1.png)
![Detailed Flow](image-2.png)

### Komponen CrewAI:

1. **Task** - Tugas yang akan dikerjakan oleh agents
   - Research Task: Riset peserta dan perusahaan
   - Industry Analysis Task: Analisis industri
   - Meeting Strategy Task: Strategi meeting
   - Summary and Briefing Task: Kompilasi hasil

2. **Agents** - AI yang melakukan task
   - Research Specialist
   - Industry Analyst
   - Meeting Strategy Advisor
   - Briefing Coordinator

3. **Tools** - Tools yang digunakan agents
   - EXASearchTool: Untuk searching dan research di web

4. **Process** - Urutan eksekusi task
   - Sequential & Async execution

## 🚀 Cara Instalasi

### 1. Setup Environment

```bash
# Buat conda environment (opsional tapi direkomendasikan)
conda create --name crewai_meeting python=3.10

# Aktifkan environment
conda activate crewai_meeting
```

### 2. Install Dependencies

```bash
# Install semua package yang diperlukan
pip install -r requirements.txt
```

### 3. Setup API Keys

Buat file `.env` di root folder dan tambahkan API keys:

```properties
OPENAI_API_KEY=your_openai_api_key_here
EXA_API_KEY=your_exa_api_key_here
LANGCHAIN_API_KEY=your_langchain_api_key_here (opsional)
LANGCHAIN_TRACING_V2=true (opsional, untuk debugging)
OPENAI_MODEL_NAME=gpt-3.5-turbo-0125
```

#### Cara Mendapatkan API Keys:

- **OpenAI API Key**: https://platform.openai.com/api-keys
- **EXA API Key**: https://exa.ai/ (untuk search tools)
- **LangChain API Key**: https://smith.langchain.com/ (opsional, untuk tracing)

## 💻 Cara Penggunaan

### Menjalankan Aplikasi

```bash
cd src
python main.py
```

### Input yang Diperlukan

Aplikasi akan meminta 3 input:

1. **Email Peserta Meeting**: Email peserta lain (selain Anda)
   ```
   Contoh: john.doe@company.com, jane.smith@corp.com
   ```

2. **Konteks Meeting**: Topik atau konteks meeting
   ```
   Contoh: investing for cat cafe business
   ```

3. **Objective Meeting**: Tujuan Anda dalam meeting
   ```
   Contoh: securing funding for expansion
   ```

### Contoh Output

Aplikasi akan menghasilkan:
- ✅ Laporan research tentang peserta meeting
- ✅ Analisis industri dan tren terkini
- ✅ Talking points strategis
- ✅ Dokumen briefing lengkap

## 📁 Struktur Project

```
CrewAI_Agent/
│
├── src/
│   ├── main.py           # Entry point aplikasi
│   ├── agents.py         # Definisi AI agents
│   ├── task.py           # Definisi tasks
│   └── tools.py          # Tools untuk agents
│
├── .env                  # API keys (jangan di-commit!)
├── requirements.txt      # Dependencies
└── readme.md            # Dokumentasi
```

## 🔧 Penjelasan Code

### agents.py
Mendefinisikan 4 AI agents dengan role, goal, tools, dan backstory masing-masing.

### task.py
Mendefinisikan 4 tasks yang akan dikerjakan oleh agents:
- `research_task`: Research peserta dan perusahaan
- `industry_analysis_task`: Analisis industri
- `meeting_strategy_task`: Strategi meeting
- `summary_and_briefing_task`: Kompilasi hasil

### tools.py
Menggunakan `EXASearchTool` dari crewai-tools untuk melakukan web search.

### main.py
Orchestrator yang menggabungkan agents, tasks, dan membentuk crew untuk bekerja sama.

## 🛠️ Troubleshooting

### Error: ImportError
```bash
# Pastikan semua package terinstall
pip install -r requirements.txt
```

### Error: API Key tidak valid
```bash
# Cek file .env dan pastikan API keys valid
# Jangan gunakan spasi atau quotes di sekitar nilai
```

### Error: Rate limit
```bash
# Tunggu beberapa saat jika terkena rate limit OpenAI
# Atau upgrade plan OpenAI Anda
```

## 📚 Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [EXA Search API](https://docs.exa.ai/)
- [LangChain Documentation](https://python.langchain.com/)

## 🎯 Tips Penggunaan

1. **Berikan Konteks yang Jelas**: Semakin detail konteks meeting, semakin baik hasil research
2. **Spesifik Objective**: Jelaskan tujuan meeting dengan spesifik
3. **Review Output**: Selalu review output sebelum digunakan di meeting
4. **Customize Agents**: Sesuaikan role dan backstory agents sesuai kebutuhan Anda

## 📝 License

MIT License - Silakan digunakan untuk keperluan apapun

## 👨‍💻 Author

Dibuat untuk keperluan pembelajaran dan produktivitas meeting preparation.

---

**Happy Meeting Prep! 🚀**
