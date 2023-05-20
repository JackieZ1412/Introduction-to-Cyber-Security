import tweepy # https://github.com/tweepy/tweepy
import struct
import codecs
import time
import clique_find
import json

# Twitter API Credentials
consumer_key = "O8CoG2IufDW2NnuOivX3Dljt1"
consumer_secret = "rEk321iMtW9aP4COOe44LS40zPq2dTGCuPlaPLHxQj8dPDQ6Iu"
access_key = "828441325594873856-3p6sjej2155OkzHvsu7isuGhQg2Z6YM"
access_secret = "G66LNp1YrDEU57cwUs3uOBvvOL567ecM95zKGXtnN4yiI"
userID = "44196397"

def get_profile_info(userID):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit_notify=True)
    getuser = api.get_user(userID)
    user_id = getuser.id
    # user_name = str(getuser.name).encode('utf-8')
    screen_name = getuser.screen_name
    global nodeIndex
    global friend
    while True:
        try:
            friendList = api.friends_ids(userID)
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

            else:
                print("other fault, error: ", e)
                print("Error Fetch nodeIndex, UserID", nodeIndex, userID)
                data.write("other fault,nodeIndex: %d" % nodeIndex)
                data.close()
                nodeIndex = nodeIndex + 1
                friendList = api.friends_ids(friend[nodeIndex - 1])
                break
        break

    friend = friend + friendList
    data = codecs.open(str(user_id) + '.txt', 'w+', 'utf-8')

    for item in friendList:
        # nameid=api.get_user(item)
        # name=unicode(nameid.name)
        data.write("%d \n" % item)
        # data.write("%s \n" % name)
        data.close()

    # print("The user name is: ", user_name)
    # print("The screenname is: ", screen_name)
    # print("The userID is: ", user_id)
    # print("The user's friend list is: ", friendList)

friend = []
get_profile_info(userID)
nodeIndex = 1

while nodeIndex < 2001:
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