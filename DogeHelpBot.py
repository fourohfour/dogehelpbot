import praw
import urllib.error
import time

pagemap = {}

def getFromAlias(phrase):
    for key in pagemap.keys():
        for alias in pagemap[key]:
            if alias.lower() == phrase.lower():
                return key

    return "FALSE"
    
def getIntro():
    comment = []
    try:
        with open("./pages/intro.md") as f:
            comment.append(f.read() + "  \n")
    except IOError:
        print("ERROR: NO intro.md FOUND")
    comment.append("  \n")
    for item in pagemap.keys():
        comment.append("* " + item + "\n")
    comment.append("\n")
    return comment
    
def getInfo(phrase):
    comment = []
    if phrase.lower() == "index":
        comment = getIntro()
    elif phrase.lower() == "dictionary":
        comment.append("**Dictionary of Dogecoin**  \n")
        with open("./pages/dictionary.md") as info:
            comment.append(info.read() + "  \n")
    elif phrase.lower() == "subreddits":
        comment.append("**Dogecoin Related Subreddits**  \n")
        with open("./pages/dogesubs.md") as info:
            comment.append(info.read() + "  \n")
    else:
        try:
            with open("./pages/" + getFromAlias(phrase).lower() + ".md") as info:
                comment.append("**Information about " + phrase + "**  \n")
                comment.append("  \n") 
                comment.append(info.read() + "  \n")
        except:
                comment.append("**Could not find " + phrase + " - Listing all pages**  \n")
                comment.append("**Try looking in the dictionary with the command** dogehelpbot dictionary**.**  \n")
                comment = comment + getIntro()

    comment.append("  \n")       
    comment.append("*Information from DogeHelpBot. Want to contribute or get more info? Go to /r/DogeHelpBot*")
    return comment

def readCommand(comment, nxt, w, r):
    if not nxt == 0:
        print("Found Applicable Comment: " + comment.id)
        print("Body: " + str(w[nxt - 1 :nxt + 2]))
        print("Author: " + comment.author.name)
        try:
            command = w[nxt]
        except IndexError:
            return

        redir = False
        if command.lower() == "@op" or command.lower() == "op":
            redir = True
            nxt = nxt + 1
            try:
                command = w[nxt]
            except IndexError:
                print("Redir OP: No Command Found")

        reply = ""
        try:
            if command.lower() == "explain" or command.lower() == "help":
                print("Matches Command: Explain / Help")
                topic = w[nxt + 1]
                
                for line in getInfo(topic):
                    reply = reply + line
                    
            elif command.lower() == "introduction" or command.lower() == "index":
                print("Matches Command: Intro/Index")
                
                for line in getInfo("Index"):
                    reply = reply + line
                
            elif command.lower() == "dictionary":
                print("Matches Command: Dictionary")
                
                for line in getInfo("Dictionary"):
                    reply = reply + line

            elif command.lower() == "subreddits":
                print("Matches Command: Subreddits")
                
                for line in getInfo("Subreddits"):
                    reply = reply + line
            
        except IndexError:
            for line in getInfo("Index"):
                reply = reply + line
        
        if reply == "":
            for line in getInfo("Index"):
                reply = reply + line
            
        if not redir:
            comment.reply(reply)
        else:
            reply = reply +"  \n**/u/" +  comment.author.name + " directed this information at you.**"
            op = ""
            if comment.is_root:
                opsub = comment.submission
                op = opsub.author.name
                newcomment = opsub.add_comment(reply)
            else:
                opcomment = r.get_info(thing_id=comment.parent_id)
                op = opcomment.author.name
                newcomment = opcomment.reply(reply)

            if op == None:
                op = "[deleted]"
            
            comment.reply("Directed information at /u/" + op + ". See the comment [here](" + newcomment.permalink + ").")

def parse(comment, r):
    w = comment.body.split()
    match = ["dogehelpbot", "helpbot", "/u/dogehelpbot", "+/u/dogehelpbot"]
    count = 0
    nxt = 0
    for word in w:
        if word.lower() in match:
            nxt = count + 1
            readCommand(comment, nxt, w, r)
        count += 1
        
    
    
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

        print("READING INDEX...")
        curval = ""
        aliases = []
        with open("./index.txt") as f:
            for line in f:
                if line[0] == "-":
                    aliases.append(line[1:].strip())
                    print("ADDING ALIAS " + line[1:].strip().lower() + " TO " + curval)
                else:
                    if not curval == "":
                        pagemap[curval] = aliases
                    curval = line.strip()
                    aliases = [curval.strip()]
                    print("PAGE: " + line.strip())

            if not curval == "":
                pagemap[curval] = aliases
            
        r.login(user, passwrd)

        while True:
            sreddits = r.get_subreddit(subreddits)
            comments = sreddits.get_comments()
            for c in comments:
                if c.id not in done:
                    if not c.author.name == "DogeHelpBot":
                        parse(c, r)
                    done.insert(0, c.id)

            with open("./dealtwith.txt", "w") as f:
                count = 0
                for item in done:
                    if count == 50:
                        break
                    f.write(item + "\n")
                    count = count + 1
                    
            time.sleep(8)
    except urllib.error.HTTPError as e:
        print("HTTPError Code: " + str(e.code) + " - retrying in [60] seconds.")
        time.sleep(60)
        main()

if __name__ == "__main__":
    main()
