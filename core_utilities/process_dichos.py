#!/usr/bin/env python3
"""
Comprehensive Dicho Processing: Clean, Canonicalize, and Check for Duplicates
Incorporates all learnings from fix scripts for robust processing
"""
import pandas as pd
import re
import sqlite3
import json
from difflib import SequenceMatcher
from core_utilities.database_utils import DichosDatabase

def clean_dicho_text(text):
    """Clean up dicho text by removing emoticons and fixing common issues"""
    if not text:
        return ""
    
    # Remove emoticons and special characters
    text = re.sub(r'[😀-]', '', text)  # Remove emojis
    text = re.sub(r'[^\w\s\.,!?;:\-\(\)]', '', text)  # Keep only letters, numbers, spaces, and basic punctuation
    
    # Clean up extra spaces and punctuation
    text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single space
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)  # Remove space before punctuation
    text = re.sub(r'([.,!?;:])\s*([.,!?;:])', r'\1', text)  # Remove duplicate punctuation
    
    # Fix common spelling issues and canonical forms
    canonical_forms = {
        "que que": "que",
        "mas ": "más ",
        "mas vale": "más vale",
        "diay": "diay",  # Keep Costa Rican "diay"
        "...": ",",  # Replace ellipsis with comma
        "!!": "!",  # Reduce multiple exclamation marks
        "??": "?",  # Reduce multiple question marks
    }
    
    for variation, canonical in canonical_forms.items():
        if variation.lower() in text.lower():
            text = text.replace(variation, canonical)
    
    return text.strip()

def is_semantic_variant(text1, text2):
    """Check if two dichos are semantic variants of each other using improved logic"""
    # Clean both texts
    clean1 = clean_dicho_text(text1).lower()
    clean2 = clean_dicho_text(text2).lower()
    
    # Check for exact match after cleaning
    if clean1 == clean2:
        return True
    
    # Check for high similarity
    similarity = SequenceMatcher(None, clean1, clean2).ratio()
    if similarity > 0.85:
        return True
    
    # Check for common semantic patterns
    patterns = [
        (r'el que se duerme', r'el camaron que se duerme'),
        (r'no hay peor sordo', r'no hay peor ciego'),
        (r'mas perdido que', r'mas perdido que'),
        (r'el que canta', r'el que llora'),
        (r'por un oido', r'por un oído'),
        (r'se le metio', r'se le metió'),
        (r'se le corrieron', r'se le corrieron'),
    ]
    
    for pattern1, pattern2 in patterns:
        if (re.search(pattern1, clean1) and re.search(pattern2, clean2)) or \
           (re.search(pattern2, clean1) and re.search(pattern1, clean2)):
            return True
    
    return False

def find_canonical_form(dicho):
    """Find the canonical form of a dicho using improved heuristics"""
    cleaned = clean_dicho_text(dicho)
    
    # Common canonical form patterns
    canonical_patterns = [
        r'El que se duerme se lo lleva la corriente',
        r'El camaron que se duerme se lo lleva la corriente',
        r'No hay peor sordo que el que no quiere oír',
        r'El que canta su mal espanta',
        r'El que llora su mal empeora',
        r'Por un oído entra y por el otro sale',
        r'A dios rogando y con el mazo dando',
        r'En boca cerrada no entran moscas',
        r'No tiene pelos en la lengua',
        r'Llego por lana y salió trasquilado',
        r'Se quedó durmiendo en los laureles',
        r'Se le metió el agua',
        r'Se le corrieron las tejas',
    ]
    
    # Check if the cleaned text matches any canonical pattern
    for pattern in canonical_patterns:
        if re.search(pattern.lower(), cleaned.lower()):
            return pattern
    
    return cleaned

def identify_true_dichos(messages):
    """Identify actual dichos from WhatsApp messages using improved criteria"""
    dicho_keywords = [
        'mas', 'más', 'que', 'el que', 'no hay', 'por un', 'a dios', 'en boca',
        'llego', 'se quedó', 'feliz como', 'mas perdido', 'mas incómodo',
        'llovieron', 'salió', 'arrieros', 'más metido', 'luz de la calle',
        'el diablo', 'sapo verde', 'agua que no', 'perro que come',
        'no tiene pelos', 'come santos', 'quien quita', 'se le metió',
        'se le corrieron', 'los lunes', 'patitas pa', 'voy sentado',
        'a ojo de buen', 'uno más uno', 'no hay peor cuña', 'las malas conversaciones',
        'las mujeres son como', 'que agua fiestas', 'nunca falta un borracho'
    ]
    
    potential_dichos = []
    
    for msg in messages:
        text = str(msg['text']).strip()
        
        # Skip system messages, media, and very short texts
        if any(skip in text.lower() for skip in [
            '<media omitted>', 'changed the group', 'jajajaja', 'jajaja',
            'this message was edited', 'message was deleted'
        ]):
            continue
        
        # Skip very short texts (likely commentary)
        if len(text) < 10:
            continue
        
        # Check if it contains dicho-like patterns
        if any(keyword in text.lower() for keyword in dicho_keywords):
            potential_dichos.append({
                'original': text,
                'cleaned': clean_dicho_text(text),
                'canonical': find_canonical_form(text),
                'date_time': msg['date_time'],
                'contributor': msg['contributor']
            })
    
    return potential_dichos

def check_duplicates_against_database(new_dichos, db_path):
    """Check for duplicates against the existing database with improved logic"""
    print("🔍 Checking for duplicates against existing database...")
    
    # Get all existing dichos from database
    db = DichosDatabase(db_path)
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, dicho FROM dichos')
    existing_dichos = cursor.fetchall()
    conn.close()
    
    print(f"📊 Found {len(existing_dichos)} existing dichos in database")
    
    duplicates = []
    unique_dichos = []
    
    for i, new_dicho_info in enumerate(new_dichos):
        new_dicho = new_dicho_info['cleaned']
        is_duplicate = False
        duplicate_info = None
        
        for existing_id, existing_dicho in existing_dichos:
            if is_semantic_variant(new_dicho, existing_dicho):
                is_duplicate = True
                duplicate_info = {
                    'new_dicho': new_dicho,
                    'existing_id': existing_id,
                    'existing_dicho': existing_dicho,
                    'similarity': SequenceMatcher(None, 
                        clean_dicho_text(new_dicho).lower(), 
                        clean_dicho_text(existing_dicho).lower()
                    ).ratio()
                }
                break
        
        if is_duplicate:
            duplicates.append(duplicate_info)
            print(f"   ❌ DUPLICATE: '{new_dicho}' -> ID {duplicate_info['existing_id']}: '{duplicate_info['existing_dicho']}'")
        else:
            unique_dichos.append(new_dicho_info)
            print(f"   ✅ UNIQUE: '{new_dicho}'")
    
    return duplicates, unique_dichos

def process_whatsapp_messages(input_file, db_path):
    """Main processing function that handles the complete pipeline"""
    print("🚀 Processing WhatsApp Messages for Dichos")
    print("=" * 60)
    
    # Load new messages
    try:
        df = pd.read_csv(input_file)
        print(f"📱 Loaded {len(df)} WhatsApp messages")
    except FileNotFoundError:
        print(f"❌ Error: {input_file} not found")
        return None, None
    
    # Convert to list of dictionaries
    messages = df.to_dict('records')
    
    # Identify potential dichos
    print(f"\n🎯 Identifying potential dichos...")
    potential_dichos = identify_true_dichos(messages)
    print(f"   Found {len(potential_dichos)} potential dichos")
    
    # Clean and canonicalize
    print(f"\n🧹 Cleaning and canonicalizing dichos...")
    cleaned_dichos = []
    for dicho_info in potential_dichos:
        cleaned = dicho_info['cleaned']
        canonical = dicho_info['canonical']
        
        if cleaned and len(cleaned) > 5:  # Only keep substantial dichos
            cleaned_dichos.append(dicho_info)
            print(f"   '{dicho_info['original']}' -> '{cleaned}'")
    
    print(f"✅ {len(cleaned_dichos)} dichos after cleaning")
    
    # Check for duplicates
    print(f"\n🔍 Checking for duplicates...")
    duplicates, unique_dichos = check_duplicates_against_database(cleaned_dichos, db_path)
    
    print(f"\n📊 DUPLICATE CHECK RESULTS:")
    print(f"   Total potential dichos: {len(cleaned_dichos)}")
    print(f"   Duplicates found: {len(duplicates)}")
    print(f"   Unique dichos: {len(unique_dichos)}")
    
    return unique_dichos, duplicates

def main():
    """Main function for command-line usage"""
    unique_dichos, duplicates = process_whatsapp_messages(
        'new_whatsapp_messages.csv', 
        'core_data/dichos_normalized.db'
    )
    
    if unique_dichos:
        # Save results
        unique_df = pd.DataFrame(unique_dichos)
        output_file = 'unique_new_dichos.tsv'
        unique_df.to_csv(output_file, sep='\t', index=False)
        print(f"\n💾 Saved {len(unique_dichos)} unique dichos to: {output_file}")
        
        # Show first 10 unique dichos
        print(f"\n📝 FIRST 10 UNIQUE DICHOS:")
        for i, row in unique_df.head(10).iterrows():
            print(f"   {i+1:2d}. {row['cleaned']}")
    
    if duplicates:
        print(f"\n🔄 DUPLICATES FOUND:")
        for dup in duplicates[:5]:  # Show first 5 duplicates
            print(f"   '{dup['new_dicho']}' -> ID {dup['existing_id']}: '{dup['existing_dicho']}'")

if __name__ == "__main__":
    main()
