from importlib import resources
import sys
import sqlite3
import logging
from modflux import config

log = logging.getLogger("modflux")

def run():
    conn = sqlite3.connect(config.DATABASE_FILE)
    
    current_version, = next(conn.cursor().execute('PRAGMA user_version'), (0, ))
    migrations = resources.files('migrations').iterdir()
    
    for migration in list(migrations)[current_version:]:
        cur = conn.cursor()
        try:
            log.info("Applying %s", migration.name)
            cur.executescript("begin;" + migration.read_text())
        except Exception as e:
            log.error("Failed migration %s: %s", migration.name, e)
            cur.execute("rollback")
            sys.exit(1)
        else:
            cur.execute("commit")

if __name__ == "__main__":
    run()