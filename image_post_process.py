from PIL import Image
import numpy as np

def post_process_image(path, number_of_pictures, pixels_to_scroll, pixels_scrolled_last, is_landscape):
	navbar_path = f'{path}/navbar{is_landscape * '_landscape'}.png'
	img = Image.open(navbar_path)
	arr_img = np.asarray(img)
	navbar_height = arr_img.shape[0]
	for pic_index in range(1, number_of_pictures+1):
		img_path = f"{path}/screenshot_{is_landscape * 'landscape_'}{pic_index}.png"
		img = Image.open(img_path)
		curr_img = np.asarray(img)
		if pic_index == number_of_pictures:
			arr_img = np.concatenate((arr_img[:(navbar_height + (pic_index - 2) * pixels_to_scroll) + pixels_scrolled_last], curr_img), axis=0)
		else:
			arr_img = np.concatenate((arr_img[:(navbar_height + (pic_index - 1) * pixels_to_scroll)], curr_img), axis=0)
	out_path = f"{path}/full_screenshot{is_landscape * '_landscape'}.png"
	Image.fromarray(arr_img).save(out_path)