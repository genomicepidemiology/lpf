import os
import sys
import subprocess
import sqlite3
import src.sqlCommands as sqlCommands


def create_sql_db():
    print("Creating SQL database")
    conn = sqlite3.connect('/opt/lpf_databases/lpf.db')
    c = conn.cursor()

    c.execute(
        """CREATE TABLE IF NOT EXISTS sample_table(entry_id TEXT PRIMARY KEY, sample_type TEXT, reference_id TEXT)""")
    conn.commit()

    c.execute(
        """CREATE TABLE IF NOT EXISTS sequence_table(entry_id TEXT PRIMARY KEY, header TEXT, sequence TEXT)""")
    conn.commit()

    c.execute(
        """CREATE TABLE IF NOT EXISTS meta_data_table(entry_id TEXT PRIMARY KEY, meta_data_json TEXT)""")  # Consider better design for meta_data
    conn.commit()

    c.execute(
        """CREATE TABLE IF NOT EXISTS status_table(entry_id TEXT PRIMARY KEY, input_file TEXT, status TEXT, time_stamp TEXT, stage TEXT)""")
    conn.commit()

    c.execute(
        """CREATE TABLE IF NOT EXISTS sync_table(last_sync TEXT, sync_round TEXT)""")
    conn.commit()
    conn.close()
    print("SQL database created")


def insert_bacteria_references_into_sql_db():
    sql_bacteria_reference_list = []
    bacteria_db_reference_list = []

    with open('/opt/lpf_databases/bacteria_db/bacteria_db.name', 'r') as f:
        for line in f:
            bacteria_db_reference_list.append(line.rstrip())

    if os.path.exists('/opt/lpf_databases/lpf.db'):
        result = sqlCommands.sql_fetch_all("SELECT header FROM sequence_table", '/opt/lpf_databases/lpf.db')
    else:
        sys.exit("lpf.db is not found")

    print("calculating the difference between the reference table and the database")
    local_missing_references_in_sql_db = set(set(bacteria_db_reference_list) - set(result))
    local_missing_references_in_bacteria_db = set(set(result) - set(bacteria_db_reference_list))

    if len(local_missing_references_in_sql_db) > 0:
        conn = sqlite3.connect('/opt/lpf_databases/lpf.db')
        print("Updating SQL database with new references. Number of new references: {}".format(len(local_missing_references_in_sql_db)))
        with open ('/opt/lpf_databases/bacteria_db/bacteria_db.name', 'r') as f:
            t = 0
            for line in f:
                t += 1
                if t%100 == 0:
                    print("{} references processed".format(t))
                if line.rstrip() in local_missing_references_in_sql_db: #set search
                    cmd = "kma seq2fasta -t_db /opt/lpf_databases/bacteria_db/bacteria_db -seqs {}".format(t)
                    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                    output = proc.communicate()[0].decode().rstrip()
                    reference_header_text = output.split("\n")[0][1:]
                    sequence = output.split("\n")[1]
                    entry_id = md5.md5_of_sequence(sequence)
                    cmd = 'INSERT OR IGNORE INTO sample_table VALUES ("{}", "{}", "{}")'.format(entry_id, 'bacteria', '')
                    sqlCommands.sql_execute_command(cmd, '/opt/lpf_databases/lpf.db')
                    cmd = 'INSERT OR IGNORE INTO sequence_table VALUES ("{}", "{}", "{}")'.format(entry_id, reference_header_text, '')
                    sqlCommands.sql_execute_command(cmd, '/opt/lpf_databases/lpf.db')
        conn.commit()
        conn.close()

