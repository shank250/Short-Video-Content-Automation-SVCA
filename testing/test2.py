from SecretColors import palette
p = palette.Palette("material" ,color_mode = 'rgb')
colors = p.random(no_of_colors = 10)
#  gradient=False
def convert_rgb_to_255(rgb):
    return tuple(int(x * 255) for x in rgb)

rgb_values = (0.5, 0.3, 0.8)
rgb_255_0 = convert_rgb_to_255(colors[0])
rgb_list = []
for i in range(10):
    rgb_255 = convert_rgb_to_255(colors[i])
    rgb_list.append(rgb_255)

# rgb_255_1 = convert_rgb_to_255(colors[1])
def calculate_brightness(rgb):
    r, g, b = rgb
    return (r * 299 + g * 587 + b * 114) / 1000

def select_light_and_dark_colors(colors):
    lightest_color = None
    darkest_color = None

    for rgb in colors:
        brightness = calculate_brightness(rgb)

        if lightest_color is None or brightness > calculate_brightness(lightest_color):
            lightest_color = rgb

        if darkest_color is None or brightness < calculate_brightness(darkest_color):
            darkest_color = rgb

    return lightest_color, darkest_color
# colors = rgb_list
# print(rgb_255_0,rgb_255_1)
print(select_light_and_dark_colors(rgb_list))