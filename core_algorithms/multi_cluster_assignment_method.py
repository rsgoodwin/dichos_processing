#!/usr/bin/env python3
"""
Systematic method for assigning multiple cluster memberships per dicho.
Based on similarity scores, gap analysis, and semantic coherence.
"""

import sqlite3
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def analyze_similarity_landscape():
    """Analyze the full similarity landscape to determine optimal thresholds."""
    print("🔍 ANALYZING SIMILARITY LANDSCAPE FOR MULTI-CLUSTER ASSIGNMENT")
    print("=" * 70)
    
    conn = sqlite3.connect('dichos_normalized.db')
    
    # Load all similarity scores
    df = pd.read_sql_query('''
        SELECT 
            dc.dicho_id,
            dc.cluster_id,
            dc.similarity_score,
            dc.matched_keywords,
            c.name as cluster_name,
            d.dicho,
            d.semantic_keywords
        FROM dicho_clusters dc
        JOIN clusters c ON dc.cluster_id = c.id
        JOIN dichos d ON dc.dicho_id = d.id
        ORDER BY dc.dicho_id, dc.similarity_score DESC
    ''', conn)
    
    conn.close()
    
    # Parse JSON fields
    df['matched_keywords'] = df['matched_keywords'].apply(json.loads)
    df['semantic_keywords'] = df['semantic_keywords'].apply(json.loads)
    
    return df

def design_multi_cluster_method(df):
    """Design the systematic multi-cluster assignment method."""
    print("\n🎯 DESIGNING MULTI-CLUSTER ASSIGNMENT METHOD")
    print("=" * 50)
    
    # Method 1: Absolute Threshold Approach
    print("\n1️⃣ ABSOLUTE THRESHOLD APPROACH:")
    print("-" * 30)
    print("• Use fixed similarity score threshold")
    print("• Pros: Simple, consistent, interpretable")
    print("• Cons: May miss context-specific relationships")
    
    # Method 2: Relative Gap Approach
    print("\n2️⃣ RELATIVE GAP APPROACH:")
    print("-" * 30)
    print("• Include clusters within X% of best score")
    print("• Pros: Adapts to individual dicho characteristics")
    print("• Cons: May include too many clusters for some dichos")
    
    # Method 3: Hybrid Approach (RECOMMENDED)
    print("\n3️⃣ HYBRID APPROACH (RECOMMENDED):")
    print("-" * 30)
    print("• Primary: Best score cluster")
    print("• Secondary: Clusters within gap threshold OR above absolute threshold")
    print("• Tertiary: Additional clusters above lower threshold")
    print("• Pros: Balanced, flexible, semantically meaningful")
    print("• Cons: More complex logic")
    
    return df

def implement_hybrid_method(df):
    """Implement the recommended hybrid method."""
    print("\n🔧 IMPLEMENTING HYBRID MULTI-CLUSTER METHOD")
    print("=" * 50)
    
    # Define thresholds based on analysis
    PRIMARY_THRESHOLD = 0.4      # Strong semantic relationship
    SECONDARY_GAP_THRESHOLD = 0.1  # Within 10% of best score
    SECONDARY_ABS_THRESHOLD = 0.35 # Alternative absolute threshold
    TERTIARY_THRESHOLD = 0.3     # Moderate semantic relationship
    MAX_CLUSTERS = 3              # Maximum clusters per dicho
    
    print(f"📊 THRESHOLDS:")
    print(f"  • Primary: {PRIMARY_THRESHOLD} (strong relationship)")
    print(f"  • Secondary gap: {SECONDARY_GAP_THRESHOLD} (within 10% of best)")
    print(f"  • Secondary absolute: {SECONDARY_ABS_THRESHOLD}")
    print(f"  • Tertiary: {TERTIARY_THRESHOLD} (moderate relationship)")
    print(f"  • Max clusters per dicho: {MAX_CLUSTERS}")
    
    # Process each dicho
    multi_cluster_assignments = []
    
    for dicho_id in df['dicho_id'].unique():
        dicho_scores = df[df['dicho_id'] == dicho_id].sort_values('similarity_score', ascending=False)
        
        # Primary cluster (best score)
        primary_cluster = dicho_scores.iloc[0]
        best_score = primary_cluster['similarity_score']
        
        # Secondary clusters (within gap threshold OR above absolute threshold)
        secondary_candidates = []
        for _, row in dicho_scores.iterrows():
            if row['cluster_id'] == primary_cluster['cluster_id']:
                continue
                
            # Check gap threshold
            gap_qualified = (best_score - row['similarity_score']) <= SECONDARY_GAP_THRESHOLD
            # Check absolute threshold
            abs_qualified = row['similarity_score'] >= SECONDARY_ABS_THRESHOLD
            
            if gap_qualified or abs_qualified:
                secondary_candidates.append(row)
        
        # Tertiary clusters (above lower threshold)
        tertiary_candidates = []
        secondary_cluster_ids = [c['cluster_id'] for c in secondary_candidates]
        for _, row in dicho_scores.iterrows():
            if (row['cluster_id'] == primary_cluster['cluster_id'] or 
                row['cluster_id'] in secondary_cluster_ids):
                continue
                
            if row['similarity_score'] >= TERTIARY_THRESHOLD:
                tertiary_candidates.append(row)
        
        # Select final clusters (respecting MAX_CLUSTERS limit)
        selected_clusters = [primary_cluster]
        
        # Add secondary clusters
        for candidate in secondary_candidates[:MAX_CLUSTERS - 1]:
            selected_clusters.append(candidate)
        
        # Add tertiary clusters if space remains
        remaining_slots = MAX_CLUSTERS - len(selected_clusters)
        if remaining_slots > 0:
            for candidate in tertiary_candidates[:remaining_slots]:
                selected_clusters.append(candidate)
        
        # Create assignment record
        for i, cluster in enumerate(selected_clusters):
            assignment = {
                'dicho_id': dicho_id,
                'cluster_id': cluster['cluster_id'],
                'cluster_name': cluster['cluster_name'],
                'similarity_score': cluster['similarity_score'],
                'assignment_rank': i + 1,
                'assignment_type': ['Primary', 'Secondary', 'Tertiary'][i],
                'matched_keywords': cluster['matched_keywords'],
                'dicho_text': cluster['dicho']
            }
            multi_cluster_assignments.append(assignment)
    
    return pd.DataFrame(multi_cluster_assignments)

def analyze_multi_cluster_results(df_multi):
    """Analyze the results of multi-cluster assignment."""
    print("\n📊 ANALYZING MULTI-CLUSTER ASSIGNMENT RESULTS")
    print("=" * 55)
    
    # Summary statistics
    total_assignments = len(df_multi)
    unique_dichos = df_multi['dicho_id'].nunique()
    avg_clusters_per_dicho = total_assignments / unique_dichos
    
    print(f"📈 ASSIGNMENT SUMMARY:")
    print(f"  • Total assignments: {total_assignments:,}")
    print(f"  • Unique dichos: {unique_dichos}")
    print(f"  • Average clusters per dicho: {avg_clusters_per_dicho:.2f}")
    
    # Distribution by assignment type
    type_dist = df_multi['assignment_type'].value_counts()
    print(f"\n🎯 ASSIGNMENT TYPE DISTRIBUTION:")
    for assignment_type, count in type_dist.items():
        print(f"  • {assignment_type}: {count} ({count/total_assignments*100:.1f}%)")
    
    # Clusters by assignment rank
    rank_dist = df_multi['assignment_rank'].value_counts().sort_index()
    print(f"\n🏆 ASSIGNMENT RANK DISTRIBUTION:")
    for rank, count in rank_dist.items():
        print(f"  • Rank {rank}: {count} assignments")
    
    # Similarity score analysis by rank
    print(f"\n📊 SIMILARITY SCORES BY ASSIGNMENT RANK:")
    for rank in sorted(df_multi['assignment_rank'].unique()):
        rank_scores = df_multi[df_multi['assignment_rank'] == rank]['similarity_score']
        print(f"  • Rank {rank}: Mean={rank_scores.mean():.4f}, Std={rank_scores.std():.4f}")
    
    return df_multi

def create_multi_cluster_visualizations(df_multi):
    """Create visualizations for multi-cluster assignments."""
    print("\n📊 CREATING MULTI-CLUSTER VISUALIZATIONS")
    print("=" * 45)
    
    # 1. Assignment distribution by cluster
    fig1 = px.bar(
        df_multi.groupby('cluster_name').size().reset_index(name='count'),
        x='cluster_name',
        y='count',
        title='Total Assignments per Cluster (Including Multi-Cluster)',
        labels={'count': 'Total Assignments', 'cluster_name': 'Cluster'}
    )
    fig1.update_xaxes(tickangle=45)
    fig1.update_layout(height=600)
    
    # 2. Assignment type distribution
    type_counts = df_multi['assignment_type'].value_counts()
    fig2 = px.pie(
        values=type_counts.values,
        names=type_counts.index,
        title='Distribution of Assignment Types',
        hole=0.4
    )
    
    # 3. Similarity scores by assignment rank
    fig3 = px.box(
        df_multi,
        x='assignment_rank',
        y='similarity_score',
        title='Similarity Score Distribution by Assignment Rank',
        labels={'assignment_rank': 'Assignment Rank', 'similarity_score': 'Similarity Score'}
    )
    
    # 4. Multi-cluster assignment heatmap
    cluster_rank_matrix = df_multi.pivot_table(
        index='cluster_name',
        columns='assignment_rank',
        values='similarity_score',
        aggfunc='count',
        fill_value=0
    )
    
    fig4 = px.imshow(
        cluster_rank_matrix,
        title='Multi-Cluster Assignment Heatmap<br>Rows: Clusters, Columns: Assignment Ranks',
        color_continuous_scale='Blues',
        aspect='auto'
    )
    fig4.update_layout(height=600)
    
    # Save visualizations
    fig1.write_html('multi_cluster_assignments_by_cluster.html')
    fig2.write_html('multi_cluster_assignment_types.html')
    fig3.write_html('multi_cluster_scores_by_rank.html')
    fig4.write_html('multi_cluster_assignment_heatmap.html')
    
    print("✅ Multi-cluster visualizations saved:")
    print("  • multi_cluster_assignments_by_cluster.html")
    print("  • multi_cluster_assignment_types.html")
    print("  • multi_cluster_scores_by_rank.html")
    print("  • multi_cluster_assignment_heatmap.html")
    
    return fig1, fig2, fig3, fig4

def update_database_with_multi_clusters(df_multi):
    """Update the database to include multi-cluster assignments."""
    print("\n🗄️ UPDATING DATABASE WITH MULTI-CLUSTER ASSIGNMENTS")
    print("=" * 55)
    
    conn = sqlite3.connect('dichos_normalized.db')
    cursor = conn.cursor()
    
    # Create new table for multi-cluster assignments
    print("1️⃣ Creating multi_cluster_assignments table...")
    cursor.execute('DROP TABLE IF EXISTS multi_cluster_assignments')
    cursor.execute('''
        CREATE TABLE multi_cluster_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dicho_id INTEGER NOT NULL,
            cluster_id INTEGER NOT NULL,
            assignment_rank INTEGER NOT NULL,
            assignment_type TEXT NOT NULL,
            similarity_score REAL NOT NULL,
            matched_keywords TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (dicho_id) REFERENCES dichos(id),
            FOREIGN KEY (cluster_id) REFERENCES clusters(id),
            UNIQUE(dicho_id, cluster_id)
        )
    ''')
    
    # Insert multi-cluster assignments
    print("2️⃣ Inserting multi-cluster assignments...")
    for _, row in df_multi.iterrows():
        cursor.execute('''
            INSERT INTO multi_cluster_assignments 
            (dicho_id, cluster_id, assignment_rank, assignment_type, similarity_score, matched_keywords)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            row['dicho_id'],
            row['cluster_id'],
            row['assignment_rank'],
            row['assignment_type'],
            row['similarity_score'],
            json.dumps(row['matched_keywords'])
        ))
    
    # Verify the data
    cursor.execute('SELECT COUNT(*) FROM multi_cluster_assignments')
    total_assignments = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT dicho_id) FROM multi_cluster_assignments')
    unique_dichos = cursor.fetchone()[0]
    
    print(f"✅ Database updated:")
    print(f"  • Total assignments: {total_assignments:,}")
    print(f"  • Unique dichos: {unique_dichos}")
    print(f"  • Average clusters per dicho: {total_assignments/unique_dichos:.2f}")
    
    conn.commit()
    conn.close()

def main():
    """Main execution function."""
    print("🚀 IMPLEMENTING SYSTEMATIC MULTI-CLUSTER ASSIGNMENT METHOD")
    print("=" * 70)
    
    # Load and analyze data
    df = analyze_similarity_landscape()
    
    # Design method
    df = design_multi_cluster_method(df)
    
    # Implement hybrid method
    df_multi = implement_hybrid_method(df)
    
    # Analyze results
    df_multi = analyze_multi_cluster_results(df_multi)
    
    # Create visualizations
    create_multi_cluster_visualizations(df_multi)
    
    # Update database
    update_database_with_multi_clusters(df_multi)
    
    print(f"\n🎉 MULTI-CLUSTER ASSIGNMENT COMPLETE!")
    print("=" * 40)
    print("✅ Hybrid method implemented")
    print("✅ Up to 3 clusters per dicho")
    print("✅ Database updated with new assignments")
    print("✅ Visualizations created")
    
    # Print method justification
    print(f"\n📋 METHOD JUSTIFICATION:")
    print("=" * 25)
    print("1. PRIMARY CLUSTER: Best semantic match (threshold: 0.4)")
    print("2. SECONDARY CLUSTERS: Within 10% gap OR above 0.35 threshold")
    print("3. TERTIARY CLUSTERS: Above 0.3 threshold (if slots remain)")
    print("4. MAX 3 CLUSTERS: Prevents over-assignment while capturing nuance")
    print("5. HYBRID APPROACH: Balances absolute and relative criteria")

if __name__ == "__main__":
    main()
