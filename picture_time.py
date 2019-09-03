from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import os


def headless():
    options = webdriver.FirefoxOptions()
    options.set_preference("dom.push.enabled", False)
    options.headless = True
    b = webdriver.Firefox(options=options)

    return b


def nsfw_check(b):
    try:
        b.find_element_by_css_selector('._1HunhFR-0b-AYs0WG9mU_P.i2sTp1duDdXdwoKi1l8ED').click()
    except NoSuchElementException:
        pass


def screenshot_title(link, directoryname, filename, id):
    browser = headless()
    browser.get(link)
    nsfw_check(browser)

    if id:
        element = browser.find_element_by_id(id)
        browser.execute_script("arguments[0].scrollIntoView(alignToTop=false);", element)


    browser.save_screenshot("{}/pictures/{}.png".format(directoryname, filename))
    browser.quit()


def screenshot_comment(link, directoryname, filename, id):
    browser = headless()
    browser.get(link)
    nsfw_check(browser)


    try:
        browser.find_element_by_css_selector('.PiO8QDmoJoOL2sDjJAk4C.j9NixHqtN2j8SKHcdJ0om').click()
    except NoSuchElementException:
        pass

    if id:
        element = browser.find_element_by_id(id)
        browser.execute_script("arguments[0].scrollIntoView(alignToTop=false);", element)


    browser.save_screenshot("{}/pictures/{}.png".format(directoryname, filename))
    browser.quit()

    
if __name__ == '__main__':
    os.mkdir('tester_dir')
    os.mkdir('tester_dir/pictures')
    for number in range(3):
        screenshot_comment(
            'https://www.reddit.com/r/AskReddit/comments/cy1rvg/every_sexual_fantasy_youve_ever_had_just_came/eyp9lbg/',
            'tester_dir', 
            'test_file{}'.format(str(number)),
            "t1_eyp9lbg"
        )
