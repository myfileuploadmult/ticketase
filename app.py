from datetime import datetime
from flask import Flask
from flask import request
from flask import render_template
import json
import requests
import pprint
import copy
from tabulate import tabulate

TOKEN = None

boilarplate_result_data = {'EGAROSINDHUR PROVATI (737)': {'train_name': 'EGAROSINDHUR PROVATI (737)', 'available_seats': [{'from_city': 'Dhaka', 'to_city': 'Bhairab_Bazar', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 8: {'type': 'SHOVAN', 'fare': 85.0, 'seat_counts': 13}}}, {'from_city': 'Dhaka', 'to_city': 'Kuliarchar', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 184.0, 'seat_counts': 1}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 8: {'type': 'SHOVAN', 'fare': 100.0, 'seat_counts': 16}}}, {'from_city': 'Dhaka', 'to_city': 'Bajitpur', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 125.0, 'seat_counts': 1}, 8: {'type': 'SHOVAN', 'fare': 105.0, 'seat_counts': 41}}}, {'from_city': 'Dhaka', 'to_city': 'Sararchar', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 8: {'type': 'SHOVAN', 'fare': 110.0, 'seat_counts': 34}}}, {'from_city': 'Dhaka', 'to_city': 'Manikkhali', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 248.0, 'seat_counts': 1}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 8: {'type': 'SHOVAN', 'fare': 135.0, 'seat_counts': 20}}}, {'from_city': 'Dhaka', 'to_city': 'Gachihata', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 8: {'type': 'SHOVAN', 'fare': 135.0, 'seat_counts': 20}}}, {'from_city': 'Dhaka', 'to_city': 'Kishorganj', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 248.0, 'seat_counts': 40}, 7: {'type': 'S_CHAIR', 'fare': 160.0, 'seat_counts': 54}, 8: {'type': 'SHOVAN', 'fare': 135.0, 'seat_counts': 119}}}]}, 'MAHANAGAR PROVATI (704)': {'train_name': 'MAHANAGAR PROVATI (704)', 'available_seats': [{'from_city': 'Dhaka', 'to_city': 'Bhairab_Bazar', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 105.0, 'seat_counts': 25}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Brahmanbaria', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 150.0, 'seat_counts': 1}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Laksam', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 255.0, 'seat_counts': 1}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Gunabati', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 547.0, 'seat_counts': 4}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 285.0, 'seat_counts': 17}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Feni', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 575.0, 'seat_counts': 3}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 300.0, 'seat_counts': 12}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Chattogram', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 932.0, 'seat_counts': 16}, 3: {'type': 'SNIGDHA', 'fare': 777.0, 'seat_counts': 147}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 621.0, 'seat_counts': 33}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 405.0, 'seat_counts': 53}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}]}, 'KISHORGANJ EXPRESS (781)': {'train_name': 'KISHORGANJ EXPRESS (781)', 'available_seats': [{'from_city': 'Dhaka', 'to_city': 'Bhairab_Bazar', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 105.0, 'seat_counts': 8}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Kuliarchar', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 120.0, 'seat_counts': 7}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Bajitpur', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 242.0, 'seat_counts': 1}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 125.0, 'seat_counts': 17}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Sararchar', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 130.0, 'seat_counts': 33}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Manikkhali', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 160.0, 'seat_counts': 24}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Gachihata', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 160.0, 'seat_counts': 17}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Kishorganj', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 368.0, 'seat_counts': 8}, 3: {'type': 'SNIGDHA', 'fare': 305.0, 'seat_counts': 45}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 160.0, 'seat_counts': 177}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}]}, 'CHATTALA EXPRESS (802)': {'train_name': 'CHATTALA EXPRESS (802)', 'available_seats': [{'from_city': 'Dhaka', 'to_city': 'Bhairab_Bazar', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 156.0, 'seat_counts': 1}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 8: {'type': 'SHOVAN', 'fare': 85.0, 'seat_counts': 1}}}, {'from_city': 'Dhaka', 'to_city': 'Cumilla', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 345.0, 'seat_counts': 2}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 225.0, 'seat_counts': 2}, 8: {'type': 'SHOVAN', 'fare': 190.0, 'seat_counts': 24}}}, {'from_city': 'Dhaka', 'to_city': 'Laksam', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 255.0, 'seat_counts': 12}, 8: {'type': 'SHOVAN', 'fare': 210.0, 'seat_counts': 23}}}, {'from_city': 'Dhaka', 'to_city': 'Feni', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 300.0, 'seat_counts': 8}, 8: {'type': 'SHOVAN', 'fare': 250.0, 'seat_counts': 33}}}, {'from_city': 'Dhaka', 'to_city': 'Chattogram', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 621.0, 'seat_counts': 5}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 405.0, 'seat_counts': 28}, 8: {'type': 'SHOVAN', 'fare': 340.0, 'seat_counts': 38}}}, {'from_city': 'Dhaka', 'to_city': 'Shashidal', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 200.0, 'seat_counts': 5}, 8: {'type': 'SHOVAN', 'fare': 170.0, 'seat_counts': 5}}}, {'from_city': 'Dhaka', 'to_city': 'Nangolkot', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 8: {'type': 'SHOVAN', 'fare': 225.0, 'seat_counts': 10}}}, {'from_city': 'Dhaka', 'to_city': 'Hasanpur', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 8: {'type': 'SHOVAN', 'fare': 230.0, 'seat_counts': 15}}}, {'from_city': 'Dhaka', 'to_city': 'Kumira', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 8: {'type': 'SHOVAN', 'fare': 340.0, 'seat_counts': 5}}}]}, 'EGAROSINDHUR GODHULI (749)': {'train_name': 'EGAROSINDHUR GODHULI (749)', 'available_seats': [{'from_city': 'Dhaka', 'to_city': 'Kuliarchar', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 184.0, 'seat_counts': 2}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 8: {'type': 'SHOVAN', 'fare': 100.0, 'seat_counts': 7}}}, {'from_city': 'Dhaka', 'to_city': 'Bajitpur', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 196.0, 'seat_counts': 1}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 8: {'type': 'SHOVAN', 'fare': 105.0, 'seat_counts': 22}}}, {'from_city': 'Dhaka', 'to_city': 'Manikkhali', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 248.0, 'seat_counts': 2}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 8: {'type': 'SHOVAN', 'fare': 135.0, 'seat_counts': 19}}}, {'from_city': 'Dhaka', 'to_city': 'Gachihata', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 248.0, 'seat_counts': 2}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 8: {'type': 'SHOVAN', 'fare': 135.0, 'seat_counts': 20}}}, {'from_city': 'Dhaka', 'to_city': 'Kishorganj', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 248.0, 'seat_counts': 19}, 7: {'type': 'S_CHAIR', 'fare': 160.0, 'seat_counts': 13}, 8: {'type': 'SHOVAN', 'fare': 135.0, 'seat_counts': 127}}}]}, 'MOHANAGAR EXPRESS (722)': {'train_name': 'MOHANAGAR EXPRESS (722)', 'available_seats': [{'from_city': 'Dhaka', 'to_city': 'Bhairab_Bazar', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 105.0, 'seat_counts': 20}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Cumilla', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 432.0, 'seat_counts': 1}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 225.0, 'seat_counts': 10}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Laksam', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 255.0, 'seat_counts': 16}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Feni', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 575.0, 'seat_counts': 5}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 300.0, 'seat_counts': 11}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Chattogram', 'seat_types': {1: {'type': 'AC_B', 'fare': 1398.0, 'seat_counts': 2}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 777.0, 'seat_counts': 112}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 405.0, 'seat_counts': 81}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Nangolkot', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 270.0, 'seat_counts': 10}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Kumira', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 405.0, 'seat_counts': 5}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}]}, 'UPABAN EXPRESS (739)': {'train_name': 'UPABAN EXPRESS (739)', 'available_seats': [{'from_city': 'Dhaka', 'to_city': 'Bhairab_Bazar', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 105.0, 'seat_counts': 22}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Shaistaganj', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 235.0, 'seat_counts': 8}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}]}, 'TURNA (742)': {'train_name': 'TURNA (742)', 'available_seats': [{'from_city': 'Dhaka', 'to_city': 'Bhairab_Bazar', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 196.0, 'seat_counts': 2}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 105.0, 'seat_counts': 15}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Brahmanbaria', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 288.0, 'seat_counts': 2}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 150.0, 'seat_counts': 41}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Cumilla', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 432.0, 'seat_counts': 1}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 225.0, 'seat_counts': 16}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Laksam', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 255.0, 'seat_counts': 8}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Feni', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 300.0, 'seat_counts': 1}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': 'Chattogram', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 777.0, 'seat_counts': 43}, 4: {'type': 'F_BERTH', 'fare': 932.0, 'seat_counts': 2}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 405.0, 'seat_counts': 1}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}]}}
search_track_map = []
search_results = {}
const_seat_types = {
                1: {
                    "type": "AC_B",
                    "fare": "N/A",
                    "seat_counts": 0,
                },
                2: {
                    "type": "AC_S",
                    "fare": "N/A",
                    "seat_counts": 0,
                },
                3: {
                    "type": "SNIGDHA",
                    "fare": "N/A",
                    "seat_counts": 0,
                },
                4: {
                    "type": "F_BERTH",
                    "fare": "N/A",
                    "seat_counts": 0,
                },
                5: {
                    "type": "F_SEAT",
                    "fare": "N/A",
                    "seat_counts": 0,
                },
                6: {
                    "type": "F_CHAIR",
                    "fare": "N/A",
                    "seat_counts": 0,
                },
                7: {
                    "type": "S_CHAIR",
                    "fare": "N/A",
                    "seat_counts": 0,
                },
                8: {
                    "type": "SHOVAN",
                    "fare": "N/A",
                    "seat_counts": 0,
                },
            }
request_count = 0
table_headers_list = ['Station Combination']
all_station_list = ['Abdulpur', 'Ahsanganj', 'Akhaura', 'Akkelpur', 'Alamdanga', 'Ashuganj', 'Azampur', 'B Sirajul Islam', 'Bajitpur', 'Banani', 'Barhatta', 'BBSetu_E', 'Benapole', 'Bhairab_Bazar', 'Bhanga', 'Bhanga_Junction', 'Bhanugach', 'Bheramara', 'Biman_Bandar', 'Birampur', 'Bogura', 'Bonar_Para', 'Boral_Bridge', 'Brahmanbaria', 'Burimari', 'Chandpur', 'Chandpur_Court', 'Chapai Nawabganj', 'Chatmohar', 'Chattogram', 'Chilahati', 'Choumuhani', 'Chuadanga', "Cox's Bazar", 'Cumilla', 'Darshana_Halt', 'Dewanganj_Bazar', 'Dhaka', 'Dhaka_Cantonment', 'Dinajpur', 'Domar', 'Faridpur', 'Feni', 'Fulbari', 'Gachihata', 'Gafargaon', 'Gaibandha', 'Gouripur_Myn', 'Harashpur', 'Ishwardi', 'Ishwardi Bypass', 'Islampur_Bazar', 'Jamalpur_Town', 'Jamtail', 'Jashore', 'Jhikargacha', 'Joydebpur', 'Joypurhat', 'Kaunia', 'Khulna', 'Kishorganj', 'Kolkata', 'Kotchandpur', 'Kulaura', 'Kuliarchar', 'Kumarkhali', 'Kurigram', 'Kushtia_Court', 'Laksam', 'Lalmonirhat', 'Maijgaon', 'Mawa', 'Melandah_Bazar', 'Mohanganj', 'Mubarakganj', 'Mymensingh', 'Nangolkot', 'Narsingdi', 'Natore', 'Nayapara', 'Netrakona', 'New Jalpaiguri', 'Nilphamari', 'Noakhali', 'Noapara', 'Padma', 'Pangsha', 'Parbatipur', 'Pirganj', 'Poradaha', 'Quasba', 'Rajbari', 'Rajshahi', 'Ramu', 'Rangpur', 'Rohanpur', 'Saidpur', 'Santahar', 'Sararchar', 'Sarishabari', 'SH M Monsur Ali', 'Shaistaganj', 'Shamshernagar', 'Shibchar', 'Sreemangal', 'Sylhet', 'Tangail', 'Tarakandi', 'Thakurgaon_Road', 'Ullapara']
# table_header = "Station Combination\t\t\t\t"
for seat in const_seat_types:
    # table_header += f"\t {const_seat_types[seat]['type']}"
    table_headers_list.append(const_seat_types[seat]['type'])
table_headers_list.append("Buy")

#token generator by signing in
def set_token(token: str):
    global TOKEN
    TOKEN = token
def fetch_token() -> str:
    mobile_number = "01819748714"
    password = "Shaha017/"
    if not mobile_number or not password:
        raise Exception("Fixed mobile number or password not configured.")
    url = f"https://railspaapi.shohoz.com/v1.0/web/auth/sign-in"
    payload = {"mobile_number": mobile_number, "password": password}
    max_retries = 2
    retry_count = 0
    while retry_count < max_retries:
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 422:
                raise Exception("Server-side Mobile Number or Password is incorrect. Please wait a moment while we resolve this issue.")
            elif response.status_code >= 500:
                retry_count += 1
                if retry_count == max_retries:
                    raise Exception("We're facing a problem with the Bangladesh Railway website. Please try again in a few minutes.")
                continue
            data = response.json()
            token = data["data"]["token"]
            return token
        except requests.RequestException as e:
            error_str = str(e)
            if "NameResolutionError" in error_str or "Failed to resolve" in error_str:
                raise Exception("We couldn't reach the Bangladesh Railway website. Please try again in a few minutes.")
            raise Exception(f"Failed to fetch token: {error_str}")


def getStationListByTrainCode(train_id):
    global TOKEN
    if not TOKEN:
        TOKEN = fetch_token()
        set_token(TOKEN)
    url = 'https://railspaapi.shohoz.com/v1.0/web/train-routes'
    params = {'model': train_id}
    headers = {"Authorization": f"Bearer {TOKEN}"}
    result = requests.post(url, params=params, headers=headers)
    station_list = []
    if result.status_code == 200:
        result_json = json.loads(result.text)
        for route in result_json['data']['routes']:
            station_list.append(route['city'])
    return station_list

def getSuitableTrainList(from_city, to_city, journey_date):
    global TOKEN
    if not TOKEN:
        TOKEN = fetch_token()
        set_token(TOKEN)
    url = f"https://railspaapi.shohoz.com/v1.0/web/bookings/search-trips-v2?from_city={from_city}&to_city={to_city}&date_of_journey={journey_date}&seat_class=S_CHAIR"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    print(url)
    result = requests.get(url, headers=headers)
    suitable_train_list = []
    if result.status_code == 200:
        result_json = json.loads(result.text)
        for train in result_json['data']['trains']:
            train_code = train['trip_number'][-4:-1]
            suitable_train_list.append(train_code)
    return suitable_train_list


def processSearch(from_city, to_city, journey_date, suitable_train_codes):
    global TOKEN
    if not TOKEN:
        TOKEN = fetch_token()
        set_token(TOKEN)
    url = f"https://railspaapi.shohoz.com/v1.0/web/bookings/search-trips-v2?from_city={from_city}&to_city={to_city}&date_of_journey={journey_date}&seat_class=S_CHAIR"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    result = requests.get(url, headers = headers)
    if result.status_code == 200:
        result_json = json.loads(result.text)
        for train in result_json['data']['trains']:
            if train['trip_number'][-4:-1] not in suitable_train_codes:
                continue
            key = train['trip_number']
            search_results[key] = search_results.get(key, {"train_name": key, "available_seats": []})
            seat_types = copy.deepcopy(const_seat_types)
            has_seat = False
            for seat in train['seat_types']:
                total_available_seats = int(seat['seat_counts']['online']) + int(seat['seat_counts']['offline'])
                if total_available_seats > 0:
                    has_seat = True
                    seat_key = seat['key']
                    total_fare = float(seat['fare']) + seat['vat_amount']
                    seat_types[seat_key]['fare'] = total_fare
                    seat_types[seat_key]['seat_counts'] = total_available_seats
            if has_seat:
                search_results[key]['available_seats'].append({"from_city": from_city, "to_city": to_city, "seat_types": seat_types})


def showResults():
    for train_name in search_results:
        print(train_name)
        combo_list = search_results[train_name]['available_seats']
        # print(combo_list)
        if len(combo_list) < 1:
            print("No tickets available")
            continue
        # print(table_header)
        # print("-------------------------------------------------------------------------------------------")
        # for station_combo in combo_list:
        #     result_line = f"{station_combo['from_city']} -> {station_combo['to_city']}\t\t\t\t"
        #     for i in range(1, 9):
        #         result_line += f"\t {station_combo['seat_types'][i]['seat_counts']}"
        #     print(result_line)
        # print('\n')
        table_data = []
        for station_combo in combo_list:
            row_item = [f"{station_combo['from_city']} -> {station_combo['to_city']}"]
            for i in range(1, 9):
                row_item.append(station_combo['seat_types'][i]['seat_counts'])
            table_data.append(row_item)
        print(tabulate(table_data, headers=table_headers_list))
        print("\n")


#
# demo_result = {'PARJOTAK EXPRESS (816)': {'train_name': 'PARJOTAK EXPRESS (816)', 'available_seats': [{'from_city': 'Dhaka', 'to_city': 'Chattogram', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 855.0, 'seat_counts': 32}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 450.0, 'seat_counts': 45}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}, {'from_city': 'Dhaka', 'to_city': "Cox's Bazar", 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 1325.0, 'seat_counts': 24}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 695.0, 'seat_counts': 19}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}]}, 'SONAR BANGLA EXPRESS (788)': {'train_name': 'SONAR BANGLA EXPRESS (788)', 'available_seats': [{'from_city': 'Dhaka', 'to_city': 'Chattogram', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 855.0, 'seat_counts': 168}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 450.0, 'seat_counts': 224}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}]}, 'MAHANAGAR PROVATI (704)': {'train_name': 'MAHANAGAR PROVATI (704)', 'available_seats': [{'from_city': 'Dhaka', 'to_city': 'Chattogram', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 932.0, 'seat_counts': 16}, 3: {'type': 'SNIGDHA', 'fare': 777.0, 'seat_counts': 150}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 621.0, 'seat_counts': 18}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 405.0, 'seat_counts': 20}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}]}, 'CHATTALA EXPRESS (802)': {'train_name': 'CHATTALA EXPRESS (802)', 'available_seats': [{'from_city': 'Dhaka', 'to_city': 'Chattogram', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 'N/A', 'seat_counts': 0}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 621.0, 'seat_counts': 6}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 405.0, 'seat_counts': 23}, 8: {'type': 'SHOVAN', 'fare': 340.0, 'seat_counts': 32}}}]}, 'SUBORNO EXPRESS (702)': {'train_name': 'SUBORNO EXPRESS (702)', 'available_seats': [{'from_city': 'Dhaka', 'to_city': 'Chattogram', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 855.0, 'seat_counts': 182}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 450.0, 'seat_counts': 1}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}]}, 'MOHANAGAR EXPRESS (722)': {'train_name': 'MOHANAGAR EXPRESS (722)', 'available_seats': [{'from_city': 'Dhaka', 'to_city': 'Chattogram', 'seat_types': {1: {'type': 'AC_B', 'fare': 1398.0, 'seat_counts': 20}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 777.0, 'seat_counts': 125}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 405.0, 'seat_counts': 128}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}]}, 'COXS BAZAR EXPRESS (814)': {'train_name': 'COXS BAZAR EXPRESS (814)', 'available_seats': [{'from_city': 'Dhaka', 'to_city': 'Chattogram', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 855.0, 'seat_counts': 26}, 4: {'type': 'F_BERTH', 'fare': 'N/A', 'seat_counts': 0}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}]}, 'TURNA (742)': {'train_name': 'TURNA (742)', 'available_seats': [{'from_city': 'Dhaka', 'to_city': 'Chattogram', 'seat_types': {1: {'type': 'AC_B', 'fare': 'N/A', 'seat_counts': 0}, 2: {'type': 'AC_S', 'fare': 'N/A', 'seat_counts': 0}, 3: {'type': 'SNIGDHA', 'fare': 777.0, 'seat_counts': 70}, 4: {'type': 'F_BERTH', 'fare': 932.0, 'seat_counts': 5}, 5: {'type': 'F_SEAT', 'fare': 'N/A', 'seat_counts': 0}, 6: {'type': 'F_CHAIR', 'fare': 'N/A', 'seat_counts': 0}, 7: {'type': 'S_CHAIR', 'fare': 405.0, 'seat_counts': 32}, 8: {'type': 'SHOVAN', 'fare': 'N/A', 'seat_counts': 0}}}]}}
# demo_headers_list = ['Station Combination', 'AC_B', 'AC_S', 'SNIGDHA', 'F_BERTH', 'F_SEAT', 'F_CHAIR', 'S_CHAIR', 'SHOVAN']


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def homePage():
    global search_track_map
    global search_results
    if request.method == 'POST':
        # return render_template('result.html', headers = table_headers_list, result = boilarplate_result_data)
        search_results = {}
        datetime_object = datetime.strptime(request.form['journey_date'], '%Y-%m-%d')
        formatted_date = datetime_object.strftime('%d-%b-%Y')
        from_city = request.form['from_city']
        to_city = request.form['to_city']
        journey_date = formatted_date
        train_codes = getSuitableTrainList(from_city, to_city, journey_date)
        print(train_codes)
        for train_code in train_codes:
            station_list = getStationListByTrainCode(train_code)
            start_station_index = station_list.index(from_city)
            end_station_index = station_list.index(to_city)
            print(station_list)
            # print(f"{start_station_index}  {end_station_index}")
            # print('\n')
            for j in range(end_station_index, len(station_list)):
                for i in range(0, start_station_index + 1):
                    print(f"{station_list[i]} -> {station_list[j]}")
                    search_string = station_list[i] + station_list[j]
                    if search_string not in search_track_map:
                        search_track_map.append(search_string)
                        processSearch(station_list[i], station_list[j], journey_date, train_codes)
        # showResults()
        search_results_copy = copy.deepcopy(search_results)
        search_results = {}
        search_track_map = []
        return render_template('result.html', headers = table_headers_list, result = search_results_copy, date = journey_date)
    else:
        return render_template('index.html', all_station_list = all_station_list)

# if __name__ == '__main__':
#     app.run(debug=False, port=3000, host='0.0.0.0')