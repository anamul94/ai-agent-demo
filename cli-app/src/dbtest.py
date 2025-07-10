from sqlalchemy import create_engine, MetaData, Table, select, desc, and_
from sqlalchemy.engine import Engine
from constant import DB_FILE, TABLE_NAME
from agno.storage.sqlite import SqliteStorage

def get_engine(db_file: str = DB_FILE) -> Engine:
    return create_engine(f"sqlite:///{db_file}")

def reflect_table(engine: Engine, table_name: str) -> Table:
    metadata = MetaData()
    metadata.reflect(bind=engine)
    if table_name not in metadata.tables:
        SqliteStorage(
        table_name=TABLE_NAME, db_file=DB_FILE
        
    ),
        # raise ValueError(f"Table '{table_name}' not found in the database.")
    return metadata.tables[table_name]

def read_all_sessions(db_file: str = DB_FILE, table_name: str = TABLE_NAME):
    """Read all records from the session table."""
    engine = get_engine(db_file)
    table = reflect_table(engine, table_name)

    with engine.connect() as conn:
        stmt = select(table)
        results = conn.execute(stmt).fetchall()
        return [dict(row._mapping) for row in results]

def read_sessions(session_id: str = None, user_id: str = None, db_file: str = DB_FILE, table_name: str = TABLE_NAME):
    """Read session(s) by session_id or user_id (or both)."""
    engine = get_engine(db_file)
    table = reflect_table(engine, table_name)

    with engine.connect() as conn:
        stmt = select(table)

        filters = []
        if session_id:
            filters.append(table.c.session_id == session_id)
        if user_id:
            filters.append(table.c.user_id == user_id)

        if filters:
            stmt = stmt.where(and_(*filters))

        results = conn.execute(stmt).fetchall()
        return [dict(row._mapping) for row in results]

def get_last_session_id_by_user(user_id: str, db_file: str = DB_FILE, table_name: str = TABLE_NAME):
    """Get the latest session_id for a given user_id based on updated_at timestamp."""
    engine = get_engine(db_file)
    table = reflect_table(engine, table_name)

    with engine.connect() as conn:
        stmt = (
            select(table.c.session_id)
            .where(table.c.user_id == user_id)
            .order_by(desc(table.c.updated_at))  # Or desc(table.c.created_at)
            .limit(1)
        )
        result = conn.execute(stmt).fetchone()
        return result[0] if result else None

# Optional: quick test
if __name__ == "__main__":
    print("All Sessions:")
    # print(read_all_sessions())

    print("\nSessions for user_id='user-123':")
    print(read_sessions(user_id="anamul"))

    print("\nSession for session_id='session-abc':")
    print(read_sessions(session_id="fixed_id_for_demo"))

    print("\nLast session_id for user_id='user-123':")
    print(get_last_session_id_by_user("anamul"))
