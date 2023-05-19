import codecs
import tweepy
import os
import time

# Twitter API Credentials
consumer_key = "O8CoG2IufDW2NnuOivX3Dljt1"
consumer_secret = "rEk321iMtW9aP4COOe44LS40zPq2dTGCuPlaPLHxQj8dPDQ6Iu"
access_key = "828441325594873856-3p6sjej2155OkzHvsu7isuGhQg2Z6YM"
access_secret = "G66LNp1YrDEU57cwUs3uOBvvOL567ecM95zKGXtnN4yiI"
userID = "44196397"

# Crawling Function
def get_profile_info(userID):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit_notify=True)
    getuser = api.get_user(userID)
    user_id = getuser.id
    screen_name = getuser.screen_name
    global nodeIndex
    global friend
    friendList = []
    while True:
        try:
            friendList = api.friends_ids(friend[nodeIndex - 1])
            print("The user id is: ", user_id)
        except tweepy.TweepError as e:
            print("e:", e)
            data = codecs.open('Errorlog.txt', 'w+', 'utf-8')
            data.write("error: %s \n" % e)
            if e.args[0][0]['code'] == 88:
                print("rate time error: ", userID)
                data.write("rate limit, user id: %s " % user_id)
                data.close()
                time.sleep(60 * 16)
                continue
            elif e.args[0][0]['code'] == 63:
                print("Branch: Not authorized ")
                data.write("not authorized, id : %s \n" % user_id)
                data.close()
                nodeIndex = nodeIndex + 1
                break
            else:
                print("other fault, error: ", e)
                print("Error Fetch nodeIndex, UserID", nodeIndex, userID)
                data.write("other fault,nodeIndex: %d" % nodeIndex)
                data.close()
                nodeIndex = nodeIndex + 1
                break

    data = codecs.open(str(user_id) + '.txt', 'w+', 'utf-8')

    for item in friendList:
        data.write("%d \n" % item)
    data.close()

# Create Friend
friend = []
friend_size = 0
dat = codecs.open('seqNodes.txt', 'r', 'utf-8')
line = dat.readline()
while line:
    if friend_size > 2510:
        break
    line = line.strip()
    friend.append(line)
    friend_size = friend_size + 1
    line = dat.readline()
print("friend Array Finished Creation")
data = codecs.open('friend.txt', 'w+', 'utf-8')
data.write("%s \n " % friend)
data.close()
dat.close()
# Start crawling

nodeIndex = 1365
while nodeIndex < 2500:
    get_profile_info(friend[nodeIndex - 1])
    nodeIndex = nodeIndex + 1

print("nodeIndex: ", nodeIndex)
print("friend(nodeIndex-1): ", friend[nodeIndex - 1])
print("BFS Length is:", len(friend))
data = codecs.open('result.txt', 'w+', 'utf-8')
data.write("nodeIndex:%d \n " % nodeIndex)
data.write("friend(nodeIndex-1): %s \n" % friend[nodeIndex - 1])
data.write("BFS length: %d \n" % len(friend))
data.close()