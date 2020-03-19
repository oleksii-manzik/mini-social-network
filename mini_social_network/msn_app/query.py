NUMBER_OF_LIKES_QUERY = """
    SELECT id, is_liked
    FROM msn_app_like AS l1
    JOIN (
        SELECT owner_id, MAX(created) AS created
        FROM msn_app_like
        WHERE post_id = %s
        GROUP BY owner_id
    ) AS l2
    ON l1.owner_id = l2.owner_id
    AND l1.created = l2.created"""

IS_LIKED_QUERY = """
    SELECT id, is_liked 
    FROM msn_app_like
    WHERE owner_id = %s
    AND post_id = %s
    AND created = (
        SELECT MAX(created) 
        FROM msn_app_like
        WHERE owner_id = %s
        AND post_id = %s)"""
