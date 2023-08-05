# -*- coding: utf-8 -*-
"""
@authors: Suhas Sharma and Rahul P
"""

import fluffypancakes

def test_fluffypancakes(url):
    return fluffypancakes.serve(url, progressBar=True)

def test_answer():
    assert test_fluffypancakes('pes.edu') == -1