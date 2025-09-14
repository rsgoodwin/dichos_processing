#!/usr/bin/env python3
"""
Comprehensive Database Insertion for Dichos
Handles all related tables: dichos, english_proverbs, dicho_proverb_relationships, multi_cluster_assignments
Incorporates all learnings from insertion scripts
"""
import pandas as pd
import sqlite3
import json
from datetime import datetime
from core_utilities.database_utils import DichosDatabase

def get_existing_clusters(db_path):
    """Get all existing clusters from the database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get clusters
    cursor.execute('SELECT id, name, description FROM clusters ORDER BY id')
    clusters = cursor.fetchall()
    
    # Get cluster assignments
    cursor.execute('SELECT dicho_id, cluster_id, similarity_score FROM multi_cluster_assignments')
    assignments = cursor.fetchall()
    
    conn.close()
    
    return clusters, assignments

def assign_dichos_to_clusters(new_dichos, existing_clusters, existing_assignments):
    """Assign new dichos to existing clusters based on semantic keywords"""
    cluster_assignments = []
    
    # Create a mapping of cluster_id to cluster_name for reference
    cluster_map = {cluster[0]: cluster[1] for cluster in existing_clusters}
    
    # Get existing dicho assignments to understand patterns
    existing_dicho_clusters = {}
    for dicho_id, cluster_id, strength in existing_assignments:
        if dicho_id not in existing_dicho_clusters:
            existing_dicho_clusters[dicho_id] = []
        existing_dicho_clusters[dicho_id].append((cluster_id, strength))
    
    # Define keyword-to-cluster mapping based on semantic analysis
    keyword_cluster_mapping = {
        # Wisdom and Philosophy
        'wisdom': [1, 2, 3],
        'philosophy': [1, 2, 3],
        'wise': [1, 2, 3],
        'practical': [1, 2, 3],
        
        # Humor and Irony
        'humor': [4, 5, 6],
        'ironic': [4, 5, 6],
        'humorous': [4, 5, 6],
        'playful': [4, 5, 6],
        
        # Social and Relationships
        'social': [7, 8, 9],
        'relationships': [7, 8, 9],
        'community': [7, 8, 9],
        'interference': [7, 8, 9],
        
        # Work and Productivity
        'work': [10, 11, 12],
        'productivity': [10, 11, 12],
        'effort': [10, 11, 12],
        'achievement': [10, 11, 12],
        
        # Emotions and Psychology
        'emotions': [13, 14, 15],
        'happiness': [13, 14, 15],
        'sadness': [13, 14, 15],
        'confusion': [13, 14, 15],
        
        # Religion and Faith
        'religion': [16, 17, 18],
        'faith': [16, 17, 18],
        'prayer': [16, 17, 18],
        'hypocrisy': [16, 17, 18],
        
        # Nature and Environment
        'nature': [19, 20, 21],
        'water': [19, 20, 21],
        'animals': [19, 20, 21],
        'environment': [19, 20, 21]
    }
    
    for i, dicho in enumerate(new_dichos, 1):
        # Parse semantic keywords
        keywords_str = dicho.get('semantic_keywords', '')
        if isinstance(keywords_str, str):
            keywords = [k.strip() for k in keywords_str.split(',')]
        else:
            keywords = []
        
        # Find matching clusters based on keywords
        matching_clusters = set()
        for keyword in keywords:
            keyword_lower = keyword.lower()
            for category, cluster_ids in keyword_cluster_mapping.items():
                if category in keyword_lower or keyword_lower in category:
                    matching_clusters.update(cluster_ids)
        
        # If no matches found, assign to general clusters (1, 2, 3)
        if not matching_clusters:
            matching_clusters = {1, 2, 3}
        
        # Assign to top 3 matching clusters with decreasing strength
        cluster_list = list(matching_clusters)[:3]
        for j, cluster_id in enumerate(cluster_list):
            strength = 0.9 - (j * 0.2)  # Decreasing strength: 0.9, 0.7, 0.5
            cluster_assignments.append({
                'dicho_id': i,
                'cluster_id': cluster_id,
                'assignment_strength': strength,
                'assignment_method': 'semantic_keyword_matching'
            })
    
    return cluster_assignments

def insert_english_equivalents(english_equivalents, db_path):
    """Insert English equivalents into the english_proverbs table"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get next available ID
    cursor.execute('SELECT MAX(id) FROM english_proverbs')
    max_id = cursor.fetchone()[0]
    next_id = (max_id + 1) if max_id else 1
    
    inserted_equivalents = []
    
    for i, equivalent in enumerate(english_equivalents, next_id):
        # Check if equivalent already exists
        cursor.execute('SELECT id FROM english_proverbs WHERE proverb = ?', (equivalent,))
        existing = cursor.fetchone()
        
        if existing:
            inserted_equivalents.append(existing[0])
            continue
        
        # Insert new equivalent
        cursor.execute('''
            INSERT INTO english_proverbs (
                id, proverb, word_count, char_count, origin, 
                difficulty_level, category, formality_level, 
                usage_count, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            i, 
            equivalent, 
            len(equivalent.split()),  # word_count
            len(equivalent),  # char_count
            'Costa Rican Spanish',  # origin
            2,  # difficulty_level (intermediate)
            'Proverb',  # category
            'Informal',  # formality_level
            0,  # usage_count
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        inserted_equivalents.append(i)
    
    conn.commit()
    conn.close()
    
    return inserted_equivalents

def insert_dichos_with_relationships(new_dichos, english_equivalent_ids, db_path):
    """Insert dichos and create relationships with English equivalents"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get next available dicho ID
    cursor.execute('SELECT MAX(id) FROM dichos')
    max_dicho_id = cursor.fetchone()[0]
    next_dicho_id = (max_dicho_id + 1) if max_dicho_id else 1
    
    inserted_dicho_ids = []
    
    for i, dicho in enumerate(new_dichos, next_dicho_id):
        # Insert dicho
        cursor.execute('''
            INSERT INTO dichos (
                id, dicho, translation, expanded_context_usage, semantic_keywords,
                cultural_context, emotion_tone, difficulty_level, learning_notes,
                date_time, contributor_first, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            i,
            dicho['dicho'],
            dicho['translation'],
            dicho['expanded_context_usage'],
            dicho['semantic_keywords'],
            dicho['cultural_context'],
            dicho['emotion_tone'],
            dicho['difficulty_level'],
            dicho['learning_notes'],
            dicho['date_time'],
            dicho['contributor_first'],
            dicho['created_at'],
            dicho['updated_at']
        ))
        
        inserted_dicho_ids.append(i)
        
        # Create relationship with English equivalent
        if i - next_dicho_id < len(english_equivalent_ids):
            english_id = english_equivalent_ids[i - next_dicho_id]
            
            # Get next relationship ID
            cursor.execute('SELECT MAX(id) FROM dicho_proverb_relationships')
            max_rel_id = cursor.fetchone()[0]
            next_rel_id = (max_rel_id + 1) if max_rel_id else 1
            
            cursor.execute('''
                INSERT INTO dicho_proverb_relationships (
                    id, dicho_id, proverb_id, created_at
                ) VALUES (?, ?, ?, ?)
            ''', (
                next_rel_id,
                i,
                english_id,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
    
    conn.commit()
    conn.close()
    
    return inserted_dicho_ids

def insert_cluster_assignments(cluster_assignments, db_path):
    """Insert cluster assignments into multi_cluster_assignments table"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Group assignments by dicho_id to handle ranking properly
    assignments_by_dicho = {}
    for assignment in cluster_assignments:
        dicho_id = assignment['dicho_id']
        if dicho_id not in assignments_by_dicho:
            assignments_by_dicho[dicho_id] = []
        assignments_by_dicho[dicho_id].append(assignment)
    
    # Get next available ID
    cursor.execute('SELECT MAX(id) FROM multi_cluster_assignments')
    max_id = cursor.fetchone()[0]
    next_id = (max_id + 1) if max_id else 1
    
    for dicho_id, assignments in assignments_by_dicho.items():
        # Sort by strength (highest first)
        assignments.sort(key=lambda x: x['assignment_strength'], reverse=True)
        
        for rank, assignment in enumerate(assignments, 1):
            # Check if assignment already exists
            cursor.execute('''
                SELECT id FROM multi_cluster_assignments 
                WHERE dicho_id = ? AND cluster_id = ?
            ''', (assignment['dicho_id'], assignment['cluster_id']))
            
            if cursor.fetchone():
                continue  # Skip if already exists
            
            cursor.execute('''
                INSERT INTO multi_cluster_assignments (
                    id, dicho_id, cluster_id, rank, similarity_score, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                next_id,
                assignment['dicho_id'],
                assignment['cluster_id'],
                rank,
                assignment['assignment_strength'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            next_id += 1
    
    conn.commit()
    conn.close()

def insert_dichos_from_file(input_file, db_path):
    """Main function to insert new dichos with all related data from a TSV file"""
    print("🚀 Inserting New Dichos with Cluster Assignments and English Equivalents")
    print("=" * 80)
    
    # Load new dichos
    try:
        df = pd.read_csv(input_file, sep='\t')
        print(f"📚 Loaded {len(df)} new dichos")
    except FileNotFoundError:
        print(f"❌ Error: {input_file} not found")
        return
    
    # Convert to list of dictionaries
    new_dichos = df.to_dict('records')
    
    # Get existing clusters
    print("🔍 Getting existing clusters...")
    clusters, assignments = get_existing_clusters(db_path)
    print(f"   Found {len(clusters)} existing clusters")
    
    # Assign dichos to clusters
    print("🎯 Assigning dichos to clusters...")
    cluster_assignments = assign_dichos_to_clusters(new_dichos, clusters, assignments)
    print(f"   Created {len(cluster_assignments)} cluster assignments")
    
    # Extract English equivalents
    english_equivalents = [dicho.get('translation', '') for dicho in new_dichos]
    english_equivalents = [eq for eq in english_equivalents if eq and eq != 'Translation needed for: ']
    
    print(f"📝 Found {len(english_equivalents)} English equivalents")
    
    # Insert English equivalents
    print("💾 Inserting English equivalents...")
    english_equivalent_ids = insert_english_equivalents(english_equivalents, db_path)
    print(f"   Inserted {len(english_equivalent_ids)} English equivalents")
    
    # Insert dichos with relationships
    print("💾 Inserting dichos and relationships...")
    dicho_ids = insert_dichos_with_relationships(new_dichos, english_equivalent_ids, db_path)
    print(f"   Inserted {len(dicho_ids)} dichos")
    
    # Insert cluster assignments
    print("💾 Inserting cluster assignments...")
    insert_cluster_assignments(cluster_assignments, db_path)
    print(f"   Inserted {len(cluster_assignments)} cluster assignments")
    
    # Verify insertion
    print("\n🔍 Verifying insertion...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check total dichos
    cursor.execute('SELECT COUNT(*) FROM dichos')
    total_dichos = cursor.fetchone()[0]
    print(f"   Total dichos in database: {total_dichos}")
    
    # Check new dichos
    cursor.execute('SELECT id, dicho FROM dichos WHERE id >= ? ORDER BY id DESC LIMIT 5', (dicho_ids[0],))
    new_entries = cursor.fetchall()
    print(f"   Last 5 new entries:")
    for entry in new_entries:
        print(f"     ID {entry[0]:3d}: {entry[1]}")
    
    # Check relationships
    cursor.execute('SELECT COUNT(*) FROM dicho_proverb_relationships')
    total_relationships = cursor.fetchone()[0]
    print(f"   Total relationships: {total_relationships}")
    
    # Check cluster assignments
    cursor.execute('SELECT COUNT(*) FROM multi_cluster_assignments')
    total_assignments = cursor.fetchone()[0]
    print(f"   Total cluster assignments: {total_assignments}")
    
    conn.close()
    
    print(f"\n🎉 INSERTION COMPLETE!")
    print(f"   ✅ Inserted {len(dicho_ids)} new dichos")
    print(f"   ✅ Created {len(english_equivalent_ids)} English equivalents")
    print(f"   ✅ Created {len(cluster_assignments)} cluster assignments")
    print(f"   ✅ Created {len(english_equivalent_ids)} dicho-proverb relationships")

def main():
    """Main function for command-line usage"""
    insert_dichos_from_file('enriched_new_dichos.tsv', 'core_data/dichos_normalized.db')

if __name__ == "__main__":
    main()
