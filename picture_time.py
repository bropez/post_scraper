"""Picture Time
This script opens a headless browser to a specified css selector, takes a screenshot,
and saves it to a specified directory with a specified filename as a png

This script requires that `selenium` be installed within the Python environment
you are running this script in.

This file can also be imported as a module and contains the following functions:

    * headless - Creates a headless firefox browser object to use
    * nsfw_check - Checks if it is a nsfw reddit post and says yes to the 18+ prompt
    * screenshot_title - The browser takes a screenshot of the title
    * screenshot_comment - The browser takes a screenshot of the comment
"""


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import os, socket
import time
from threading import Timer
from text_to_speech import tts
from tqdm import tqdm


def headless() -> webdriver.Firefox:
    """Creates a headless firefox browser object to use

    Args:
        None
    
    Returns:
        b (webdriver.Firefox): The browser object to use for the rest of the script
    """
    options = webdriver.FirefoxOptions()
    options.set_preference("dom.push.enabled", False)
    options.headless = True
    b = webdriver.Firefox(options=options)
    b.set_window_size(1920, 1080)
    return b


def nsfw_check(b: webdriver.Firefox):
    """Checks if it is a nsfw reddit post and says yes to the 18+ prompt

    Args:
        b (webdriver.Firefox): The browser object to use

    Returns:
        None
    """
    try:
        b.find_element_by_css_selector('._1HunhFR-0b-AYs0WG9mU_P.i2sTp1duDdXdwoKi1l8ED').click()
    except NoSuchElementException:
        pass


def screenshot_title(browser: webdriver.Firefox, link: str, directoryname: str, filename: str, id: str):
    """The browser takes a screenshot of the title

    Args:
        link (str): The link to the post's title
        directoryname (str): The directory to save the screenshot in
        filename (str): The name of the file to save as
        id (str): The id of the title to move to on the page

    Returns:
        None
    """
    browser.get(link)
    nsfw_check(browser)

    if id:
        element = browser.find_element_by_id(id)
        browser.execute_script("arguments[0].scrollIntoView(alignToTop=false);", element)

    browser.save_screenshot("{}/pictures/{}.png".format(directoryname, filename))


def screenshot_comment(comments: list, directory_name: str):
    """The browser takes a screenshot of the comment

    Args:
        link (str): The link to the post's comment
        directoryname (str): The directory to save the screenshot in
        filename (str): The name of the file to save as
        id (str): The id of the comment to move to on the page

    Returns:
        None
    """
    browser = headless()

    title = comments.pop(0)
    post, post_link = title.split("|||")
    post_title, post_author = post.split(" submitted by ")
    tts(post_title, directory_name, ".title")
    screenshot_title(browser, post_link, directory_name, ".title", None)

    file = open("{}/.description.txt".format(directory_name), "w")
    file.write(post_title + "\n" + post_link)
    file.close()

    # youtube description
    file = open("{}/.ytdescription.txt".format(directory_name), "w")
    file.write("{}\n\nPosted by u/{}".format(post_title, post_author))
    file.close()

    f = open("{}/.comments.txt".format(directory_name), "a")
    
    for comment in tqdm(comments):
        comment_number, comment_text, comment_link, comment_id = comment.split("|||")
        id = "t1_{}".format(comment_id)
        file_name = "comment{}".format(comment_number)
        
        browser.get(comment_link)
        nsfw_check(browser)

        try:
            browser.find_element_by_css_selector('.PiO8QDmoJoOL2sDjJAk4C.j9NixHqtN2j8SKHcdJ0om').click()
        except NoSuchElementException:
            pass

        if id:
            try:
                element = browser.find_element_by_id(id)
            except NoSuchElementException:
                time.sleep(10)
                element = browser.find_element_by_id(id)
            browser.execute_script("arguments[0].scrollIntoView(alignToTop=false);", element)
        browser.save_screenshot("{}/pictures/{}.png".format(directory_name, file_name))

        tts(comment_text, directory_name, file_name)
        f.write("{}|||{}\n".format(comment_number, comment_link))

    f.close()
    browser.quit()

    
if __name__ == '__main__':
    os.mkdir('tester_dir')
    os.mkdir('tester_dir/pictures')
    # for number in range(3):
    #     screenshot_comment(
    #         'https://www.reddit.com/r/AskReddit/comments/cy1rvg/every_sexual_fantasy_youve_ever_had_just_came/eyp9lbg/',
    #         'tester_dir', 
    #         'test_file{}'.format(str(number)),
    #         "t1_eyp9lbg"
    #     )
