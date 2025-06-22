import sqlite3
from contextlib import contextmanager
from threading import Lock
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import OperationalError

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.sqlite_lock = Lock()
        try:
            # Configure SQLAlchemy engine
            self.engine = create_engine(
                f'sqlite:///{db_path}',
                connect_args={
                    'timeout': 5,
                    'check_same_thread': False,
                    'isolation_level': 'IMMEDIATE'
                }
            )
            
            self.Session = scoped_session(sessionmaker(bind=self.engine))
        except OperationalError as e:
            logger.error(f"SQLAlchemy engine creation error: {e}")
            raise

    @contextmanager
    def get_db(self):
        conn = None
        try:
            with self.sqlite_lock:
                conn = sqlite3.connect(
                    self.db_path,
                    timeout=5,
                    isolation_level='IMMEDIATE'
                )
                conn.row_factory = sqlite3.Row
                yield conn
        except sqlite3.Error as e:
            logger.error(f"SQLite connection error: {e}")
            if conn:
                conn.rollback()
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_db: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                try:
                    conn.close()
                except Exception:
                    logger.error(f"Error closing SQLite connection: {e}")

    @contextmanager
    def get_session(self):
        session = self.Session()
        try:
            yield session
        except Exception as e:
            session.rollback()
            logger.error(f"Session error: {e}")
            raise
        else:
            try:
                session.commit()
            except Exception as e:
                session.rollback()
                logger.error(f"Session commit error: {e}")
                raise
        finally:
            session.close()
            self.Session.remove()

    def __del__(self):
        if hasattr(self, 'engine'):
            try:
                self.engine.dispose()
            except Exception as e:
                logger.error(f"Error disposing engine: {e}")

db_manager = DatabaseManager('login_app/database.db')