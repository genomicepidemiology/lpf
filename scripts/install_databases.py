"""lpf database install script"""
import sys
import os
import argparse
import subprocess

sys.path = [os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')] + sys.path

import setupSqlDb as setup_sql_db

parser = argparse.ArgumentParser(description='.')
parser.add_argument('-info', type=int, help='lpf database install script. Use -override to override existing databases. '
                                            'Use -all to install all databases (without -override existing databases will NOT be re-downloaded). '
                                            'Use -bacteria_db to install only the bacteria database. '
                                            'Use -resfinder_db to install only the resfinder database. '
                                            'Use -plasmidfinder_db to install only the plasmidfinder database. '
                                            'Use -virulencefinder_db to install only the virulencefinder database. '
                                            'Use -mlst_db to install only the mlst database. '
                                            'Use -cdd_db to install only the conserved domain database. '
                                            '-override can be used with any of the other options and will override that database.')
parser.add_argument('-all', action="store_true", dest='all',
                    help='Installs all databases. Will NOT override existing databases. Use the -override flag to override existing databases')
parser.add_argument('-bacteria_db', action="store_true", dest='bacteria_db',
                                    help='bacteria database')
parser.add_argument('-resfinder_db', action="store_true", dest='resfinder_db',
                                    help='resfinder database')
parser.add_argument('-plasmidfinder_db', action="store_true", dest='plasmidfinder_db',
                                    help='plasmidfinder database')
parser.add_argument('-virulencefinder_db', action="store_true", dest='virulencefinder_db',
                                    help='virulencefinder database')
parser.add_argument('-mlst_db', action="store_true", dest='mlst_db',
                help='mlst database')
parser.add_argument('-cdd_db', action="store_true", dest='cdd_db',
                                    help='cdd database')
#parser.add_argument('-virus_db', action="store_true", dest='virus_db',
#                                    help='virus database')
parser.add_argument('-override', action="store_true", dest='override',
                                    help='override existing databases')
args = parser.parse_args()

database_list = []

if args.all:
    database_list = ['bacteria_db', 'resfinder_db', 'plasmidfinder_db', 'virulencefinder_db', 'mlst_db', 'cdd_db']
elif args.bacteria_db:
    database_list.append('bacteria_db')
elif args.resfinder_db:
    database_list.append('resfinder_db')
elif args.plasmidfinder_db:
    database_list.append('plasmidfinder_db')
elif args.virulencefinder_db:
    database_list.append('virulencefinder_db')
elif args.mlst_db:
    database_list.append('mlst_db')
elif args.cdd_db:
    database_list.append('cdd_db')


if args.override:
    os.system('sudo mkdir -m 777 /opt/lpf_db_tmp')
    for item in database_list:
        if item != 'mlst_db':
            os.system('sudo mkdir -m 777 /opt/lpf_db_tmp/{0}'.format(item))
            os.system("sudo wget -O /opt/lpf_db_tmp/{0}/{0}.fasta.gz https://cge.food.dtu.dk/services/MINTyper/lpf_databases/{0}/export/{0}.fasta.gz"
                      .format(item))
        if item == 'bacteria_db':
            os.system(
                "kma index -i /opt/lpf_db_tmp/{0}/{0}.fasta.gz -o /opt/lpf_db_tmp/{0}/{0} -m 14 -Sparse ATG".format(
                    item))
        elif item == 'mlst_db':
            if not os.path.exists('schemes/notes.txt'):
                os.system("cp scripts/schemes/notes.txt /opt/lpf_db_tmp/virulencefinder_db/notes.txt")
                os.system("cp scripts/schemes/phenotypes.txt /opt/lpf_db_tmp/resfinder_db/phenotypes.txt")
            else:
                os.system("cp schemes/notes.txt /opt/lpf_db_tmp/virulencefinder_db/notes.txt")
                os.system("cp schemes/phenotypes.txt /opt/lpf_db_tmp/resfinder_db/phenotypes.txt")
            os.system("git clone https://bitbucket.org/genomicepidemiology/mlst_db.git /opt/lpf_databases/mlst_db")
            os.system('chmod -R 777 /opt/lpf_db_tmp/mlst_db')
            file_list = os.listdir('/opt/lpf_db_tmp/mlst_db')
            for species in file_list:
                if os.path.exists('/opt/lpf_db_tmp/mlst_db/{0}/{0}.fsa'.format(species)):
                    os.system(
                        "kma index -i /opt/lpf_db_tmp/mlst_db/{0}/{0}.fsa -o /opt/lpf_db_tmp/mlst_db/{0}/{0} -m 14".format(
                            species, species))
        else:
            os.system("kma index -i /opt/lpf_db_tmp/{0}/{0}.fasta.gz"
                      " -o /opt/lpf_db_tmp/{0}/{0} -m 14".format(item))
    os.system('sudo mv /opt/lpf_databases /opt/lpf_databases_old_backup')
    os.system('sudo mv /opt/lpf_db_tmp /opt/lpf_databases')


else:
    if not os.path.exists('/opt/lpf_databases'):
        os.system('sudo mkdir -m 777 /opt/lpf_databases')
    for item in database_list:
        if not os.path.exists('/opt/lpf_databases/{0}'.format(item)):
            if item != 'mlst_db':
                os.system('sudo mkdir -m 777 /opt/lpf_databases/{0}'.format(item))
                os.system("sudo wget -O /opt/lpf_databases/{0}/{0}.fasta.gz https://cge.food.dtu.dk/services/MINTyper/lpf_databases/{0}/export/{0}.fasta.gz"
                          .format(item))
            if item == 'bacteria_db':
                os.system("kma index -i /opt/lpf_databases/{0}/{0}.fasta.gz -o /opt/lpf_databases/{0}/{0} -m 14 -Sparse ATG".format(item))
            elif item == 'mlst_db':
                if not os.path.exists('schemes/notes.txt'):
                    os.system("cp scripts/schemes/notes.txt /opt/lpf_databases/virulencefinder_db/notes.txt")
                    os.system("cp scripts/schemes/phenotypes.txt /opt/lpf_databases/resfinder_db/phenotypes.txt")
                else:
                    os.system("cp schemes/notes.txt /opt/lpf_databases/virulencefinder_db/notes.txt")
                    os.system("cp schemes/phenotypes.txt /opt/lpf_databases/resfinder_db/phenotypes.txt")
                os.system("git clone https://bitbucket.org/genomicepidemiology/mlst_db.git /opt/lpf_databases/mlst_db")
                os.system('chmod -R 777 /opt/lpf_databases/mlst_db')
                file_list = os.listdir('/opt/lpf_databases/mlst_db')
                for species in file_list:
                    if os.path.exists('/opt/lpf_databases/mlst_db/{0}/{0}.fsa'.format(species)):
                        os.system("kma index -i /opt/lpf_databases/mlst_db/{0}/{0}.fsa -o /opt/lpf_databases/mlst_db/{0}/{0} -m 14".format(species, species))
            else:
                os.system("kma index -i /opt/lpf_databases/{0}/{0}.fasta.gz -o /opt/lpf_databases/{0}/{0} -m 14".format(item, item))

        else:
            print('Database {0} already exists. Use -override to override existing databases'.format(item))

if not os.path.exists('/opt/lpf_databases/lpf.db'):
    setup_sql_db.create_sql_db()
elif os.path.getsize('/opt/lpf_databases/lpf.db') == 0:
    setup_sql_db.create_sql_db()

setup_sql_db.insert_bacteria_references_into_sql_db()

"""Makes the lpf filesystem"""
    path_list = ["/opt/lpf_data/",
                 "/opt/lpf_analyses/",
                 "/opt/lpf_metadata_json/",
                 "/opt/lpf_metadata_json/individual_json",
                 "/opt/lpf_databases/",
                 "/opt/lpf_reports/",
                 "/opt/lpf_logs/"]
    for item in path_list:
        if not os.path.exists(item):
            os.system("sudo mkdir -m 777 {}".format(item))
            print("Created {}".format(item))
            if item == '/opt/lpf_databases/':
                if os.path.exists('/opt/lpf_databases/lpf.db'):
                    os.system("sudo rm /opt/lpf_databases/lpf.db")
                    print("Removed old lpf.db")