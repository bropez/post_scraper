import praw
from text_to_speech import tts
from picture_time import screenshot_comment, screenshot_title
from video_delivery import zip_and_del
import os
import datetime
# TODO: document this please


def login():
    reddit = praw.Reddit(client_id=os.environ['rv_pus'], \
                        client_secret=os.environ['rv_sec'], \
                        user_agent=os.environ['rv_ua'], \
                        username=os.environ['rv_un'], \
                        password=os.environ['rv_pw'])
    
    return reddit


def get_hot(reddit, submissions_amount):
    subreddit = reddit.subreddit('AskReddit')
    hottest = subreddit.hot(limit=submissions_amount)
    ids = []
    for submission in hottest:
        ids.append(submission.id)
    return ids


def get_comments(directory, reddit, submission_id, comments_amount):
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


def make_directories(date, number):
    directory_name = "{}/submission{}".format(date, number)
    os.mkdir(directory_name)
    os.mkdir("{}/sounds".format(directory_name))
    os.mkdir("{}/pictures".format(directory_name))
    os.mkdir("{}/movies".format(directory_name))

    return directory_name


def loading(number, total):
    print("Comment {}/{} completed.".format(str(number), str(total)), end="\r")


def picture_and_tts(total_submissions, total_comments, hottest):
    
    date_dir = datetime.datetime.now().strftime("%m.%d.%Y_%H.%M")
    os.mkdir(date_dir)

    hottest_iteration = 0
    for submission_id in hottest:

        iteration = 0
        directory_name = make_directories(date_dir, str(hottest_iteration))
        all_comments = get_comments(directory_name,reddit_obj, submission_id, total_comments)
        for comment in all_comments:
            if iteration == 0:
                post_title, post_link= comment.split("|||")

                tts(post_title, directory_name, ".title")
                screenshot_title(post_link, directory_name, ".title", None)

                file = open("{}/.description.txt".format(directory_name), "w")
                file.write(post_title + "\n" + post_link)
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
    total_submissions = 3
    total_comments = 80
    reddit_obj = login()

    hottest = get_hot(reddit_obj, total_submissions)
    zipped_file = picture_and_tts(total_submissions, total_comments, hottest)
    # TODO: send the zipped_file with email
