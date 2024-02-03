import models

multiple_years = 'AM General ................. 2000 - 1995'
single_year = 'Chevrolet ..................... 1984'
empty = ''
option = 'Gaskets Included: Yes'
multiple_part = 'ERR5199; ETC6660; 17079256;'
single_part = '17111D28'
single_part_all_numbers = '17078832'
description = 'Idle Air Control Valve'
title = 'AC1'


def test_oem_year_dict():
    x = models.oem_year(multiple_years)
    assert type(x) == tuple


def test_oem_year_no_space():
    y, x = models.oem_year(multiple_years)
    assert x['oem'] == 'AM General'


def test_oem_year_number_years():
    y, x = models.oem_year(multiple_years)
    assert {1995, 1996, 1997, 1998, 1999, 2000} == set(x['years'])


def test_oem_year_dict_single():
    y, x = models.oem_year(single_year)
    assert type(x) == dict


def test_oem_year_no_space_single():
    y, x = models.oem_year(single_year)
    assert x['oem'] == 'Chevrolet'


def test_oem_year_number_years_single():
    y, x = models.oem_year(single_year)
    assert {1984} == set(x['years'])


def test_oem_year_is_none():
    y, x = models.oem_year(empty)
    assert x is None
    y, x = models.oem_year(option)
    assert x is None


def test_options():
    y, x = models.options(option)
    assert x['option_name'] == 'Gaskets Included'
    assert x['value'] == 'Yes'


def test_part_numbers_multiple_parts():
    y, x = models.part_numbers(multiple_part)
    assert x == ['ERR5199', 'ETC6660', '17079256']


def test_part_number_single():
    y, x = models.part_numbers(single_part)
    assert x == ['17111D28']

def test_part_number_single_numbers():
    y, x = models.part_numbers(single_part_all_numbers)
    assert x == ['17078832']

def test_part_number_single_list():
    y, x = models.part_numbers(single_part)
    assert type(x) == list


def test_part_number_multiple_list():
    y, x = models.part_numbers(multiple_part)
    print (x)
    assert type(x) == list


def test_part_number_empty():
    y, x = models.part_numbers(empty)
    assert x is None


def test_part_number_with_option():
    y, x = models.part_numbers(option)
    assert x is None


def test_part_number_with_description():
    y, x = models.part_numbers(description)
    assert x is None


def test_part_number_with_title():
    y, x = models.part_numbers(title)
    assert x is None

def test_title():
    y, x = models.titles(title)
    assert x == 'AC1'

def test_not_title():
    y, x = models.titles(empty)
    assert x is None
    y, x = models.titles(single_year)
    assert x is None
    y, x = models.titles(option)
    assert x is None
    y, x = models.titles(multiple_part)
    assert x is None
    y, x = models.titles(description)
    assert x is None

def test_description_type():
    y, x = models.description(description)
    print(x)
    assert type(x) == str

def test_description():
    y, x = models.description(description)
    print(x)
    assert x == 'Idle Air Control Valve'
