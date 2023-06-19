import os
import sys
import subprocess
import sqlite3
import src.sqlCommands as sqlCommands
def set_up_lpf_db():
    sql_bacteria_reference_list = []
    bacteria_db_reference_list = []

    if not os.path.exists('/opt/lpf_databases/bacteria_db/bacteria_db'):
        sys.exit("bacteria_db is not found. Install prior to setting up the SQL database.")

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
                    cmd = "~/bin/kma seq2fasta -t_db /opt/lpf_databases/bacteria_db/bacteria_db -seqs {}".format(t)
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

