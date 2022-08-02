#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import Counter

def init_parkplaetze_regulaer(data):
  start, stop = data[0].strip().split(" ")
  return "".join([chr(char) for char in range(ord(start), ord(stop)+1)])

def init_parkplaetze_quer(parkplaetze, data):
  querplaetze = get_autos_auf_querparkplaetzen(data)
  ret_val = list("_"*(len(parkplaetze) - len(querplaetze.keys())*2))
  
  for key in querplaetze.keys():    
    ret_val.insert(int(key), querplaetze.get(key)*2)
  return ret_val

def get_autos_auf_querparkplaetzen(data):
  return { x.strip().split()[1]: x.strip().split()[0] for x in data[2:] }

def regulaerer_parkplatz_ist_blockiert(parkplatz_nr, parkplaetze):
  return "".join(parkplaetze["quer_moved"])[parkplatz_nr] not in ["_", "#"]
  
def auto_blockiert_nach_links(car, position, parkplaetze1):
  try:
    return "".join(parkplaetze["quer_original"])[position-1] == car[0]
  except:
    return False

def auto_blockiert_nach_rechts(car, position, parkplaetze1):
  return not auto_blockiert_nach_links(car, position, parkplaetze1)
  
def get_free_slots(parkplatz, parkplaetze):
  return {
    "spaces_before": dict(Counter(parkplaetze["quer_moved"][0:parkplatz])).pop("_", 0),
    "spaces_after": dict(Counter(parkplaetze["quer_moved"][parkplatz:])).pop("_", 0)
  }

def verschiebe_blockierende_autos(car, parkplatz, parkplaetze):
  blocking_car = "".join(parkplaetze["quer_moved"])[parkplatz]*2
  blocking_car_idx = parkplaetze["quer_moved"].index(blocking_car)
  slots = get_free_slots(parkplatz, parkplaetze)

  if any([slots["spaces_after"] == 0,
          all([auto_blockiert_nach_links(blocking_car, parkplatz, parkplaetze),
               (slots["spaces_before"] >= 1)])]):
    return verschiebe_nach_links(parkplaetze, blocking_car_idx)
  return verschiebe_nach_rechts(parkplaetze, blocking_car_idx)    
    
def verschiebe_nach_links(parkplaetze, blocking_car_idx):
  item_to_remove = len(parkplaetze["quer_moved"][:blocking_car_idx-1]) - parkplaetze["quer_moved"][:blocking_car_idx][::-1].index("_")
  parkplaetze["quer_moved"].pop(item_to_remove)
  parkplaetze["quer_moved"].insert(blocking_car_idx, "#")
  return parkplaetze["quer_moved"]
    
def verschiebe_nach_rechts(parkplaetze, blocking_car_idx):
  item_to_remove = len(parkplaetze["quer_moved"][:blocking_car_idx]) + parkplaetze["quer_moved"][blocking_car_idx:].index("_")
  parkplaetze["quer_moved"].pop(item_to_remove)
  parkplaetze["quer_moved"].insert(blocking_car_idx, "#")
  return parkplaetze["quer_moved"]
 
def auto_position_auf_verschiebeparkplatz(parkplaetze, car):
  return "".join(parkplaetze).find(car)

def print_result(parkplatz, car_to_set_free, parkplaetze, data):  
  verschiebungen = []

  for auto in get_autos_auf_querparkplaetzen(data).values():
    pos_diff = auto_position_auf_verschiebeparkplatz(parkplaetze["quer_moved"], auto) - auto_position_auf_verschiebeparkplatz(parkplaetze["quer_original"], auto)
    
    if pos_diff != 0:
      verschiebungen.append(" {} {} {}".format(auto, abs(pos_diff), "rechts" if ((pos_diff) > 0) else "links" ))

  print("{}: {}".format(car_to_set_free, ",".join(verschiebungen)))

def print_file_info(file, parkplaetze):
  parkplatz_print = ["\n+-{}-+".format("-+-".join(list("-"*len(parkplaetze["regulaer"]))))]
  parkplatz_print.append("\n| {} |".format(" | ".join(parkplaetze["regulaer"])))
  parkplatz_print.append("\n| {} |".format(" | ".join(list("".join(parkplaetze["quer_original"])))))

  print("\n\n{}\n\nDatei: {}".format("-"*(len(file)+7), file))
  print("".join([parkplatz_print[x] for x in [0, 1, 0, 2, 0]]))
  
if __name__ == "__main__":
  for counter in range(0, 6):
    file = "beispieldaten/parkplatz{}.txt".format(counter)
    with open(file, "r") as myfile:
      parkplaetze = {"regulaer": [], "quer_original": [], "quer_moved": []}
      data = myfile.readlines()
      parkplaetze["regulaer"] = init_parkplaetze_regulaer(data)
      parkplaetze["quer_original"] = init_parkplaetze_quer(parkplaetze["regulaer"], data)
  
      print_file_info(file, parkplaetze)
      
      for parkplatz_nr, car_to_set_free in enumerate(parkplaetze["regulaer"]):    
        parkplaetze["quer_moved"] = parkplaetze["quer_original"][0:]

        while regulaerer_parkplatz_ist_blockiert(parkplatz_nr, parkplaetze):
          parkplaetze["quer_moved"] = verschiebe_blockierende_autos(car_to_set_free, parkplatz_nr, parkplaetze)

        print_result(parkplatz_nr, car_to_set_free, parkplaetze, data)