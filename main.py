import os
from datetime import datetime

from selenium.webdriver.common.by import By
import json

from image_post_process import post_process_image
import gettourl


json_file = open('res_list.json')
resolutions = json.load(json_file)
additional_path = f'screenshots\\{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'
default_path = os.path.join(os.getcwd(), additional_path)

for function_name in dir(gettourl):
    if function_name.startswith('visit_'):
        current_function = getattr(gettourl, function_name)
        driver, dirname = current_function()
        for actual_res in resolutions:
            print(default_path)
            res_tuple = (actual_res["width"], actual_res["height"])
            tuples = [res_tuple, res_tuple[::-1]]
            device_name = actual_res["device"]
            current_path = os.getcwd()

            path = os.path.join(default_path, dirname, device_name)
            os.makedirs(path)

            landscape = False


            for current_width, current_height in tuples:
                driver, dirname = current_function(driver)
                driver.set_window_size(current_width, current_height)
                driver.execute_script(f"window.scrollTo(0,0)")

                navbar = driver.find_element(By.TAG_NAME, 'nav')
                navbar.screenshot(f"{path}/navbar{landscape * '_landscape'}.png")


                driver.execute_script("""
                                    var navbar = arguments[0];
                                    navbar.parentNode.removeChild(navbar);
                                    """, navbar)

                height_of_page = driver.execute_script("return $(document).height()")

                i = 1
                pixels_to_scroll = current_height // 2
                previous_pos = -1
                pixels_scrolled_last = 0
                while previous_pos != driver.execute_script("return window.pageYOffset"):
                    y_pos = driver.execute_script("return window.pageYOffset")
                    pixels_scrolled_last = y_pos - previous_pos
                    previous_pos = y_pos
                    driver.find_element(By.TAG_NAME, 'body').screenshot(f"{path}/screenshot_{landscape * 'landscape_'}{i}.png")
                    driver.execute_script(f"window.scrollTo(0, {pixels_to_scroll * i})")
                    i += 1

                post_process_image(path, i-1, pixels_to_scroll, pixels_scrolled_last, landscape)
                print(pixels_scrolled_last)

                landscape = not landscape

        teardown_function_name = function_name.replace('visit_', 'post_')
        teardown_function = getattr(gettourl, teardown_function_name)
        teardown_function(driver)
