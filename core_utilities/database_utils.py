#!/usr/bin/env python3
import sqlite3
import json
import pandas as pd

class DichosDatabase:
    """Utility class for working with the normalized dichos database."""
    
    def __init__(self, db_path='dichos_normalized.db'):
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection."""
        return sqlite3.connect(self.db_path)
    
    def search_dichos(self, query, language='both', limit=20):
        """
        Search dichos by Spanish text, English translation, or both.
        
        Args:
            query (str): Search term
            language (str): 'spanish', 'english', or 'both'
            limit (int): Maximum results to return
        """
        conn = self.get_connection()
        
        if language == 'spanish':
            sql = '''
                SELECT d.dicho, d.translation, d.difficulty_level, d.cultural_context
                FROM dichos d
                WHERE d.dicho LIKE ? OR d.expanded_context_usage LIKE ?
                ORDER BY d.difficulty_level
                LIMIT ?
            '''
            params = [f'%{query}%', f'%{query}%', limit]
        elif language == 'english':
            sql = '''
                SELECT d.dicho, d.translation, e.proverb, d.difficulty_level
                FROM dichos d
                JOIN dicho_proverb_relationships dpr ON d.id = dpr.dicho_id
                JOIN english_proverbs e ON e.id = dpr.proverb_id
                WHERE e.proverb LIKE ? OR d.translation LIKE ?
                ORDER BY d.difficulty_level
                LIMIT ?
            '''
            params = [f'%{query}%', f'%{query}%', limit]
        else:  # both
            sql = '''
                SELECT DISTINCT d.dicho, d.translation, d.difficulty_level, d.cultural_context
                FROM dichos d
                LEFT JOIN dicho_proverb_relationships dpr ON d.id = dpr.dicho_id
                LEFT JOIN english_proverbs e ON e.id = dpr.proverb_id
                WHERE d.dicho LIKE ? OR d.translation LIKE ? OR e.proverb LIKE ? OR d.expanded_context_usage LIKE ?
                ORDER BY d.difficulty_level
                LIMIT ?
            '''
            params = [f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%', limit]
        
        df = pd.read_sql_query(sql, conn, params=params)
        conn.close()
        return df
    
    def get_dichos_by_difficulty(self, level, limit=20):
        """Get dichos by difficulty level."""
        conn = self.get_connection()
        sql = '''
            SELECT d.dicho, d.translation, d.cultural_context, d.emotion_tone
            FROM dichos d
            WHERE d.difficulty_level = ?
            ORDER BY d.line_num
            LIMIT ?
        '''
        df = pd.read_sql_query(sql, conn, params=[level, limit])
        conn.close()
        return df
    
    def get_dichos_by_cultural_context(self, context, limit=20):
        """Get dichos by cultural context."""
        conn = self.get_connection()
        sql = '''
            SELECT d.dicho, d.translation, d.difficulty_level, d.emotion_tone
            FROM dichos d
            WHERE d.cultural_context = ?
            ORDER BY d.difficulty_level
            LIMIT ?
        '''
        df = pd.read_sql_query(sql, conn, params=[context, limit])
        conn.close()
        return df
    
    def get_english_proverbs_by_category(self, category, limit=20):
        """Get English proverbs by category."""
        conn = self.get_connection()
        sql = '''
            SELECT proverb, difficulty_level, origin, formality_level, usage_count
            FROM english_proverbs
            WHERE category = ?
            ORDER BY usage_count DESC
            LIMIT ?
        '''
        df = pd.read_sql_query(sql, conn, params=[category, limit])
        conn.close()
        return df
    
    def get_dicho_with_equivalents(self, dicho_id):
        """Get a specific dicho with all its English equivalents."""
        conn = self.get_connection()
        sql = '''
            SELECT 
                d.dicho, d.translation, d.expanded_context_usage, d.difficulty_level,
                d.cultural_context, d.emotion_tone, d.learning_notes,
                e.proverb, e.difficulty_level as english_difficulty, e.category
            FROM dichos d
            JOIN dicho_proverb_relationships dpr ON d.id = dpr.dicho_id
            JOIN english_proverbs e ON e.id = dpr.proverb_id
            WHERE d.id = ?
            ORDER BY e.usage_count DESC
        '''
        df = pd.read_sql_query(sql, conn, params=[dicho_id])
        conn.close()
        return df
    
    def get_most_connected_dichos(self, limit=10):
        """Get dichos with the most English equivalents."""
        conn = self.get_connection()
        sql = '''
            SELECT d.dicho, d.translation, COUNT(dpr.proverb_id) as equivalent_count
            FROM dichos d
            JOIN dicho_proverb_relationships dpr ON d.id = dpr.dicho_id
            GROUP BY d.id
            ORDER BY equivalent_count DESC
            LIMIT ?
        '''
        df = pd.read_sql_query(sql, conn, params=[limit])
        conn.close()
        return df
    
    def get_most_used_proverbs(self, limit=20):
        """Get most commonly used English proverbs."""
        conn = self.get_connection()
        sql = '''
            SELECT proverb, category, difficulty_level, usage_count
            FROM english_proverbs
            ORDER BY usage_count DESC
            LIMIT ?
        '''
        df = pd.read_sql_query(sql, conn, params=[limit])
        conn.close()
        return df
    
    def get_difficulty_distribution(self):
        """Get distribution of dichos by difficulty level."""
        conn = self.get_connection()
        sql = '''
            SELECT difficulty_level, COUNT(*) as count
            FROM dichos
            GROUP BY difficulty_level
            ORDER BY difficulty_level
        '''
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df
    
    def get_category_distribution(self):
        """Get distribution of English proverbs by category."""
        conn = self.get_connection()
        sql = '''
            SELECT category, COUNT(*) as count
            FROM english_proverbs
            GROUP BY category
            ORDER BY count DESC
        '''
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df
    
    def export_to_csv(self, table_name, output_file):
        """Export a table to CSV."""
        conn = self.get_connection()
        sql = f'SELECT * FROM {table_name}'
        df = pd.read_sql_query(sql, conn)
        df.to_csv(output_file, index=False)
        conn.close()
        print(f"✅ Exported {table_name} to {output_file}")

def main():
    """Demo the database utilities."""
    db = DichosDatabase()
    
    print("🔍 DICHOS DATABASE UTILITIES")
    print("=" * 50)
    
    # Search examples
    print("\n📝 Search for 'tiempo' (time-related):")
    results = db.search_dichos('tiempo', language='spanish', limit=5)
    print(results[['dicho', 'translation', 'difficulty_level']].to_string(index=False))
    
    print("\n📝 Search for 'money' in English:")
    results = db.search_dichos('money', language='english', limit=5)
    print(results[['dicho', 'translation', 'proverb']].to_string(index=False))
    
    # Difficulty distribution
    print("\n📊 Difficulty Level Distribution:")
    diff_dist = db.get_difficulty_distribution()
    print(diff_dist.to_string(index=False))
    
    # Most connected dichos
    print("\n🔗 Top 5 Most Connected Dichos:")
    connected = db.get_most_connected_dichos(5)
    print(connected.to_string(index=False))
    
    # Category distribution
    print("\n🏷️  English Proverbs by Category:")
    cat_dist = db.get_category_distribution()
    print(cat_dist.to_string(index=False))

if __name__ == "__main__":
    main()
