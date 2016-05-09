#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    proofchecker
    ~~~~~
    :copyright: (c) 2014-2015 by Halfmoon Labs, Inc.
    :copyright: (c) 2016 blockstack.org
    :license: MIT, see LICENSE for more details.
"""

import os
import sys
import unittest
import requests

# Hack around absolute paths
current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(current_dir + "/../")
sys.path.insert(0, parent_dir)

from proofchecker import profile_to_proofs, profile_v3_to_proofs
from proofchecker import contains_valid_proof_statement
from proofchecker import get_proof_from_txt_record

test_users = ['ryan', 'werner']

test_domains = [{"username": "muneeb", 'domain': 'muneebali.com'}]

check_proofs = ['twitter', 'facebook', 'github']

BASE_URL = 'https://resolver.onename.com/v2/users/'


def get_profile(username):

    resp = requests.get(BASE_URL + username, timeout=10)

    data = resp.json()

    if 'zone_file' in data[username]:
        return data[username]['profile'], data[username]['zone_file']
    else:
        return data[username]['profile'], None


class ProofcheckerTestCase(unittest.TestCase):

    def tearDown(self):
        pass

    def test_proofs(self):
        """ Check twitter proof
        """

        for username in test_users:
            profile, zone_file = get_profile(username)

            if zone_file is not None:
                proofs = profile_v3_to_proofs(profile, username)
            else:
                proofs = profile_to_proofs(profile, username)

            for proof in proofs:

                if proof['service'] in check_proofs:
                    self.assertTrue(proof['valid'])

    def test_domain_proof(self):
        """ Check domain proof
        """

        for test_domain in test_domains:
            username = test_domain['username']
            domain = test_domain['domain']

            proof_txt = get_proof_from_txt_record(domain)

            validProof = contains_valid_proof_statement(proof_txt, username)

            self.assertTrue(validProof)

if __name__ == '__main__':

    unittest.main()
