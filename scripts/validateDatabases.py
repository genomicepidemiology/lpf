#!/usr/bin/env python3

"""
Validate that the databases are installed correctly.
"""

import os
import sys
import logging

class ValidateDatabases:
    def __init__(self):
        self.lpf_db = "/opt/lpf_databases/bacteria_db/bacteria_db.ATG.name"
        self.resfinder_db = "/opt/lpf_databases/resfinder_db/resfinder_db.name"
        self.virulencefinder_db = "/opt/lpf_databases/virulencefinder_db/virulencefinder_db.name"
        self.plasmidfinder_db = "/opt/lpf_databases/plasmidfinder_db/plasmidfinder_db.name"
        #virus
        #metagenomic

    def validate(self):
        if not os.path.isfile(self.lpf_db):
            print("Missing database: {}".format(self.lpf_db))
            sys.exit(1)
        if not os.path.isfile(self.resfinder_db):
            print("Missing database: {}".format(self.resfinder_db))
            sys.exit(1)
        if not os.path.isfile(self.virulencefinder_db):
            print("Missing database: {}".format(self.virulencefinder_db))
            sys.exit(1)
        if not os.path.isfile(self.plasmidfinder_db):
            print("Missing database: {}".format(self.plasmidfinder_db))
            sys.exit(1)
        return (0)

    def run(self):
        self.validate()
