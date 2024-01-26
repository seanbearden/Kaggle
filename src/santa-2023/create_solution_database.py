import pandas as pd
import sqlite3
import zipfile

with zipfile.ZipFile('../../res/data/santa-2023.zip', 'r') as z:
    with z.open('puzzle_info.csv') as f:
        puzzle_info = pd.read_csv(f)

    with z.open('puzzles.csv') as f:
        puzzles = pd.read_csv(f)

    with z.open('sample_submission.csv') as f:
        submission = pd.read_csv(f)

# Connect to a new SQLite database (in-memory for this example)
conn = sqlite3.connect('solutions.db')
cursor = conn.cursor()

# Create a table
create_table_query = """
CREATE TABLE IF NOT EXISTS solutions (
    id INTEGER PRIMARY KEY,
    moves TEXT,
    count INTEGER
);
"""
cursor.execute(create_table_query)

# Create a table
create_table_query = """
CREATE TABLE IF NOT EXISTS symmetric_moves (
    puzzle_type TEXT,
    moves TEXT,
    count INTEGER
);
"""
cursor.execute(create_table_query)

# Create a table
create_table_query = """
CREATE TABLE IF NOT EXISTS puzzles (
    id INTEGER PRIMARY KEY,
    puzzle_type TEXT,
    solution_state TEXT,
    initial_state TEXT,
    num_wildcards INTEGER,
    FOREIGN KEY (id) REFERENCES solutions(id)
);
"""
cursor.execute(create_table_query)

puzzles.to_sql('puzzles', conn, if_exists='append', index=False)

# Commit the changes and close the connection
conn.commit()
conn.close()