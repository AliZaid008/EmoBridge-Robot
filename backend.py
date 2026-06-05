import sqlite3

def add_child(name, age, avatar, preferred_theme):

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO children
    (name, age, avatar, preferred_theme)
    VALUES (?, ?, ?, ?)
    """, (name, age, avatar, preferred_theme))

    conn.commit()
    conn.close()

    print("Child Added Successfully")

def add_session(
    child_id,
    start_time,
    end_time,
    dominant_emotion,
    avg_confidence,
    engagement_rate,
    distraction_count
):

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO sessions
    (
        child_id,
        start_time,
        end_time,
        dominant_emotion,
        avg_confidence,
        engagement_rate,
        distraction_count
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        child_id,
        start_time,
        end_time,
        dominant_emotion,
        avg_confidence,
        engagement_rate,
        distraction_count
    ))

    conn.commit()
    conn.close()

    print("Session Added Successfully")

def add_game_result(
    session_id,
    score,
    difficulty_level,
    total_attempts,
    success_rate,
    reaction_time
):

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO game_results
    (
        session_id,
        score,
        difficulty_level,
        total_attempts,
        success_rate,
        reaction_time
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        session_id,
        score,
        difficulty_level,
        total_attempts,
        success_rate,
        reaction_time
    ))

    conn.commit()
    conn.close()

    print("Game Result Added Successfully") 

def add_badge(
    child_id,
    badge_name,
    earned_date
):

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO badges
    (
        child_id,
        badge_name,
        earned_date
    )
    VALUES (?, ?, ?)
    """,
    (
        child_id,
        badge_name,
        earned_date
    ))

    conn.commit()
    conn.close()

    print("Badge Added Successfully")  

def search_child(name):

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM children
    WHERE name = ?
    """, (name,))

    result = cursor.fetchone()

    conn.close()

    return result 

def update_child_age(child_id, new_age):

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE children
    SET age = ?
    WHERE child_id = ?
    """, (new_age, child_id))

    conn.commit()
    conn.close()

    print("Child Updated Successfully") 

def delete_child(child_id):

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM children
    WHERE child_id = ?
    """, (child_id,))

    conn.commit()
    conn.close()

    print("Child Deleted Successfully")             

def search_session(session_id):

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM sessions
    WHERE session_id = ?
    """, (session_id,))

    result = cursor.fetchone()

    conn.close()

    return result    

def update_session_emotion(session_id, new_emotion):

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE sessions
    SET dominant_emotion = ?
    WHERE session_id = ?
    """, (new_emotion, session_id))

    conn.commit()
    conn.close()

    print("Session Updated Successfully")

def delete_session(session_id):

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM sessions
    WHERE session_id = ?
    """, (session_id,))

    conn.commit()
    conn.close()

    print("Session Deleted Successfully")

def search_game_result(result_id):

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM game_results
    WHERE result_id = ?
    """, (result_id,))

    result = cursor.fetchone()

    conn.close()

    return result


def update_game_score(result_id, new_score):

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE game_results
    SET score = ?
    WHERE result_id = ?
    """, (new_score, result_id))

    conn.commit()
    conn.close()

    print("Game Result Updated Successfully")

def delete_game_result(result_id):

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM game_results
    WHERE result_id = ?
    """, (result_id,))

    conn.commit()
    conn.close()

    print("Game Result Deleted Successfully")  

def search_badge(badge_id):

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM badges
    WHERE badge_id = ?
    """, (badge_id,))

    result = cursor.fetchone()

    conn.close()

    return result 

def delete_badge(badge_id):

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM badges
    WHERE badge_id = ?
    """, (badge_id,))

    conn.commit()
    conn.close()

    print("Badge Deleted Successfully")  

def get_total_children():

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM children
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total       

def get_total_sessions():

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM sessions
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

def get_total_badges():

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM badges
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

def get_average_score():

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT AVG(score)
    FROM game_results
    """)

    avg = cursor.fetchone()[0]

    conn.close()

    return avg

def get_most_common_emotion():

    conn = sqlite3.connect("emobridge.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT dominant_emotion
    FROM sessions
    GROUP BY dominant_emotion
    ORDER BY COUNT(*) DESC
    LIMIT 1
    """)

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None