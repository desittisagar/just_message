# just_message

# models

Users -
userid - char
username - char
contact - char

Groups - 
userid - fk from Users
groupid - char
group name - char

Sessions - 
userid - fk from Users
serverid - char

Lastseen - 
userid - fk from Users
timestamp - datetime

Message - 
msgid - 
source_userid - 
dest_userid - 
media_url - 
timestamp - 
content - 

Unsent message - 
msgid - 
source_userid - fk from Users
dest_userid - fk from Users
media_url -
timestamp - 
content - 