class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def ci_install(user, cwd):
    """Installs the databases"""
    if not check_local_software:
        print(bcolors.FAIL + "lpf dependencies are not installed, and databases cant be indexed" + bcolors.ENDC)
        sys.exit()

    database_list = ["resfinder_db",
                     "plasmidfinder_db",
                     "virulencefinder_db",
                     "bacteria_db",
                     "cdd_db",
                     "virus_db"]

    for item in database_list:
        if not os.path.exists('/opt/lpf_databases/{}'.format(item)):
            os.system("sudo mkdir -m 777 /opt/lpf_databases/{}".format(item))
        if not os.path.exists('/opt/lpf_databases/{}/{}.name'.format(item, item)):
            os.chdir('/opt/lpf_databases/{}'.format(item))
            if item == 'bacteria_db':
                os.system('cp {}/tests/fixtures/database/* /opt/lpf_databases/bacteria_db/.'.format(cwd))
                os.system("kma index -i {}.fasta.gz -o {} -m 14 -Sparse ATG".format(item, item))
            else:
                os.system(
                    "sudo wget https://cge.food.dtu.dk/services/MINTyper/lpf_databases/{0}/export/{0}.fasta.gz".format(
                        item))
                os.system("kma index -i {}.fasta.gz -o {} -m 14".format(item, item))

    if not os.path.exists('/opt/lpf_databases/mlst_db'):
        os.chdir('/opt/lpf_databases')
        os.system("git clone https://bitbucket.org/genomicepidemiology/mlst_db.git")
        os.system('chmod -R 777 /opt/lpf_databases/mlst_db')
        os.chdir('/opt/lpf_databases/mlst_db')
        file_list = os.listdir('/opt/lpf_databases/mlst_db')
        for item in file_list:
            if os.path.exists('/opt/lpf_databases/mlst_db/{0}/{0}.fsa'.format(item)):
                os.chdir('/opt/lpf_databases/mlst_db/{}'.format(item))
                os.system("kma index -i {}.fsa -o {} -m 14".format(item, item))
                os.chdir('/opt/lpf_databases/mlst_db')



    os.chdir(cwd)
    os.system("cp scripts/schemes/notes.txt /opt/lpf_databases/virulencefinder_db/notes.txt")
    os.system("cp scripts/schemes/phenotypes.txt /opt/lpf_databases/resfinder_db/phenotypes.txt")
    if not os.path.exists('/opt/lpf_databases/cdd_db/cddid_all.tbl'):
        os.system('sudo wget https://cge.food.dtu.dk/services/MINTyper/lpf_databases/cdd_db/export/cddid_all.tbl -O /opt/lpf_databases/cdd_db/cddid_all.tbl')
    if not os.path.exists('/opt/lpf_databases/lpf.db'):
        create_sql_db()
    elif os.path.getsize('/opt/lpf_databases/lpf.db') == 0:
        create_sql_db()
    insert_bacteria_references_into_sql()

    os.chdir(cwd)

    move_lpf_repo()