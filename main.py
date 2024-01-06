import os
import json
from datetime import datetime

from selenium.webdriver.common.by import By

from image_post_processing import post_process_image
import driver_manager


resolutions = json.load(open('res_list.json'))
default_path = os.path.join(os.getcwd(), f'screenshots\\{datetime.now().strftime("%Y_%m_%d_%H_%M")}')

for function_name in dir(driver_manager):
    if function_name.startswith('visit_'):
        current_visit = getattr(driver_manager, function_name)
        driver, dir_name = current_visit()
        for resolution in resolutions:
            res_tuple = (resolution["width"], resolution["height"])

            path = os.path.join(default_path, dir_name, f'{resolution["width"]}x{resolution["height"]}')
            os.makedirs(path)

            landscape = False


            for current_width, current_height in [res_tuple, res_tuple[::-1]]:
                driver, dir_name = current_visit(driver)
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

                landscape = not landscape

        teardown_function_name = function_name.replace('visit_', 'post_')
        teardown_function = getattr(driver_manager, teardown_function_name)
        teardown_function(driver)
