#!/usr/bin/env python3
"""
Complete Pipeline for Processing New WhatsApp Dichos
Orchestrates the entire process from parsing to database insertion

IMPORTANT: This pipeline requires LLM interaction for enrichment.
The enrichment step must be done externally using an LLM service.
"""
import os
import sys
from core_utilities.parse_whatsapp_chat import parse_whatsapp_chat, filter_new_messages
from core_utilities.process_dichos import process_whatsapp_messages
from core_utilities.insert_dichos import insert_dichos_from_file
from core_utilities.database_utils import DichosDatabase

def main():
    """Main processing pipeline"""
    print("🚀 Complete WhatsApp Dichos Processing Pipeline")
    print("=" * 60)
    print("⚠️  NOTE: This pipeline requires LLM interaction for enrichment")
    print("   The enrichment step must be done externally using an LLM service")
    print("=" * 60)
    
    # Step 1: Parse WhatsApp chat
    print("\n📱 STEP 1: Parsing WhatsApp Chat")
    print("-" * 40)
    
    whatsapp_file = "WhatsApp Chat with Dichosos costarricenses.txt"
    if not os.path.exists(whatsapp_file):
        print(f"❌ Error: {whatsapp_file} not found")
        return
    
    messages = parse_whatsapp_chat(whatsapp_file)
    if not messages:
        print("❌ No messages parsed")
        return
    
    # Get cutoff date from database
    try:
        db = DichosDatabase('core_data/dichos_normalized.db')
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(date_time) FROM dichos')
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0]:
            cutoff_date = result[0]
            print(f"📅 Database cutoff date: {cutoff_date}")
        else:
            print("⚠️  No date found in database, processing all messages")
            cutoff_date = "1900-01-01 00:00:00"
            
    except Exception as e:
        print(f"⚠️  Could not get database cutoff date: {e}")
        print("Processing all messages...")
        cutoff_date = "1900-01-01 00:00:00"
    
    # Filter new messages
    new_messages = filter_new_messages(messages, cutoff_date)
    if not new_messages:
        print("✅ No new messages found")
        return
    
    # Save new messages
    import pandas as pd
    df = pd.DataFrame(new_messages)
    df.to_csv('new_whatsapp_messages.csv', index=False)
    print(f"💾 Saved {len(new_messages)} new messages to new_whatsapp_messages.csv")
    
    # Step 2: Process dichos
    print("\n🎯 STEP 2: Processing Dichos")
    print("-" * 40)
    
    unique_dichos, duplicates = process_whatsapp_messages(
        'new_whatsapp_messages.csv', 
        'core_data/dichos_normalized.db'
    )
    
    if not unique_dichos:
        print("✅ No new unique dichos found")
        return
    
    # Save unique dichos
    unique_df = pd.DataFrame(unique_dichos)
    unique_df.to_csv('unique_new_dichos.tsv', sep='\t', index=False)
    print(f"💾 Saved {len(unique_dichos)} unique dichos to unique_new_dichos.tsv")
    
    # Step 3: LLM Enrichment (EXTERNAL STEP REQUIRED)
    print("\n🤖 STEP 3: LLM Enrichment (EXTERNAL STEP REQUIRED)")
    print("-" * 40)
    print("⚠️  THIS STEP REQUIRES EXTERNAL LLM INTERACTION")
    print("   The enrichment cannot be done locally by the Python scripts")
    print("   You need to:")
    print("   1. Use an LLM service (GPT-4, Claude, etc.) to enrich the dichos")
    print("   2. Generate translations, context, keywords, cultural notes, etc.")
    print("   3. Save the enriched data as 'enriched_new_dichos.tsv'")
    print("   4. Then run the database insertion step")
    print("\n   For now, using simulated enrichment (not recommended for production)")
    
    # Use simulated enrichment for demonstration
    from core_utilities.enrich_dichos import enrich_dichos_from_file
    enrich_dichos_from_file('unique_new_dichos.tsv', 'enriched_new_dichos.tsv')
    
    # Step 4: Insert into database
    print("\n💾 STEP 4: Inserting into Database")
    print("-" * 40)
    
    insert_dichos_from_file('enriched_new_dichos.tsv', 'core_data/dichos_normalized.db')
    
    # Final summary
    print("\n🎉 PROCESSING COMPLETE!")
    print("=" * 60)
    print(f"✅ Processed {len(new_messages)} new WhatsApp messages")
    print(f"✅ Identified {len(unique_dichos)} unique dichos")
    print(f"✅ Found {len(duplicates)} duplicates (not added)")
    print(f"✅ Enriched and inserted {len(unique_dichos)} dichos into database")
    print("\n⚠️  NOTE: This used simulated enrichment.")
    print("   For production, use a real LLM service for enrichment.")
    
    # Show final database status
    try:
        db = DichosDatabase('core_data/dichos_normalized.db')
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM dichos')
        total_dichos = cursor.fetchone()[0]
        conn.close()
        print(f"📊 Total dichos in database: {total_dichos}")
    except Exception as e:
        print(f"⚠️  Could not verify final database status: {e}")

if __name__ == "__main__":
    main()
