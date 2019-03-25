from PIL import Image
import numpy as np
import requests
from io import BytesIO
from shuttle import Shuttle


class Traffic:
    def __init__(self):
        self.image_h, self.image_w = 1250, 1500
        self.c_lat, self.c_long = 42.354518, -71.097159
        self.mapquest_url = "https://www.mapquestapi.com/traffic/v2/flow?key=TtNWARciA4XjSX4Q0a9GRywGPieAPCnz&" \
                            "mapLat="+str(self.c_lat)+"&mapLng="+str(self.c_long)+"&mapHeight="+str(self.image_h)+"&mapWidth="+str(self.image_w)+"&mapScale=6770"
        # self.mapquest_url = "https://www.mapquestapi.com/staticmap/v5/map?key=TtNWARciA4XjSX4Q0a9GRywGPieAPCnz&" \
        #                     "center="+str(self.c_lat)+","+str(self.c_long)+"&mapHeight="+str(self.image_h)+"&mapWidth="+str(self.image_w)+"&mapScale=6770"
        self.traffic_image = Image.open("traffic_test.png")
        self.traffic_dict = {}

    def update(self):
        response = requests.get(self.mapquest_url)
        self.traffic_image = Image.open(BytesIO(response.content))
        self.traffic_image.save("traffic_test.png")

    def show(self):
        self.traffic_image.show()

    def plot_coord(self, coord):
        pixel_x, pixel_y = self.coord_to_pixel(coord)
        map_im = Image.open("static-map.png")
        map_im = np.array(map_im.convert('RGB'))

        temp_im = self.traffic_image.convert('RGB')
        temp_im = np.array(temp_im)

        # final_image = np.round(map_im - np.where(temp_im==0, 1, 0)+ temp_im)
        final_image = temp_im // 3 + map_im*2 // 3
        final_image = Image.fromarray(final_image)

        temp_im = final_image.convert('RGB')
        temp_im_pixels = temp_im.load()

        block_size = 30
        shuttle_color = (0, 0, 255)
        for i in range(-block_size//2, block_size//2):
            for j in range(-block_size//2, block_size//2):
                if (i**2+j**2)**0.5 < block_size/2:
                    temp_im_pixels[pixel_x+i, pixel_y+j] = shuttle_color

        # final_image = Image.fromarray(final_image)
        temp_im.show()

    def coord_to_pixel(self, coord):
        pixel_x = (coord[1] - self.c_long)*46658 + self.image_w/2
        pixel_y = (coord[0] - self.c_lat) * -62971 + self.image_h / 2
        return pixel_x, pixel_y


def main():
    traffic = Traffic()
    traffic.update()
    shuttle = Shuttle()
    shuttle_coord = shuttle.coordinates
    traffic.plot_coord(shuttle_coord)


if __name__ == '__main__':
        main()
