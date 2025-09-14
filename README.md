# DICHOS PROCESSING SYSTEM
## Costa Rican Proverbs Semantic Clustering Database

A production-ready system for managing and semantically clustering Costa Rican dichos (proverbs) using NLP techniques.

---

## 🏗️ **PROJECT STRUCTURE**

```
dichos_processing/
├── 📊 core_data/                    # Core data and database
│   ├── dichos_normalized.db         # Main SQLite database (301 dichos, 13 clusters)
│   └── data/                        # Original data sources
│       └── dichos_enhanced_batches.tsv
├── 🔧 core_utilities/               # Essential utilities
│   ├── database_utils.py            # Database interaction utilities
│   ├── parse_whatsapp_chat.py      # WhatsApp chat export parser
│   ├── process_dichos.py            # Dicho processing and duplicate detection
│   ├── enrich_dichos.py             # LLM enrichment and metadata generation
│   └── insert_dichos.py             # Database insertion with relationships
├── 📋 requirements.txt               # Python package dependencies
├── 🧠 core_algorithms/              # Core NLP and clustering algorithms
│   ├── nlp_semantic_clustering.py   # Main clustering algorithm
│   └── multi_cluster_assignment_method.py  # Multi-cluster assignment logic
├── 📚 documentation/                 # Complete system documentation
│   ├── DATABASE_MAINTENANCE_GUIDE.md    # Step-by-step maintenance procedures
│   ├── ENHANCED_CLUSTERS_SUMMARY.md     # Current cluster state and descriptions
│   ├── ESSENTIAL_FILES_SUMMARY.md       # Project overview and database schema
│   └── PROJECT_CLEANUP_SUMMARY.md      # Cleanup operation summary
├── 🗄️ database_queries/             # Essential SQL queries
│   └── optimized_multi_cluster_queries.sql
├── 🐍 venv/                         # Python virtual environment
└── README.md                        # This file
```

---

## 🚀 **QUICK START**

### **1. Environment Setup:**
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies (if needed)
pip install -r requirements.txt

# Verify packages are installed
pip list | grep -E "(sentence-transformers|pandas|numpy|plotly)"
```

### **2. Database Access:**
```python
from core_utilities.database_utils import DatabaseManager

# Connect to database
db = DatabaseManager('core_data/dichos_normalized.db')

# Query current state
clusters = db.execute_query("SELECT * FROM clusters")
print(f"System has {len(clusters)} semantic clusters")
```

### **3. View Current Clusters:**
```bash
# Check cluster overview
cat documentation/ENHANCED_CLUSTERS_SUMMARY.md
```

---

## 📊 **CURRENT SYSTEM STATE**

- **Total Dichos**: 301 Costa Rican proverbs
- **Semantic Clusters**: 13 meaningful categories
- **Cluster Assignment**: Up to 3 clusters per dicho
- **Database Schema**: Fully optimized and clean
- **NLP Model**: Sentence Transformers (all-MiniLM-L6-v2)

---

## 🔄 **MAINTENANCE OPERATIONS**

### **Adding New Dichos:**
1. **Follow the complete guide**: `documentation/DATABASE_MAINTENANCE_GUIDE.md`
2. **Use core algorithms**: Scripts in `core_algorithms/`
3. **Update database**: Via utilities in `core_utilities/`

### **Key Maintenance Scripts:**
- **`process_new_whatsapp_dichos.py`**: Complete pipeline for new WhatsApp dichos
- **`core_utilities/parse_whatsapp_chat.py`**: WhatsApp chat parsing
- **`core_utilities/process_dichos.py`**: Dicho cleaning and duplicate detection
- **`core_utilities/enrich_dichos.py`**: LLM enrichment and metadata
- **`core_utilities/insert_dichos.py`**: Database insertion with relationships
- **`core_algorithms/nlp_semantic_clustering.py`**: Reclustering with new data

---

## 📋 **REQUIREMENTS**

### **Python Packages:**
- **sentence-transformers**: NLP embeddings
- **pandas**: Data manipulation
- **numpy**: Numerical operations
- **plotly**: Visualizations (optional)
- **sqlite3**: Database operations (built-in)

### **System Requirements:**
- **Python**: 3.12+
- **Memory**: 4GB+ RAM for NLP operations
- **Storage**: 2GB+ free space
- **No GPU required**: CPU-only processing

---

## 🎯 **USE CASES**

### **For Application Development:**
- **Semantic search** of dichos by meaning
- **Cluster-based navigation** through proverb categories
- **Multi-language support** (Spanish + English)
- **Cultural context** and usage examples

### **For Research:**
- **Linguistic analysis** of Costa Rican proverbs
- **Cultural studies** and folklore research
- **Language learning** resource development
- **Semantic similarity** analysis

---

## 📚 **DOCUMENTATION INDEX**

| File | Purpose | Status |
|------|---------|---------|
| `DATABASE_MAINTENANCE_GUIDE.md` | Complete maintenance procedures | ✅ Complete |
| `ENHANCED_CLUSTERS_SUMMARY.md` | Current cluster state | ✅ Current |
| `ESSENTIAL_FILES_SUMMARY.md` | System overview | ✅ Reference |
| `PROJECT_CLEANUP_SUMMARY.md` | Cleanup summary | ✅ Historical |

---

## 🔧 **DEVELOPMENT NOTES**

### **File Organization:**
- **Logical grouping** by function and purpose
- **Clear separation** of concerns
- **Easy navigation** for new developers
- **Maintenance-friendly** structure

### **Best Practices:**
- **Always backup** database before major changes
- **Test scripts** in development environment first
- **Follow maintenance guide** step-by-step
- **Validate results** after each operation

---

## 🆘 **SUPPORT**

### **For Maintenance Issues:**
1. **Check documentation** in `documentation/` folder
2. **Review maintenance guide** for step-by-step procedures
3. **Use database queries** in `database_queries/` for troubleshooting
4. **Verify environment** with utilities in `core_utilities/`

### **Common Operations:**
- **Adding new dichos**: See maintenance guide
- **Reclustering data**: Use NLP clustering script
- **Database queries**: Reference SQL examples
- **System updates**: Follow documented procedures

---

## 📈 **FUTURE ENHANCEMENTS**

### **Planned Features:**
- **Web interface** for dicho management
- **API endpoints** for application integration
- **Advanced analytics** and reporting
- **Multi-language expansion** beyond Spanish/English

### **Scalability Considerations:**
- **Cluster management** for growing collections
- **Performance optimization** for large datasets
- **Backup and recovery** procedures
- **Monitoring and alerting** systems

---

*This system represents a production-ready semantic clustering solution for Costa Rican dichos, with comprehensive documentation and maintenance procedures for ongoing operations.*
