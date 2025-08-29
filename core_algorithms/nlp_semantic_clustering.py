#!/usr/bin/env python3
"""
NLP-based Semantic Clustering of Dichos using Sentence Transformers, UMAP, and Clustering.
This script demonstrates modern NLP techniques for semantic understanding and clustering.
"""

import sqlite3
import json
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import umap
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

def explain_nlp_theory():
    """Explain the theory behind each NLP technique we're using."""
    
    print("🧠 NLP CLUSTERING THEORY EXPLANATION")
    print("=" * 60)
    
    print("\n1️⃣ SENTENCE TRANSFORMERS & EMBEDDINGS:")
    print("   • Traditional NLP used word-level analysis (bag-of-words, TF-IDF)")
    print("   • Sentence Transformers use 'transformer' neural networks trained on millions of text examples")
    print("   • They convert text into high-dimensional vectors (embeddings) that capture semantic meaning")
    print("   • Similar meanings → Similar vectors → Similar positions in high-dimensional space")
    print("   • Example: 'happy' and 'joyful' will have similar embeddings, even though they're different words")
    
    print("\n2️⃣ EMBEDDING SPACE:")
    print("   • Each keyword becomes a point in high-dimensional space (typically 384-768 dimensions)")
    print("   • Semantic relationships are preserved: similar concepts cluster together")
    print("   • Distance between points = semantic similarity")
    print("   • This is why 'useless' and 'lazy' will be close to each other in embedding space")
    
    print("\n3️⃣ UMAP (Uniform Manifold Approximation and Projection):")
    print("   • High-dimensional space is hard to visualize and cluster")
    print("   • UMAP reduces dimensions while preserving semantic relationships")
    print("   • It's like taking a 3D object and making a 2D map that preserves distances")
    print("   • Much faster and more accurate than older methods like PCA or t-SNE")
    print("   • Preserves both local structure (nearby points stay nearby) and global structure")
    
    print("\n4️⃣ CLUSTERING IN REDUCED SPACE:")
    print("   • Now we work in 2D or 3D space where clustering is much easier")
    print("   • K-means: Finds spherical clusters by minimizing distance to cluster centers")
    print("   • DBSCAN: Finds clusters of any shape by connecting nearby points")
    print("   • We can visualize the clusters and adjust parameters easily")
    
    print("\n5️⃣ WHY THIS APPROACH IS BETTER:")
    print("   • Semantic understanding vs. word matching")
    print("   • No more ties (continuous similarity scores)")
    print("   • Discovers natural groupings we might miss")
    print("   • Handles synonyms and related concepts automatically")
    
    print("\n" + "=" * 60)

def load_and_prepare_data():
    """Load dichos data and prepare for NLP processing."""
    
    print("\n📊 LOADING AND PREPARING DATA")
    print("=" * 40)
    
    conn = sqlite3.connect('dichos_normalized.db')
    cursor = conn.cursor()
    
    # Get all dichos with their semantic keywords
    cursor.execute('''
        SELECT id, dicho, translation, semantic_keywords 
        FROM dichos 
        WHERE semantic_keywords IS NOT NULL
        ORDER BY id
    ''')
    
    dichos = cursor.fetchall()
    conn.close()
    
    print(f"✅ Loaded {len(dichos)} dichos")
    
    # Parse semantic keywords and create text representations
    processed_data = []
    all_keywords = set()
    
    for dicho_id, dicho_text, translation, semantic_keywords_str in dichos:
        try:
            keywords = json.loads(semantic_keywords_str)
            if isinstance(keywords, list):
                # Create a semantic text representation by joining keywords
                # This gives the sentence transformer context about the meaning
                semantic_text = " ".join(keywords)
                
                processed_data.append({
                    'id': dicho_id,
                    'dicho': dicho_text,
                    'translation': translation,
                    'keywords': keywords,
                    'semantic_text': semantic_text,
                    'keyword_count': len(keywords)
                })
                
                all_keywords.update(keywords)
        except Exception as e:
            print(f"❌ Error processing dicho {dicho_id}: {e}")
    
    print(f"✅ Processed {len(processed_data)} dichos successfully")
    print(f"✅ Total unique keywords: {len(all_keywords)}")
    print(f"✅ Average keywords per dicho: {np.mean([d['keyword_count'] for d in processed_data]):.2f}")
    
    return processed_data, list(all_keywords)

def generate_embeddings(processed_data, all_keywords):
    """Generate embeddings using Sentence Transformers."""
    
    print("\n🤖 GENERATING SEMANTIC EMBEDDINGS")
    print("=" * 40)
    
    print("📚 Loading Sentence Transformer model...")
    print("   • Using 'all-MiniLM-L6-v2' model (fast, accurate, CPU-friendly)")
    print("   • Model size: ~90MB, generates 384-dimensional embeddings")
    print("   • Trained on millions of text examples for semantic understanding")
    
    # Load the model (this downloads it the first time)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("✅ Model loaded successfully!")
    
    # Generate embeddings for each dicho's semantic text
    print("\n🔄 Generating embeddings for dichos...")
    semantic_texts = [d['semantic_text'] for d in processed_data]
    dicho_embeddings = model.encode(semantic_texts, show_progress_bar=True)
    
    print(f"✅ Generated {len(dicho_embeddings)} embeddings")
    print(f"✅ Embedding dimensions: {dicho_embeddings.shape[1]}")
    
    # Generate embeddings for individual keywords (for cluster analysis)
    print("\n🔄 Generating embeddings for individual keywords...")
    keyword_embeddings = model.encode(all_keywords, show_progress_bar=True)
    
    print(f"✅ Generated {len(keyword_embeddings)} keyword embeddings")
    
    return model, dicho_embeddings, keyword_embeddings

def apply_umap_dimensionality_reduction(dicho_embeddings, keyword_embeddings):
    """Apply UMAP to reduce dimensions for visualization and clustering."""
    
    print("\n🗺️ APPLYING UMAP DIMENSIONALITY REDUCTION")
    print("=" * 50)
    
    print("📐 UMAP Theory:")
    print("   • Input: {dicho_embeddings.shape[1]}-dimensional embeddings")
    print("   • Output: 2D or 3D coordinates for visualization and clustering")
    print("   • Preserves semantic relationships: similar meanings stay close together")
    print("   • Much faster than t-SNE, better at preserving global structure")
    
    # UMAP parameters
    n_neighbors = 15        # How many neighbors to consider for local structure
    min_dist = 0.1          # Minimum distance between points in output space
    n_components = 2        # Reduce to 2D for easy visualization
    
    print(f"\n🔧 UMAP Parameters:")
    print(f"   • n_neighbors: {n_neighbors} (local structure preservation)")
    print(f"   • min_dist: {min_dist} (minimum separation in output)")
    print(f"   • n_components: {n_components} (2D output)")
    
    # Apply UMAP to dichos
    print("\n🔄 Reducing dicho embeddings to 2D...")
    umap_dichos = umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        n_components=n_components,
        random_state=42
    ).fit_transform(dicho_embeddings)
    
    # Apply UMAP to keywords
    print("🔄 Reducing keyword embeddings to 2D...")
    umap_keywords = umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        n_components=n_components,
        random_state=42
    ).fit_transform(keyword_embeddings)
    
    print("✅ UMAP reduction complete!")
    print(f"✅ Dicho coordinates: {umap_dichos.shape}")
    print(f"✅ Keyword coordinates: {umap_keywords.shape}")
    
    return umap_dichos, umap_keywords

def find_optimal_clusters(umap_coordinates, max_clusters=20):
    """Find optimal number of clusters using silhouette analysis."""
    
    print("\n🔍 FINDING OPTIMAL NUMBER OF CLUSTERS")
    print("=" * 45)
    
    print("📊 Silhouette Analysis Theory:")
    print("   • Measures how well each point fits in its assigned cluster")
    print("   • Range: -1 (poor fit) to +1 (excellent fit)")
    print("   • Higher scores = better clustering")
    print("   • We'll test different cluster counts to find the best")
    
    silhouette_scores = []
    cluster_counts = range(2, max_clusters + 1)
    
    print(f"\n🔄 Testing cluster counts from 2 to {max_clusters}...")
    
    for n_clusters in cluster_counts:
        try:
            # Apply K-means
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(umap_coordinates)
            
            # Calculate silhouette score
            if len(set(cluster_labels)) > 1:  # Need at least 2 clusters
                score = silhouette_score(umap_coordinates, cluster_labels)
                silhouette_scores.append(score)
                print(f"   • {n_clusters} clusters: silhouette score = {score:.3f}")
            else:
                silhouette_scores.append(0)
                print(f"   • {n_clusters} clusters: failed (single cluster)")
        except Exception as e:
            silhouette_scores.append(0)
            print(f"   • {n_clusters} clusters: error - {e}")
    
    # Find best number of clusters
    best_score = max(silhouette_scores)
    best_n_clusters = cluster_counts[silhouette_scores.index(best_score)]
    
    print(f"\n🏆 BEST CLUSTERING:")
    print(f"   • Optimal clusters: {best_n_clusters}")
    print(f"   • Silhouette score: {best_score:.3f}")
    
    return best_n_clusters, silhouette_scores, cluster_counts

def perform_final_clustering(umap_coordinates, n_clusters):
    """Perform final clustering with optimal number of clusters."""
    
    print(f"\n🎯 PERFORMING FINAL CLUSTERING ({n_clusters} clusters)")
    print("=" * 50)
    
    print("🔧 K-means Clustering:")
    print("   • Algorithm: K-means with {n_clusters} clusters")
    print("   • Method: Minimizes distance to cluster centers")
    print("   • Output: Each point assigned to exactly one cluster")
    print("   • Advantage: Fast, scalable, well-defined clusters")
    
    # Apply K-means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(umap_coordinates)
    
    # Calculate cluster statistics
    unique_labels, counts = np.unique(cluster_labels, return_counts=True)
    
    print(f"\n📊 CLUSTER STATISTICS:")
    print(f"   • Total points: {len(cluster_labels)}")
    print(f"   • Clusters found: {len(unique_labels)}")
    
    for i, (label, count) in enumerate(zip(unique_labels, counts)):
        percentage = (count / len(cluster_labels)) * 100
        print(f"   • Cluster {label}: {count} points ({percentage:.1f}%)")
    
    return cluster_labels, kmeans

def create_clusters_table(cluster_labels, processed_data, all_keywords, keyword_embeddings, model):
    """Create clusters table with semantic analysis."""
    
    print("\n🗄️ CREATING CLUSTERS TABLE")
    print("=" * 35)
    
    print("📋 Creating semantic clusters based on keyword embeddings...")
    
    # Group keywords by cluster
    cluster_keywords = {}
    for i, label in enumerate(cluster_labels):
        if label not in cluster_keywords:
            cluster_keywords[label] = []
        cluster_keywords[label].extend(processed_data[i]['keywords'])
    
    # Remove duplicates and get unique keywords per cluster
    for label in cluster_keywords:
        cluster_keywords[label] = list(set(cluster_keywords[label]))
    
    # Create database table
    conn = sqlite3.connect('dichos_normalized.db')
    cursor = conn.cursor()
    
    # Drop existing clusters table if it exists
    cursor.execute("DROP TABLE IF EXISTS clusters")
    
    # Create new clusters table
    cursor.execute('''
        CREATE TABLE clusters (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            keywords TEXT NOT NULL,
            keyword_count INTEGER NOT NULL,
            cluster_size INTEGER NOT NULL
        )
    ''')
    
    # Insert clusters
    for label in sorted(cluster_keywords.keys()):
        keywords = cluster_keywords[label]
        keyword_count = len(keywords)
        cluster_size = sum(1 for l in cluster_labels if l == label)
        
        # Generate cluster name based on most common keywords
        name = f"Cluster_{label}"
        
        # Generate description based on keywords
        description = f"Semantic cluster with {keyword_count} unique keywords and {cluster_size} dichos"
        
        cursor.execute('''
            INSERT INTO clusters (id, name, description, keywords, keyword_count, cluster_size)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (int(label), name, description, json.dumps(keywords), int(keyword_count), int(cluster_size)))
    
    conn.commit()
    
    # Show cluster summary
    print(f"\n📊 CLUSTERS CREATED:")
    for label in sorted(cluster_keywords.keys()):
        keywords = cluster_keywords[label]
        cluster_size = sum(1 for l in cluster_labels if l == label)
        print(f"   • Cluster {label}: {len(keywords)} keywords, {cluster_size} dichos")
        print(f"     Sample keywords: {keywords[:5]}")
    
    conn.close()
    
    return cluster_keywords

def assign_dichos_to_clusters(processed_data, cluster_labels, cluster_keywords_dict):
    """Assign each dicho to its cluster and create dicho_clusters table."""
    
    print("\n🎯 ASSIGNING DICHOS TO CLUSTERS")
    print("=" * 40)
    
    print("📝 Creating dicho_clusters table...")
    
    conn = sqlite3.connect('dichos_normalized.db')
    cursor = conn.cursor()
    
    # Drop existing dicho_clusters table if it exists
    cursor.execute("DROP TABLE IF EXISTS dicho_clusters")
    
    # Create new dicho_clusters table
    cursor.execute('''
        CREATE TABLE dicho_clusters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dicho_id INTEGER NOT NULL,
            cluster_id INTEGER NOT NULL,
            confidence_score REAL NOT NULL,
            matched_keywords TEXT,
            ranking_position INTEGER DEFAULT 1,
            FOREIGN KEY (dicho_id) REFERENCES dichos (id),
            FOREIGN KEY (cluster_id) REFERENCES clusters (id)
        )
    ''')
    
    # Insert assignments
    assignments = []
    for i, (dicho, label) in enumerate(zip(processed_data, cluster_labels)):
        dicho_id = dicho['id']
        cluster_id = label
        
        # Calculate confidence score based on keyword overlap
        dicho_keywords = set(dicho['keywords'])
        cluster_keywords_set = set(cluster_keywords_dict[label])
        overlap = len(dicho_keywords & cluster_keywords_set)
        confidence = overlap / len(dicho_keywords) if dicho_keywords else 0
        
        # Get matched keywords
        matched = list(dicho_keywords & cluster_keywords_set)
        
        cursor.execute('''
            INSERT INTO dicho_clusters (dicho_id, cluster_id, confidence_score, matched_keywords, ranking_position)
            VALUES (?, ?, ?, ?, ?)
        ''', (dicho_id, cluster_id, confidence, json.dumps(matched), 1))
        
        assignments.append({
            'dicho_id': dicho_id,
            'cluster_id': cluster_id,
            'confidence': confidence,
            'matches': matched
        })
    
    conn.commit()
    
    # Show assignment summary
    print(f"\n📊 ASSIGNMENT SUMMARY:")
    print(f"   • Total assignments: {len(assignments)}")
    print(f"   • Average confidence: {np.mean([a['confidence'] for a in assignments]):.3f}")
    print(f"   • Confidence range: {min([a['confidence'] for a in assignments]):.3f} to {max([a['confidence'] for a in assignments]):.3f}")
    
    # Show confidence distribution
    confidence_scores = [a['confidence'] for a in assignments]
    print(f"   • High confidence (>0.8): {sum(1 for c in confidence_scores if c > 0.8)}")
    print(f"   • Medium confidence (0.5-0.8): {sum(1 for c in confidence_scores if 0.5 <= c <= 0.8)}")
    print(f"   • Low confidence (<0.5): {sum(1 for c in confidence_scores if c < 0.5)}")
    
    conn.close()
    
    return assignments

def create_visualizations(umap_coordinates, cluster_labels, processed_data):
    """Create interactive visualizations of the clustering results."""
    
    print("\n📊 CREATING INTERACTIVE VISUALIZATIONS")
    print("=" * 45)
    
    print("🎨 Creating UMAP visualization with clusters...")
    
    # Create DataFrame for plotting
    df = pd.DataFrame({
        'UMAP_1': umap_coordinates[:, 0],
        'UMAP_2': umap_coordinates[:, 1],
        'Cluster': [f'Cluster_{label}' for label in cluster_labels],
        'Dicho': [d['dicho'][:50] + '...' for d in processed_data],
        'Keywords': [', '.join(d['keywords'][:3]) + '...' for d in processed_data],
        'Keyword_Count': [d['keyword_count'] for d in processed_data]
    })
    
    # Create scatter plot
    fig = px.scatter(
        df, 
        x='UMAP_1', 
        y='UMAP_2', 
        color='Cluster',
        hover_data=['Dicho', 'Keywords', 'Keyword_Count'],
        title='Dichos Clustering Visualization (UMAP + K-means)',
        labels={'UMAP_1': 'UMAP Dimension 1', 'UMAP_2': 'UMAP Dimension 2'}
    )
    
    fig.update_layout(
        width=1000,
        height=700,
        title_x=0.5
    )
    
    # Save the plot
    fig.write_html('nlp_clustering_visualization.html')
    print("✅ Saved visualization to 'nlp_clustering_visualization.html'")
    
    # Create cluster size distribution
    cluster_sizes = df['Cluster'].value_counts()
    fig2 = px.bar(
        x=cluster_sizes.index,
        y=cluster_sizes.values,
        title='Cluster Size Distribution',
        labels={'x': 'Cluster', 'y': 'Number of Dichos'}
    )
    
    fig2.update_layout(
        width=800,
        height=500,
        title_x=0.5
    )
    
    fig2.write_html('cluster_size_distribution.html')
    print("✅ Saved cluster distribution to 'cluster_size_distribution.html'")
    
    return fig, fig2

def main():
    """Main execution function."""
    
    print("🚀 NLP SEMANTIC CLUSTERING OF DICHOS")
    print("=" * 50)
    
    # Explain the theory
    explain_nlp_theory()
    
    # Load and prepare data
    processed_data, all_keywords = load_and_prepare_data()
    
    # Generate embeddings
    model, dicho_embeddings, keyword_embeddings = generate_embeddings(processed_data, all_keywords)
    
    # Apply UMAP
    umap_dichos, umap_keywords = apply_umap_dimensionality_reduction(dicho_embeddings, keyword_embeddings)
    
    # Find optimal clusters
    best_n_clusters, silhouette_scores, cluster_counts = find_optimal_clusters(umap_dichos)
    
    # Perform final clustering
    cluster_labels, kmeans = perform_final_clustering(umap_dichos, best_n_clusters)
    
    # Create clusters table
    cluster_keywords = create_clusters_table(cluster_labels, processed_data, all_keywords, keyword_embeddings, model)
    
    # Assign dichos to clusters
    assignments = assign_dichos_to_clusters(processed_data, cluster_labels, cluster_keywords)
    
    # Create visualizations
    fig, fig2 = create_visualizations(umap_dichos, cluster_labels, processed_data)
    
    print("\n🎉 NLP CLUSTERING COMPLETE!")
    print("=" * 30)
    print("📁 Files created:")
    print("   • nlp_clustering_visualization.html")
    print("   • cluster_size_distribution.html")
    print("   • Updated database tables: clusters, dicho_clusters")
    
    print("\n🔍 Next steps:")
    print("   • Open the HTML files to explore the clustering results")
    print("   • Analyze cluster assignments in the database")
    print("   • Refine clusters if needed based on semantic coherence")

if __name__ == "__main__":
    main()
