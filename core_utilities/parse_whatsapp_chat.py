#!/usr/bin/env python3
"""
WhatsApp Chat Parser for Dichos Processing
Extracts date_time, contributor, and text from WhatsApp chat exports
Incorporates learnings from fix scripts for robust parsing
"""
import pandas as pd
import re
import os
from datetime import datetime
from difflib import SequenceMatcher
from core_utilities.database_utils import DichosDatabase

def parse_whatsapp_chat(file_path):
    """Parse WhatsApp chat export and extract structured data with improved Unicode handling"""
    print("📱 Parsing WhatsApp chat export...")
    
    messages = []
    current_message = None
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                
                # Enhanced regex pattern to handle Unicode characters and various formats
                # Handles narrow no-break space (U+202F) and other Unicode whitespace
                match = re.match(r'^(\d{1,2}/\d{1,2}/\d{2}),\s*(\d{1,2}:\d{2})\s*([AP]M)\s*-\s*(.+)$', line)
                
                if match:
                    # This is a new message line
                    date_str, time_str, ampm, rest = match.groups()
                    
                    # Parse contributor and text
                    if ':' in rest:
                        contributor, text = rest.split(':', 1)
                        contributor = contributor.strip()
                        text = text.strip()
                    else:
                        contributor = rest.strip()
                        text = ""
                    
                    # Convert WhatsApp date format to database format
                    # WhatsApp: 08/23/25 07:21 PM -> Database: 2025-08-23 19:21:00
                    try:
                        # Parse the date components
                        month, day, year = date_str.split('/')
                        hour, minute = time_str.split(':')
                        
                        # Convert to 24-hour format
                        hour = int(hour)
                        if ampm.upper() == 'PM' and hour != 12:
                            hour += 12
                        elif ampm.upper() == 'AM' and hour == 12:
                            hour = 0
                        
                        # Create datetime object and format as database format
                        dt = datetime(2000 + int(year), int(month), int(day), hour, int(minute))
                        db_date_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                        
                    except ValueError as e:
                        print(f"⚠️  Could not parse date: {date_str} {time_str} {ampm} - {e}")
                        continue
                    
                    # Store previous message if exists
                    if current_message:
                        messages.append(current_message)
                    
                    # Start new message
                    current_message = {
                        'line_num': line_num,
                        'date_time': db_date_time,  # Use database format
                        'contributor': contributor,
                        'text': text
                    }
                    
                elif current_message and line:
                    # This is a continuation line - append to current message
                    current_message['text'] += ' ' + line
        
        # Add the last message
        if current_message:
            messages.append(current_message)
        
        print(f"✅ Parsed {len(messages)} messages")
        return messages
        
    except Exception as e:
        print(f"❌ Error parsing file: {e}")
        return []

def filter_new_messages(messages, cutoff_date_str):
    """Filter messages to only include those newer than the cutoff date"""
    if not messages:
        return []
    
    try:
        # Parse cutoff date (database format: 2025-08-24 10:26:00)
        cutoff_dt = datetime.strptime(cutoff_date_str, '%Y-%m-%d %H:%M:%S')
        print(f"🔍 Filtering messages newer than: {cutoff_date_str}")
        
        new_messages = []
        for msg in messages:
            try:
                msg_dt = datetime.strptime(msg['date_time'], '%Y-%m-%d %H:%M:%S')
                if msg_dt > cutoff_dt:
                    new_messages.append(msg)
            except ValueError as e:
                print(f"⚠️  Could not parse message date {msg['date_time']}: {e}")
                continue
        
        print(f"✅ Found {len(new_messages)} new messages after {cutoff_date_str}")
        return new_messages
        
    except ValueError as e:
        print(f"❌ Error parsing cutoff date {cutoff_date_str}: {e}")
        return messages

def find_contributor_for_dicho(dicho_text, whatsapp_messages, threshold=0.6):
    """Find the original contributor for a dicho using fuzzy matching"""
    best_match = None
    best_score = 0
    
    for msg in whatsapp_messages:
        # Clean both texts for comparison
        clean_dicho = clean_text_for_matching(dicho_text)
        clean_msg = clean_text_for_matching(msg['text'])
        
        # Calculate similarity
        score = SequenceMatcher(None, clean_dicho, clean_msg).ratio()
        
        if score > best_score and score >= threshold:
            best_score = score
            best_match = msg
    
    return best_match['contributor'] if best_match else None

def clean_text_for_matching(text):
    """Clean text for fuzzy matching by removing special characters and normalizing"""
    if not text:
        return ""
    
    # Remove emoticons and special characters
    text = re.sub(r'[😀-]', '', text)
    text = re.sub(r'[^\w\s\.,!?;:\-\(\)]', '', text)
    
    # Normalize whitespace and punctuation
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    
    return text.strip().lower()

def main():
    """Main function to parse WhatsApp chat and filter new messages"""
    print("🚀 WhatsApp Chat Parser for Dichos Processing")
    print("=" * 50)
    
    # Parse the WhatsApp chat
    messages = parse_whatsapp_chat("WhatsApp Chat with Dichosos costarricenses.txt")
    
    if not messages:
        print("❌ No messages parsed")
        return
    
    # Get the most recent date from the database
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
    
    # Filter messages newer than the cutoff date
    new_messages = filter_new_messages(messages, cutoff_date)
    
    if not new_messages:
        print("✅ No new messages found")
        return
    
    # Display summary
    print(f"\n📊 NEW MESSAGES SUMMARY:")
    print(f"   Total new messages: {len(new_messages)}")
    print(f"   Date range: {new_messages[0]['date_time']} to {new_messages[-1]['date_time']}")
    
    # Get unique contributors
    contributors = set(msg['contributor'] for msg in new_messages)
    print(f"   Contributors: {len(contributors)}")
    
    # Show first 10 new messages
    print(f"\n📝 FIRST 10 NEW MESSAGES:")
    for i, msg in enumerate(new_messages[:10], 1):
        print(f"   {msg['date_time']} - {msg['contributor']}: {msg['text'][:50]}{'...' if len(msg['text']) > 50 else ''}")
    
    # Save to CSV
    output_file = 'new_whatsapp_messages.csv'
    df = pd.DataFrame(new_messages)
    df.to_csv(output_file, index=False)
    print(f"\n💾 Saved new messages to: {output_file}")

if __name__ == "__main__":
    main()