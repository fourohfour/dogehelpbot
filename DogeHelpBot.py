import praw

r = praw.Reddit(user_agent = "DogeHelpBot - Provides information about Dogecoin on request")

done = []
user = ""
passwrd = ""
subreddits = ""


with f as open("./dealtwith.txt"):
    for line in f:
        done.append(line)

with f as open("./credentials.txt"):
    search = 0
    for line in f:
        if search == 0:
            user = line
            search = 1
        else:
            passwrd = line
            break

with f as open("./subreddits.txt"):
    for line in f:
        subreddits = subreddits + "+" + line

r.login(user, passwrd)

while True:
    sreddits = r.get_subreddit(subreddits)
    comments = subreddit.get_comments()
    flatc = praw.helpers.flatten_tree(comments)
    #do stuff - TODO
