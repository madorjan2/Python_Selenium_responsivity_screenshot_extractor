from PIL import Image
import numpy as np

def get_nav_height(path):
	img = Image.open(path)
	arr_img = np.asarray(img)
	return arr_img.shape[0]
def post_process_image(path, number_of_pictures, pixels_to_scroll, pixels_scrolled_last, is_landscape):
	navbar_path = f'{path}/navbar{is_landscape * '_landscape'}.png'
	img = Image.open(navbar_path)
	arr_img = np.asarray(img)
	pointer = arr_img.shape[0]
	for pic_index in range(1, number_of_pictures+1):
		img_path = f"{path}/screenshot_{is_landscape * 'landscape_'}{pic_index}.png"
		img = Image.open(img_path)
		curr_img = np.asarray(img)
		arr_img = np.concatenate((arr_img[:pointer], curr_img), axis=0)
		if pic_index == number_of_pictures - 1:
			pointer += pixels_scrolled_last
		else:
			pointer += pixels_to_scroll
	out_path = f"{path}/full_screenshot{is_landscape * '_landscape'}.png"
	Image.fromarray(arr_img).save(out_path)