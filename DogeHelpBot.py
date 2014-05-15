import praw
import time

def getInfo(phrase):
    comment = []
    if phrase.lower() == "index":
        with open("./index.txt") as info:
            comment.append(info.read() + "  \n")
    elif phrase.lower() == "dictionary":
        comment.append("**Dictionary of Dogecoin**  \n")
        with open("./index.txt") as info:
            comment.append(info.read() + "  \n")
    else:
        try:
            with open("./pages/" + phrase.lower() + ".txt") as info:
                comment.append("**Information about " + phrase + "**  \n")
                comment.append(info.read() + "  \n")
        except IOError:
            try:
                with open("./index.txt") as info:
                    comment.append("**Could not find " + phrase + " - Listing all pages**  \n")
                    comment.append(info.read() + "  \n")
            except IOError:
                print("ERROR: NO index.txt FOUND")
    comment.append("\n  ")       
    comment.append("*Information from DogeHelpBot. More info at /r/DogeHelpBot*")
    return comment
    
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
            print("Matches Command: Explain")
            
            try:
                topic = w[nxt + 1]
            except IndexError:
                topic = "Index"
                
            reply = ""
            
            for line in getInfo(topic):
                reply = reply + line
                
            comment.reply(reply)
        elif command.lower() == "introduction" or command.lower() == "index":
            print("Matches Command: Intro/Index")
            reply = ""
            
            for line in getInfo("Index"):
                reply = reply + line
                
            comment.reply(reply)
            
        elif command.lower() == "dictionary":
            print("Matches Command: Dictionary")
            reply = ""
            
            for line in getInfo("Dictionary"):
                reply = reply + line
                
            comment.reply(reply)
    
def main():
    try:
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
                    print("Parsing " + c.id)
                    if not c.author.name == "DogeHelpBot":
                        parse(c)
                    done.insert(0, c.id)

            with open("./dealtwith.txt", "w") as f:
                count = 0
                for item in done:
                    if count == 50:
                        break
                    f.write(item + "\n")
                    count = count + 1
                    
            time.sleep(8)
    except:
        main()
main()
