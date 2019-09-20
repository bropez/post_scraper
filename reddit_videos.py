"""Reddit Videos
This script automates getting the hottest posts on r/AskReddit, takes a screenshot of
their title and top comments, creates text to speech audio for each, save everything in 
a directory titled as the current date, zips the directory, and deletes the original.

This script requires that `praw` be installed within the Python environment
you are running this script in.

This script requires that `picture_time.py`, `video_delivery.py`, `text_to_speech.py`
be installed within the same directory.

This file can also be imported as a module and contains the following
functions:

    * login - Creates a praw.Reddit object
    * get_hot - Gets the top posts from r/AskReddit
    * get_comments - Gets all of comments from a specific reddit post but only returns the amount specified
    * make_directories - Creates all the directories that the script will need to function correctly
    * loading - Print a loading screen within the command line
    * picture_and_tts - Combines scripts that take a screencap of a comment along with saving a text to speech audio file
"""


import praw
from text_to_speech import tts
from picture_time import screenshot_comment, screenshot_title
from video_delivery import zip_and_del
import os
import datetime


def login() -> praw.Reddit:
    """Creates a praw.Reddit object

    Args:
        None

    Returns:
        reddit (praw.Reddit): A praw.Reddit object with your specified reddit app
    """
    reddit = praw.Reddit(client_id=os.environ['rv_pus'], \
                        client_secret=os.environ['rv_sec'], \
                        user_agent=os.environ['rv_ua'], \
                        username=os.environ['rv_un'], \
                        password=os.environ['rv_pw'])

    return reddit


def get_hot(reddit: praw.Reddit, submissions_amount: int) -> list:
    """Gets the top posts from r/AskReddit

    Args:
        reddit (praw.Reddit): The reddit object you're using
        submission_amount (int): How many top posts you want returned
    
    Returns:
        ids (list): A list of reddit post ids
    """
    subreddit = reddit.subreddit('AskReddit')
    hottest = subreddit.hot(limit=submissions_amount)
    ids = []

    for submission in hottest:
        ids.append(submission.id)

    return ids


def get_comments(directory: str, reddit: praw.Reddit, submission_id: str, comments_amount: int) -> list:
    """Gets all of the comments from a specific reddit post but only returns the amount specified

    Args:
        directory (str): The directory you would like to save the comments to
        reddit (praw.Reddit): The reddit object you're using
        submission_id (str): The id of the reddit post you want to grab the comments from
        comments_amount (int): The amount of comments you want returned

    Returns:
        list: The comments list but only up to the amount you've specified
    """
    submission = reddit.submission(id=submission_id)
    print(submission.title)

    submission.comment_sort = 'best'
    submission.comments.replace_more()
    comments = []

    comments.append("{} submitted by {}|||{}".format(submission.title, submission.author, submission.url))
    for index, top_comment in enumerate(submission.comments):
        formatted = "{}|||{}|||https://www.reddit.com{}|||{}".format(str(index + 1), top_comment.body, top_comment.permalink, top_comment.id)
        comments.append(formatted)

    return comments[:comments_amount]


def make_directories(date: str, number: int) -> str:
    """Creates all the directories that the script will need to function correctly

    Args:
        date (str): The current date in string form
        number (int): A specified number within the loop

    Returns:
        directory_name (str): The directory name that has been created
    """
    directory_name = "{}/submission{}".format(date, number)
    os.mkdir(directory_name)
    os.mkdir("{}/sounds".format(directory_name))
    os.mkdir("{}/pictures".format(directory_name))
    os.mkdir("{}/movies".format(directory_name))

    return directory_name


def loading(number: int, total: int):
    """Print a loading screen within the command line

    Args:
        number (int): A number specified within the loop
        total (int): The total amount of loops

    Returns:
        None
    """
    print("Comment {}/{} completed.".format(str(number), str(total)), end="\r")


def picture_and_tts(total_submissions: int, total_comments: int, hottest: list) -> str:
    """Combines scripts that take a screencap of a comment along with saving a text to speech audio file

    Args:
        total_submissions (int): The total amount of submissions you'd like
        total_comments (int): The total amount of comments you'd like
        hottest (list): list of ids of the hottest posts on subreddit

    Returns:
        date_dir (str): The string of a directory that was made
    """
    date_dir = datetime.datetime.now().strftime("%m.%d.%Y")
    os.mkdir(date_dir)

    hottest_iteration = 0
    for submission_id in hottest:

        iteration = 0
        directory_name = make_directories(date_dir, str(hottest_iteration))
        all_comments = get_comments(directory_name,reddit_obj, submission_id, total_comments)
        for comment in all_comments:
            if iteration == 0:
                post_title, post_link = comment.split("|||")
                title, author = post_title.split(" submitted by ")

                tts(post_title, directory_name, ".title")
                screenshot_title(post_link, directory_name, ".title", None)

                file = open("{}/.description.txt".format(directory_name), "w")
                file.write(post_title + "\n" + post_link)
                file.close()

                # youtube description
                file = open("{}/.ytdescription.txt".format(directory_name), "w")
                file.write("{}\n\nPosted by u/{}".format(title, author))
                file.close()
            else:
                comment_number, comment_text, comment_link, comment_id = comment.split("|||")
                comment_name = "comment{}".format(str(iteration))

                f = open("{}/.comments.txt".format(directory_name), "a")
                f.write("{}|||{}\n".format(comment_number, comment_link))
                f.close()

                tts(comment_text, directory_name, comment_name)
                screenshot_comment(comment_link, directory_name, comment_name, "t1_" + comment_id)

            loading(iteration, total_comments)
            iteration += 1
        
        print("Submission {} has been completed successfully".format(str(hottest_iteration)))
        print()
        hottest_iteration += 1
    zip_and_del(date_dir)

    return date_dir


if __name__ == '__main__':
    total_submissions = 4
    total_comments = 80
    reddit_obj = login()

    hottest = get_hot(reddit_obj, total_submissions)
    zipped_file = picture_and_tts(total_submissions, total_comments, hottest)
