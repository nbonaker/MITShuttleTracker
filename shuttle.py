from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import time
import csv
import os.path

named_tuple = time.localtime() # get struct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
print(time_string)


class Shuttle:
    def __init__(self, shuttle="saferidebostone"):
        self.shuttle_name = shuttle
        self.tracking_url = "https://mobi.mit.edu/transit/route?feed=nextbus&direction=loop&agency=mit&route=" \
                            + self.shuttle_name
        self.coordinates = None
        self.update(write_data=False)

    def update(self, write_data=True):
        print("REQUESTING SHUTTLE LOCATION: ")
        self.update_time()
        req = Request(self.tracking_url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        text = str(webpage)
        start = text.find("ModoTransitVehicleNextBus")
        shuttle_text = text[start:]

        vehicle_num = shuttle_text[26:30].replace('"','')

        stop = shuttle_text.find("kgomap:latitude")
        shuttle_text = shuttle_text[:stop]

        location_text = shuttle_text[(shuttle_text.find('"kgoDeflatedData":["') + 20):shuttle_text.find('"]},')]
        if len(location_text) == 0:
            print("SHUTTLE IS OFFLINE")
            self.coordinates = None
        else:
            shuttle_location = [float(num) for num in location_text.split('","')]
            print("VEHICLE NUMBER "+vehicle_num+" IS AT: " + str(shuttle_location))
            self.coordinates = tuple(shuttle_location)
            if write_data:
                self.write_data()

    def update_time(self):
        self.local_time = time.localtime() # get struct_time
        self.string_time = time.strftime("%m/%d/%Y, %H:%M:%S", self.local_time)

    def write_data(self):
        date, time = self.string_time.split(',')
        write_header = not os.path.isfile('data/'+self.shuttle_name+'.csv')
        with open('data/'+self.shuttle_name+'.csv', mode='a') as csv_file:
            fieldnames = ['date', 'time', 'latitude', 'longitude']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames,lineterminator='\n')
            if write_header:
                writer.writeheader()
            writer.writerow({'date': date, 'time': time, 'latitude': self.coordinates[0], 'longitude': self.coordinates[1]})
        csv_file.close()

def main():
    shuttle = Shuttle()
    while True:
        time.sleep(15)
        shuttle.update()


if __name__ == '__main__':
        main()
