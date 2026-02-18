#!/usr/bin/env python3
"""
One-time cleanup utility: remove persisted API keys from knowledge base records.
"""
from datetime import datetime, timezone

from database import SessionLocal, KnowledgeBase


def main() -> int:
    db = SessionLocal()
    try:
        updated = (
            db.query(KnowledgeBase)
            .filter(KnowledgeBase.api_key.isnot(None))
            .update(
                {
                    KnowledgeBase.api_key: None,
                    KnowledgeBase.updated_at: datetime.now(timezone.utc),
                },
                synchronize_session=False,
            )
        )
        db.commit()
        print(f"Cleared API keys for {updated} knowledge base(s).")
        return 0
    except Exception as exc:
        db.rollback()
        print(f"Failed to cleanup API keys: {exc}")
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
