import imaplib
import email
import os
import schedule
import time

# The user name and passwd
#app key = 'hnwy uofq umvy vssd' beacaus gmail safe
#its my example email that is set up and can work will get random photos
user = "violetaaveniite@gmail.com"
password = "hnwy uofq umvy vssd"

# URL for IMAP connection
imap_url = 'imap.gmail.com'

# Connection with GMAIL using SSL
my_mail = imaplib.IMAP4_SSL(imap_url)

# Log in using your credentials
my_mail.login(user, password)

# Select the Inbox to fetch messages
my_mail.select('Inbox')

# Search for emails with atribute unseen, its assigned to emails that have not been read
_, data = my_mail.search(None, 'UNSEEN') 

# IDs of all emails that we want to fetch 
mail_id_list = data[0].split() 

# Where i want to save the images
path = "/Users/chupakabra/Pictures/Gramatvedība"

#We will use it multible times so we need it to be a method
def GmailExtraction():
    #Iterate through messages and extract data into folder
    for num in mail_id_list:
        #RFC822 returns whole message
        typ, data = my_mail.fetch(num, '(RFC822)') 
        #Gmail emails have 2 dimensions, we want the one with content
        raw_email = data[0][1] 
        #Creating a object that can be used to access the body, also can see sender, recipient, subject if needed
        email_message = email.message_from_bytes(raw_email) 
        
        #Ittarate trough all parts of the email, in my case resching for image
        for part in email_message.walk():
            #Ff its a image we want it, even its its incorrect it will be filtered down the line
            if part.get_content_type() == 'image/jpeg':
                #Geting the name of the image
                filename = part.get_filename()
                #If it does not have one we give it one
                if not filename:
                    filename = 'image.jpg'
                #Connects a active directory and the filename, returns a string, that is a path to the file
                filepath = os.path.join(os.getcwd(), filename)
                #Writing the content of the email attachment to a file, in binary write mode, i used this to see it imediately
                open(filepath, 'wb').write(part.get_payload(decode=True))
                #We rename the file to the path were we want it and adding its name
                os.rename(filename, os.path.join(path, filename))

#The times when the program runs, adjustable to preferences
schedule.every().day.at("04:00").do(GmailExtraction)
schedule.every().day.at("10:00").do(GmailExtraction)
schedule.every().day.at("18:00").do(GmailExtraction)

#Executng the methods untill manually stopped
while True:
    schedule.run_pending()
    time.sleep(10000)

