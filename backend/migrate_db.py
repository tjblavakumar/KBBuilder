"""
Database migration script to add provider and api_key columns to existing database
"""
import sqlite3
from pathlib import Path

def migrate():
    db_path = Path("kb_builder.db")
    
    if not db_path.exists():
        print("Database doesn't exist yet. No migration needed.")
        return
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(knowledgebases)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'provider' not in columns:
            print("Adding 'provider' column...")
            cursor.execute("ALTER TABLE knowledgebases ADD COLUMN provider VARCHAR(50) DEFAULT 'bedrock'")
            cursor.execute("UPDATE knowledgebases SET provider = 'bedrock' WHERE provider IS NULL")
            print("✓ Added 'provider' column")
        else:
            print("'provider' column already exists")
        
        if 'api_key' not in columns:
            print("Adding 'api_key' column...")
            cursor.execute("ALTER TABLE knowledgebases ADD COLUMN api_key VARCHAR(500)")
            print("✓ Added 'api_key' column")
        else:
            print("'api_key' column already exists")
        
        conn.commit()
        print("\n✓ Migration completed successfully!")
        
    except Exception as e:
        print(f"✗ Migration failed: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
