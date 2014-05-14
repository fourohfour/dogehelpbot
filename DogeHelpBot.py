import praw
import time

def parse(comment):
    w = comment.body.split()
    match = ["dogehelpbot", "helpbot"]
    count = 0
    nxt = 0
    for word in w:
        if word.lower() in match:
            nxt = count + 1
            break
        count += 1
        
    if not nxt == 0:
        try:
            command = w[nxt]
        except IndexError:
            pass

        if command.lower() == "explain":
            comment.reply("Test 4")
            
    
def main():
    r = praw.Reddit(user_agent = "DogeHelpBot - Provides information about Dogecoin on request")

    done = []
        
    user = ""
    passwrd = ""
    subreddits = ""


    with open("./dealtwith.txt") as f:
        for line in f:
            done.append(line.strip())

    with open("./credentials.txt") as f:
        search = 0
        for line in f:
            if search == 0:
                user = line.strip()
                search = 1
            else:
                passwrd = line.strip()
                break

    with open("./subreddits.txt") as f:
        for line in f:
            subreddits = subreddits + "+" + line.strip()

    r.login(user, passwrd)

    while True:
        sreddits = r.get_subreddit(subreddits)
        comments = sreddits.get_comments()
        for c in comments:
            if c.id not in done:
                parse(c)
                done.insert(0, c.id)

        with open("./dealtwith.txt", "w") as f:
            count = 0
            for item in done:
                if count == 25:
                    break
                f.write(item + "\n")
                count = count + 1
                
        time.sleep(8)

main()
