from sqlalchemy import create_engine, text
import os

# Set up path for SQLite DB
DB_PATH = os.path.join('data', 'mlb_data.db')
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

def init_db():
    with engine.begin() as conn:
        # Create League table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS league (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """))

        # Create Division table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS division (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """))

        # Create Team table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS team (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                league_id INTEGER,
                division_id INTEGER,
                FOREIGN KEY (league_id) REFERENCES league(id),
                FOREIGN KEY (division_id) REFERENCES division(id)
            )
        """))

        # Create Standings table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS standings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team TEXT UNIQUE NOT NULL,
                ld TEXT,
                wins INTEGER,
                losses INTEGER,
                win_pct REAL,
                home_win_pct REAL,
                away_win_pct REAL,
                streak TEXT,
                last_10_win_pct REAL,
                east_win_pct REAL,
                cent_win_pct REAL,
                west_win_pct REAL,
                intr_win_pct REAL
            )
        """))

def seed_initial_data():
    with engine.begin() as conn:
        # Insert leagues
        conn.execute(text("INSERT OR IGNORE INTO league (name) VALUES ('AL'), ('NL')"))
        # Insert divisions
        conn.execute(text("INSERT OR IGNORE INTO division (name) VALUES ('E'), ('C'), ('W')"))

def insert_teams():
    teams = [
        # AL East
        ('Baltimore Orioles', 'AL', 'E'),
        ('Boston Red Sox', 'AL', 'E'),
        ('New York Yankees', 'AL', 'E'),
        ('Tampa Bay Rays', 'AL', 'E'),
        ('Toronto Blue Jays', 'AL', 'E'),

        # AL Central
        ('Chicago White Sox', 'AL', 'C'),
        ('Cleveland Guardians', 'AL', 'C'),
        ('Detroit Tigers', 'AL', 'C'),
        ('Kansas City Royals', 'AL', 'C'),
        ('Minnesota Twins', 'AL', 'C'),

        # AL West
        ('Houston Astros', 'AL', 'W'),
        ('Los Angeles Angels', 'AL', 'W'),
        ('Oakland Athletics', 'AL', 'W'),
        ('Seattle Mariners', 'AL', 'W'),
        ('Texas Rangers', 'AL', 'W'),

        # NL East
        ('Atlanta Braves', 'NL', 'E'),
        ('Miami Marlins', 'NL', 'E'),
        ('New York Mets', 'NL', 'E'),
        ('Philadelphia Phillies', 'NL', 'E'),
        ('Washington Nationals', 'NL', 'E'),

        # NL Central
        ('Chicago Cubs', 'NL', 'C'),
        ('Cincinnati Reds', 'NL', 'C'),
        ('Milwaukee Brewers', 'NL', 'C'),
        ('Pittsburgh Pirates', 'NL', 'C'),
        ('St. Louis Cardinals', 'NL', 'C'),

        # NL West
        ('Arizona Diamondbacks', 'NL', 'W'),
        ('Colorado Rockies', 'NL', 'W'),
        ('Los Angeles Dodgers', 'NL', 'W'),
        ('San Diego Padres', 'NL', 'W'),
        ('San Francisco Giants', 'NL', 'W'),
    ]

    with engine.begin() as conn:
        # Fetch league and division mappings
        league_map = {
            row["name"]: row["id"]
            for row in conn.execute(text("SELECT id, name FROM league")).mappings()
        }
        division_map = {
            row["name"]: row["id"]
            for row in conn.execute(text("SELECT id, name FROM division")).mappings()
        }

        # Insert teams
        for name, league, division in teams:
            league_id = league_map[league]
            division_id = division_map[division]
            conn.execute(
                text("INSERT OR IGNORE INTO team (name, league_id, division_id) VALUES (:name, :league_id, :division_id)"),
                {"name": name, "league_id": league_id, "division_id": division_id}
            )

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    init_db()
    seed_initial_data()
    insert_teams()
    print("✅ Database initialized and all team data inserted.")
