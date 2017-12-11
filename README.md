# 620_job_forum

Readme 

Group project: Job Forum Service

instructor: Ryan Shaw   
Group members: Yuhe Ding, Tian Wang, Chudi Zhong


(1) Description: Our project is about job forum service. In this project, you can post a message to the forum and reply other messgae as well. Only Administer can delete the messgae and replies in the forum. We have realized all the function in message part. Because of time, similar work on reply delete will be finished later.

(2) Project: our project include two html files, a server.py and a data.json

(3) Class and Rel:
a file documenting the class and rel attribute values we used to describe our job forum service in the deliverable 2. 

Resources: Discussion, DiscussionAsJson, Message, MessageAsJson, Reply 

class = "name" indicates the name of individual message
class = "delete" indicates the message deletion in the discussion 
class = "new-message" indicates the new message section in the discussion.
class = "add-message" indicates the editing area when adding a new message
class = "new-reply" indicates a new reply section for this message
class = "add-reply" indicates the editing area when adding a new reply

rel="item" indicates that it is one of the item in the discussion

(4) Microdata:   
Microdata of message.html

itemtype="http://schema.org/CreativeWork" indicates that the type of message is CreativeWork
itemprop = "headline" indicates the title of a message 
itemprop = "text" indicates the content of a message
itemprop = "author" itemtype = "http://schema.org/Person" 
	itemprop = "name" indicates the author of a message
itemprop = "dateCreated" indicates the time a message is created
itemprop = "comment" itemtype = "http://schema.org/Comment"
	itemprop = "name" indicates the title of a reply
	itemprop = "text" indicates the content of a reply
	itemprop = "author" itemtype = "http://schema.org/Person"
	itemprop = "name" indicates the author of a reply
	itemprop = "dateCreated" indicates the time a reply is created


Microdata of discussion.html

This html will list all message, which are CreativeWork in the project.
itemtype = "http://schema.org/CreativeWork" indicates that the type of message is CreativeWork
itemprop = "headline" indicates the title of a message
itemprop = "dateCreated" indicates the time a message is created 
