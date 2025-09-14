# DATABASE MAINTENANCE GUIDE
## Adding New Dichos and Maintaining Database Integrity

This guide provides a step-by-step process for maintaining and updating the `dichos_normalized.db` database when new Costa Rican dichos are discovered. The process ensures data quality, maintains semantic clustering, and keeps the database clean and efficient.

---

## 📋 **PREREQUISITES**

### **Required Environment:**
- Python 3.12+ with virtual environment
- SQLite3 database: `dichos_normalized.db`
- Access to LLM services (OpenAI, Anthropic, etc.) for text analysis
- Local NLP capabilities for semantic clustering

### **Current Database State:**
- **301 dichos** across **13 semantic clusters**
- **Multi-cluster assignments** (up to 3 per dicho)
- **Enhanced clusters** with descriptions and icons
- **Clean schema** with no redundant tables

---

## 🔄 **MAINTENANCE WORKFLOW OVERVIEW**

```
WhatsApp Dump → Parse & Extract → Filter New → LLM Analysis → Enrich Data → NLP Clustering → Update Database → Clean & Optimize
```

---

## 📥 **STEP 1: READ AND PARSE WHATSAPP TEXT DUMP**

### **Objective:** Extract datetime, contributor, and text from new WhatsApp chat export

### **Process:**
1. **Obtain new WhatsApp export** (text format) - typically named `WhatsApp Chat with [Group Name].txt`
2. **Use the WhatsApp parser script**: `core_utilities/parse_whatsapp_chat.py`
3. **Parse each line** to extract:
   - `date_time`: Timestamp of message (M/D/YY H:MM AM/PM format)
   - `contributor`: Sender name or phone number
   - `text`: Full message content (including continuation lines)

### **WhatsApp Export Format:**
```
8/17/25, 4:48 PM - Javier Soto: Ahi poco a poco añado mas gente.  Hoy hablaba con Randall de los dichos costarricenses y le decía que tenia la misma idea.  Asi que pongan los dichos q se sepan.  Si saben de donde vienen y un ejemplo de como se usa.
8/17/25, 4:58 PM - Javier Soto: Y recuerdense:  no se haga la barba en seco.
8/17/25, 6:11 PM - Maria Goodwin: A palabras necias, oidos sordos
```

### **Special Considerations:**
- **Continuation lines**: Lines not starting with dates are continuations of previous messages
- **System messages**: Skip lines containing "created group", "added", "changed", etc.
- **Unicode characters**: Handle special characters between time and AM/PM
- **Encoding**: Use UTF-8 with error handling

### **Parser Script Usage:**
```bash
# Activate virtual environment
source venv/bin/activate

# Run the parser
python3 core_utilities/parse_whatsapp_chat.py
```

### **Output:** 
- **Console summary** of parsing results
- **CSV file**: `new_whatsapp_messages.csv` with columns: `line_num`, `date_time`, `contributor`, `text`
- **Filtered messages**: Only messages newer than the most recent date in the database

### **Example Output:**
```
🚀 WhatsApp Chat Parser for Dichos Processing
==================================================
📱 Parsing WhatsApp chat export...
✅ Parsed 53 messages
📅 Database cutoff date: 8/23/25 6:56 AM
🔍 Filtering messages newer than: 8/23/25 6:56 AM
✅ Found 53 new messages after 8/23/25 6:56 AM

📊 NEW MESSAGES SUMMARY:
   Total new messages: 53
   Date range: 8/23/25 08:18 AM to 8/29/25 02:38 PM
   Contributors: 8
💾 Saved new messages to: new_whatsapp_messages.csv
```

### **File Organization:**
- **Parser script**: `core_utilities/parse_whatsapp_chat.py`
- **Input file**: `WhatsApp Chat with [Group Name].txt` (place in project root)
- **Output file**: `new_whatsapp_messages.csv` (generated in project root)
- **Database**: `core_data/dichos_normalized.db`

---

## 🆕 **STEP 2: IDENTIFY NEW DICHOS**

### **Objective:** Determine which rows contain new dichos based on timestamp comparison

### **Process:**
1. **Query current database** for most recent `date_time`:
   ```sql
   SELECT MAX(date_time) FROM dichos;
   ```

2. **Filter new rows** where `date_time > most_recent_in_db`

3. **Remove duplicates** by comparing text content with existing dichos

4. **Identify potential dichos** vs. commentary (preliminary filtering)

### **Output:** List of new, unique messages that need processing

---

## 🤖 **STEP 3: LLM ANALYSIS - DICHO IDENTIFICATION**

### **Objective:** Use LLM to determine which new rows contain actual Spanish dichos vs. commentary

### **Process:**
1. **Send new messages to LLM** with prompt:
   ```
   Analyze this WhatsApp message and determine if it contains a Costa Rican dicho (proverb/saying):
   
   Message: [MESSAGE_TEXT]
   Sender: [CONTRIBUTOR]
   Timestamp: [DATETIME]
   
   Respond with:
   - IS_DICHO: true/false
   - REASON: Brief explanation
   - SPANISH_TEXT: Extract the dicho if present
   - CONFIDENCE: 0-1 score
   ```

2. **Filter results** to keep only rows where `IS_DICHO = true` and `CONFIDENCE > 0.7`

3. **Extract Spanish text** for confirmed dichos

### **Output:** Filtered list of confirmed new dichos with extracted Spanish text

---

## 🎯 **STEP 4: LLM ENRICHMENT - COMPLETE METADATA**

### **Objective:** Use LLM to enrich each new dicho with complete metadata matching existing schema

### **Process:**
1. **For each confirmed dicho**, send to LLM with enrichment prompt:
   ```
   Enrich this Costa Rican dicho with complete metadata:
   
   Dicho: [SPANISH_TEXT]
   
   Provide:
   - translation: English translation
   - expanded_context_usage: Detailed explanation of when/how to use
   - semantic_keywords: 5-10 English keywords capturing meaning
   - cultural_context: Cultural background (Tico-specific or universal)
   - emotion_tone: Emotional tone (advice, warning, humor, etc.)
   - difficulty_level: 1-5 scale for learners
   - learning_notes: Language learning insights
   ```

2. **Validate LLM output** for consistency and quality
3. **Standardize semantic_keywords** (lowercase, underscore_separated, no duplicates)

### **Output:** Enriched dichos with complete metadata matching existing schema

---

## 🔍 **STEP 5: KEYWORD ANALYSIS AND CLUSTER COMPATIBILITY**

### **Objective:** Analyze new semantic keywords and ensure they fit within existing cluster structure

### **Process:**
1. **Extract all new semantic_keywords** from new dichos
2. **Compare with existing keywords** in clusters table:
   ```sql
   SELECT DISTINCT keywords FROM clusters;
   ```
3. **Identify new keywords** that don't exist in current clusters
4. **Analyze semantic compatibility** with existing clusters
5. **Plan cluster expansion** if new keywords require new clusters

### **Output:** Assessment of whether new dichos fit existing clusters or require schema changes

---

## 🧠 **STEP 6: NLP RECLUSTERING (LOCAL PROCESSING)**

### **Objective:** Use local NLP capabilities to assign new dichos to existing clusters

### **Process:**
1. **Load existing clustering model** (SentenceTransformer 'all-MiniLM-L6-v2')
2. **Generate embeddings** for:
   - All existing cluster keywords
   - New dicho semantic_keywords
3. **Calculate similarity scores** between new dichos and existing clusters
4. **Assign clusters** using same logic as current system:
   - Primary cluster (best match)
   - Secondary clusters (within 10% gap or above 0.35 threshold)
   - Tertiary clusters (above 0.3 threshold)
   - Maximum 3 clusters per dicho

### **Output:** Cluster assignments for all new dichos

---

## 🗄️ **STEP 7: DATABASE UPDATES**

### **Objective:** Insert new dichos and update all related tables

### **Process:**
1. **Insert new dichos** into `dichos` table
2. **Insert cluster assignments** into `multi_cluster_assignments` table
3. **Update cluster sizes** in `clusters` table
4. **Verify foreign key constraints** and relationships
5. **Update any derived data** (e.g., total counts, statistics)

### **Output:** Updated database with new dichos and cluster assignments

---

## 🧹 **STEP 8: DATABASE CLEANUP AND OPTIMIZATION**

### **Objective:** Maintain database performance and cleanliness

### **Process:**
1. **Reindex database** for optimal performance:
   ```sql
   REINDEX;
   ```

2. **Update statistics** for query optimizer:
   ```sql
   ANALYZE;
   ```

3. **Verify data integrity**:
   - Check foreign key relationships
   - Validate cluster assignments
   - Confirm no orphaned records

4. **Clean up temporary files** and intermediate data

### **Output:** Clean, optimized database ready for application use

---

## 📊 **STEP 9: VALIDATION AND TESTING**

### **Objective:** Ensure new data maintains quality and system integrity

### **Process:**
1. **Verify cluster distributions** are reasonable
2. **Test semantic similarity** calculations
3. **Validate multi-cluster assignments** follow established rules
4. **Check application queries** still work correctly
5. **Update documentation** with new cluster sizes and statistics

### **Output:** Validated system ready for production use

---

## 🚨 **IMPORTANT CONSIDERATIONS**

### **Data Quality:**
- **LLM outputs** should be validated for consistency
- **Semantic keywords** must follow established format
- **Cluster assignments** should maintain semantic coherence

### **Performance:**
- **Batch processing** for large numbers of new dichos
- **Incremental updates** to avoid full reclustering
- **Regular maintenance** to prevent database bloat

### **Scalability:**
- **Monitor cluster sizes** as they grow
- **Consider cluster splitting** if any become too large
- **Plan for keyword expansion** in existing clusters

---

## 🔧 **TECHNICAL IMPLEMENTATION NOTES**

### **Required Python Packages:**
```bash
pip install sentence-transformers pandas sqlite3 numpy plotly
```

### **Database Schema Changes:**
- **No schema changes** required for adding new dichos
- **Cluster sizes** will update automatically
- **Multi-cluster assignments** will expand as needed

### **File Management:**
- **Backup database** before major updates
- **Version control** for enrichment scripts
- **Log all changes** for audit purposes

---

## 📈 **MONITORING AND MAINTENANCE**

### **Regular Tasks:**
- **Weekly**: Check for new WhatsApp exports
- **Monthly**: Review cluster distributions and quality
- **Quarterly**: Full database optimization and cleanup

### **Metrics to Track:**
- **Total dichos** and growth rate
- **Cluster sizes** and distribution
- **Semantic keyword coverage**
- **Database performance** and query times

---

## 🆘 **TROUBLESHOOTING**

### **Common Issues:**
1. **LLM API limits** - Implement rate limiting and retry logic
2. **Cluster assignment failures** - Check similarity score thresholds
3. **Database performance** - Regular reindexing and cleanup
4. **Data consistency** - Validate LLM outputs before insertion

### **Recovery Procedures:**
- **Database rollback** from backups if needed
- **Partial reinsertion** of failed records
- **Manual cluster assignment** for edge cases

---

## 📚 **RESOURCES AND REFERENCES**

### **Current System Documentation:**
- `ENHANCED_CLUSTERS_SUMMARY.md` - Cluster descriptions and icons
- `optimized_multi_cluster_queries.sql` - Query examples
- `DATABASE_CLEANUP_SUMMARY.md` - Schema optimization details

### **NLP Model Information:**
- **Model**: `all-MiniLM-L6-v2`
- **Embedding dimensions**: 384
- **Similarity calculation**: Cosine similarity
- **Clustering method**: K-means with silhouette analysis

---

## ✅ **SUCCESS CRITERIA**

### **Maintenance Complete When:**
- [ ] All new dichos processed and enriched
- [ ] Cluster assignments completed
- [ ] Database updated and optimized
- [ ] Data integrity verified
- [ ] Application functionality tested
- [ ] Documentation updated

---

*This guide should be used in conjunction with the current database schema and clustering system. Always backup the database before making changes and test thoroughly in a development environment first.*

### **Parser Script Usage:**
```bash
# Activate virtual environment
source venv/bin/activate

# Run the parser
python3 core_utilities/parse_whatsapp_chat.py
```

### **File Organization:**
- **Parser script**: `core_utilities/parse_whatsapp_chat.py`
- **Input file**: `WhatsApp Chat with [Group Name].txt` (place in project root)
- **Output file**: `new_whatsapp_messages.csv` (generated in project root)
- **Database**: `core_data/dichos_normalized.db`
