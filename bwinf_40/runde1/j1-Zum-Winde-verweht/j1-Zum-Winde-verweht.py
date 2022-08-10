#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
from pipe import map

def prepare_file_row(entry):
  return list(entry.strip().split()
              | map(lambda x: int(x)))

def init_bauwerk(entry):
  return dict(zip(["x", "y"], entry))

def init_windrad(windrad, haeuser):
  windrad["hoehe"] = min(
    list(haeuser
         | map(lambda haus: berechne_abstand(windrad, haus)))
  )
  return windrad

def berechne_abstand(windrad, haus):
  return math.sqrt(
    sum([((windrad.get("x")-haus.get("x")) ** 2),
        ((windrad.get("y")-haus.get("y")) ** 2)])
  )/10

def print_windrad(windrad):
  print('Windrad ({x:>6}/{y:>6}) darf {hoehe:>6.2f}m hoch sein'.format(**windrad))
  
if __name__ == "__main__":
  for counter in range(1, 5):
    file = "beispieldaten/landkreis{}.txt".format(counter)
    print("\n\n{}\n\nDatei: {}\n".format("-"*(len(file)+7), file))

    with open(file, "r") as myfile:
      file_data = list(myfile.readlines()
                       | map(prepare_file_row))
      cnt_haeuser, cnt_windraeder = file_data.pop(0)
      haeuser = list(file_data[:cnt_haeuser]
                     | map(init_bauwerk))
      windraeder = list(file_data[cnt_haeuser:]
                        | map(init_bauwerk)
                        | map(lambda entry: init_windrad(entry, haeuser))
                        | map(print_windrad))