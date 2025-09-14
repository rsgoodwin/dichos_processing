-- OPTIMIZED MULTI-CLUSTER ASSIGNMENT QUERIES
-- Simplified to use rank 1,2,3 instead of assignment_type

-- 1. FIND ALL CLUSTERS FOR A SPECIFIC DICHO
SELECT 
    d.dicho,
    d.translation,
    c.name as cluster_name,
    mca.rank,
    mca.similarity_score
FROM dichos d
JOIN multi_cluster_assignments mca ON d.id = mca.dicho_id
JOIN clusters c ON mca.cluster_id = c.id
WHERE d.id = 1  -- Change this to any dicho ID
ORDER BY mca.rank;

-- 2. FIND ALL DICHOS IN A SPECIFIC CLUSTER WITH THEIR RANKS
SELECT 
    d.dicho,
    d.translation,
    mca.rank,
    mca.similarity_score
FROM clusters c
JOIN multi_cluster_assignments mca ON c.id = mca.cluster_id
JOIN dichos d ON mca.dicho_id = d.id
WHERE c.id = 12  -- Change this to any cluster ID
ORDER BY mca.rank, mca.similarity_score DESC;

-- 3. FIND DICHOS WITH MULTIPLE CLUSTER ASSIGNMENTS
SELECT 
    d.dicho,
    d.translation,
    COUNT(mca.cluster_id) as cluster_count,
    GROUP_CONCAT(c.name || ' (Rank ' || mca.rank || ')') as cluster_assignments
FROM dichos d
JOIN multi_cluster_assignments mca ON d.id = mca.dicho_id
JOIN clusters c ON mca.cluster_id = c.id
GROUP BY d.id, d.dicho, d.translation
HAVING COUNT(mca.cluster_id) > 1
ORDER BY cluster_count DESC, d.dicho
LIMIT 10;

-- 4. CLUSTER OVERLAP ANALYSIS
SELECT 
    c1.name as cluster1,
    c2.name as cluster2,
    COUNT(DISTINCT mca1.dicho_id) as shared_dichos,
    AVG(mca1.similarity_score) as avg_score_cluster1,
    AVG(mca2.similarity_score) as avg_score_cluster2
FROM multi_cluster_assignments mca1
JOIN multi_cluster_assignments mca2 ON mca1.dicho_id = mca2.dicho_id
JOIN clusters c1 ON mca1.cluster_id = c1.id
JOIN clusters c2 ON mca2.cluster_id = c2.id
WHERE mca1.cluster_id < mca2.cluster_id
GROUP BY c1.id, c1.name, c2.id, c2.name
HAVING shared_dichos > 0
ORDER BY shared_dichos DESC, avg_score_cluster1 DESC
LIMIT 15;

-- 5. RANK QUALITY ANALYSIS
SELECT 
    mca.rank,
    COUNT(*) as assignment_count,
    ROUND(AVG(mca.similarity_score), 4) as avg_similarity,
    ROUND(MIN(mca.similarity_score), 4) as min_similarity,
    ROUND(MAX(mca.similarity_score), 4) as max_similarity,
    ROUND(STDDEV(mca.similarity_score), 4) as std_dev_similarity
FROM multi_cluster_assignments mca
GROUP BY mca.rank
ORDER BY mca.rank;

-- 6. FIND DICHOS BY RANK
SELECT 
    d.dicho,
    d.translation,
    c.name as cluster_name,
    mca.similarity_score
FROM multi_cluster_assignments mca
JOIN dichos d ON mca.dicho_id = d.id
JOIN clusters c ON mca.cluster_id = c.id
WHERE mca.rank = 1  -- Change to 2 or 3
ORDER BY mca.similarity_score DESC
LIMIT 10;

-- 7. CLUSTER ASSIGNMENT SUMMARY BY RANK
SELECT 
    c.name as cluster_name,
    COUNT(CASE WHEN mca.rank = 1 THEN 1 END) as rank1_assignments,
    COUNT(CASE WHEN mca.rank = 2 THEN 1 END) as rank2_assignments,
    COUNT(CASE WHEN mca.rank = 3 THEN 1 END) as rank3_assignments,
    COUNT(*) as total_assignments
FROM clusters c
LEFT JOIN multi_cluster_assignments mca ON c.id = mca.cluster_id
GROUP BY c.id, c.name
ORDER BY total_assignments DESC;

-- 8. FIND DICHOS WITH CLOSE RANK 1 vs RANK 2
SELECT 
    d.dicho,
    d.translation,
    c1.name as rank1_cluster,
    mca1.similarity_score as rank1_score,
    c2.name as rank2_cluster,
    mca2.similarity_score as rank2_score,
    ROUND(mca1.similarity_score - mca2.similarity_score, 4) as score_gap
FROM multi_cluster_assignments mca1
JOIN multi_cluster_assignments mca2 ON mca1.dicho_id = mca2.dicho_id
JOIN dichos d ON mca1.dicho_id = d.id
JOIN clusters c1 ON mca1.cluster_id = c1.id
JOIN clusters c2 ON mca2.cluster_id = c2.id
WHERE mca1.rank = 1 
  AND mca2.rank = 2
  AND (mca1.similarity_score - mca2.similarity_score) <= 0.1
ORDER BY score_gap ASC
LIMIT 10;

-- 9. COMPREHENSIVE DICHO ANALYSIS
SELECT 
    d.dicho,
    d.translation,
    d.expanded_context_usage,
    GROUP_CONCAT(
        c.name || ' (Rank ' || mca.rank || ' - Score: ' || ROUND(mca.similarity_score, 4) || ')'
        ORDER BY mca.rank
        SEPARATOR ' | '
    ) as cluster_profile
FROM dichos d
LEFT JOIN multi_cluster_assignments mca ON d.id = mca.dicho_id
LEFT JOIN clusters c ON mca.cluster_id = c.id
WHERE d.id = 1  -- Change this to any dicho ID
GROUP BY d.id, d.dicho, d.translation, d.expanded_context_usage;
