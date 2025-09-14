# LLM Workflow Guide for Dichos Processing

## Overview

The dichos processing system requires **external LLM interaction** for enrichment. The Python scripts handle parsing, cleaning, duplicate detection, and database insertion, but **cannot perform LLM enrichment locally**.

## Workflow Steps

### 1. **Local Processing (Python Scripts)**
These steps run locally and don't require LLM interaction:

- **Parse WhatsApp chat** → `core_utilities/parse_whatsapp_chat.py`
- **Clean and identify dichos** → `core_utilities/process_dichos.py`
- **Check for duplicates** → `core_utilities/process_dichos.py`
- **Insert into database** → `core_utilities/insert_dichos.py`

### 2. **LLM Enrichment (External)**
This step **requires external LLM interaction** and cannot be done locally:

- **Enrich dichos with metadata** → Requires LLM service (GPT-4, Claude, etc.)

## Complete Workflow

### Option A: Automated Pipeline (with simulated enrichment)
```bash
python process_new_whatsapp_dichos.py
```
This runs all steps but uses **simulated enrichment** (hardcoded data).

### Option B: Manual Pipeline (with real LLM enrichment)
```bash
# Step 1: Parse WhatsApp chat
python -c "from core_utilities.parse_whatsapp_chat import main; main()"

# Step 2: Process dichos
python -c "from core_utilities.process_dichos import main; main()"

# Step 3: LLM Enrichment (EXTERNAL - requires LLM service)
# Use an LLM service to enrich unique_new_dichos.tsv
# Save result as enriched_new_dichos.tsv

# Step 4: Insert into database
python -c "from core_utilities.insert_dichos import main; main()"
```

## LLM Enrichment Requirements

### Input File
- **File**: `unique_new_dichos.tsv`
- **Format**: Tab-separated values
- **Columns**: `original`, `cleaned`, `canonical`, `date_time`, `contributor`

### Required Enrichments
For each dicho, the LLM should generate:

1. **Translation** - English equivalent
2. **Expanded Context** - Usage examples and context
3. **Semantic Keywords** - Keywords for clustering
4. **Cultural Context** - Regional usage and cultural notes
5. **Emotion Tone** - Mood and emotional context
6. **Difficulty Level** - Learning difficulty (beginner/intermediate/advanced)
7. **Learning Notes** - Tips for language learners

### Output File
- **File**: `enriched_new_dichos.tsv`
- **Format**: Tab-separated values
- **Required columns**: `dicho`, `translation`, `expanded_context_usage`, `semantic_keywords`, `cultural_context`, `emotion_tone`, `difficulty_level`, `learning_notes`, `date_time`, `contributor_first`, `created_at`, `updated_at`

## LLM Service Integration

### Example LLM Prompt
```
Please enrich this Costa Rican dicho with comprehensive metadata:

Dicho: "Le salió el tiro por la culata"

Please provide:
1. English translation
2. Expanded context and usage examples
3. Semantic keywords (comma-separated)
4. Cultural context and regional usage
5. Emotion tone and mood
6. Difficulty level (beginner/intermediate/advanced)
7. Learning notes for Spanish learners

Format the response as structured data suitable for database insertion.
```

### API Integration Example
```python
# Example of how to integrate with LLM API
def call_llm_for_enrichment(dicho_text):
    prompt = f"Enrich this Costa Rican dicho: {dicho_text}"
    response = llm_api_call(prompt)
    return parse_llm_response(response)
```

## Current Limitations

1. **No LLM API Integration** - The current system uses hardcoded dictionaries
2. **Simulated Enrichment** - Not suitable for production use
3. **Manual Process** - Requires external LLM service interaction

## Recommendations

1. **For Development/Testing**: Use the automated pipeline with simulated enrichment
2. **For Production**: Implement real LLM API integration
3. **For Batch Processing**: Use external LLM service to process `unique_new_dichos.tsv`

## Files Created During Processing

- `new_whatsapp_messages.csv` - Parsed WhatsApp messages
- `unique_new_dichos.tsv` - Cleaned, unique dichos (input for LLM)
- `enriched_new_dichos.tsv` - LLM-enriched dichos (output from LLM)
- Database updates - New dichos inserted with relationships

## Error Handling

- **Missing LLM enrichment**: The system will use simulated data
- **Invalid enrichment format**: Check TSV column structure
- **Database insertion errors**: Verify enrichment data format

---

**Note**: This workflow is designed to be flexible and allow for different LLM service integrations while maintaining the core processing pipeline.
