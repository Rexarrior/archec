
def read_coords(path):
    with open(path, 'rt', encoding="utf8") as f:
        text = f.read()
    return coords_from_text(text)

def coords_from_text(text):
    lines = text.strip().split('\n')
    coordinates = [lines[i] for i in range(4, len(lines), 3)]
    coordinates = [coord.replace("N", "").replace("E", "").replace(",", ".").split(' ') for coord in coordinates]
    return coordinates

def make_url(coords):
    base_url = "https://yandex.ru/maps/?l=sat"
    delim = "%2C"
    points_delim = "~"
    first_lat = float(coords[0][1])
    first_lng =  float(coords[0][0])
    lat = first_lat
    lng =first_lng
    part = f"&ll={lat}{delim}{lng}&rl={lat}{delim}{lng}"
    for point in coords[1:]:
        new_lat = float(point[1]) 
        new_lng =  float(point[0])
        df_lat = new_lat - lat
        df_lng = new_lng - lng
        lat = new_lat
        lng = new_lng
        part += f"{points_delim}{df_lat}{delim}{df_lng}"
    df_lat = first_lat - lat
    df_lng = first_lng - lng
    part += f"{points_delim}{df_lat}{delim}{df_lng}"

    return base_url + part


#sample_url https://yandex.ru/maps/?l=sat&ll=32.837181%2C69.299002&rl=32.833603%2C69.298605~-0.001615%2C0.000998~0.001813%2C0.000296~0.001491%2C-0.000898&rlt=area&z=16

def coords_from_url(url):
    # https://yandex.ru/maps/?l=sat&ll=32.775813%2C69.231477&rl=32.775829%2C69.231608~0.001115%2C0.000063~0.001695%2C0.000609~0.004570%2C0.000084~0.000300%2C-0.001112~-0.005386%2C-0.000030~-0.001030%2C0.000267~-0.003583%2C-0.000114~-0.000139%2C0.000141&rlt=area&z=18
    url = url.replace("https://yandex.ru/maps/?l=sat&", "")
    parts = url.split("&")
    center_part = parts[0]
    parts = parts[1].split("~")
    start_part = parts[0]
    start_part = start_part.replace("rl=", "")
    start_points = [float(el) for el in start_part.split("%2C")]
    last_point = [start_points[0], start_points[1]]
    points = [start_points]
    for point_part in parts[1:]:
        current_point_shift = [float(el) for el in point_part.split("%2C")]
        current_point = [last_point[0] + current_point_shift[0], last_point[1] + current_point_shift[1]]
        points.append(current_point)
        last_point = current_point
    return points


def test_url_builder(read_coords, make_url):
    coords = read_coords("sample_in.txt")
    url = make_url(coords)
    print(url)

def test_url_parser():
    import pprint 
    # url = "https://yandex.ru/maps/?l=sat&ll=32.775813%2C69.231477&rl=32.775829%2C69.231608~0.001115%2C0.000063~0.001695%2C0.000609~0.004570%2C0.000084~0.000300%2C-0.001112~-0.005386%2C-0.000030~-0.001030%2C0.000267~-0.003583%2C-0.000114~-0.000139%2C0.000141&rlt=area&z=18"
    url = "https://yandex.ru/maps/?l=sat&ll=32.785235%2C69.231772&rl=32.774928%2C69.231638~0.003432%2C0.000093~-0.000065%2C0.000289~0.004033%2C0.000046~0.000193%2C-0.000998~-0.004077%2C-0.000053~-0.000258%2C0.000320~-0.003161%2C-0.000015~0.000098%2C-0.000421~-0.002021%2C-0.000051~-0.000182%2C0.000758&rlt=area&z=16"
    points = coords_from_url(url)
    pprint.pprint(points)

if __name__ == "__main__":
    # test_url_builder(read_coords, make_url)
    test_url_parser()