from django.conf import settings
#import imaplib as imaplib_base
import gmail_mailboxes, gmail_messages, gmail_message
import oauth2 as oauth
import oauth2.clients.imap as imaplib

BASE_URL = "https://mail.google.com/mail/b/%s/imap/"

class gmail_imap:

    def __init__ (self, email, oauth_token, oauth_token_secret):
        self.url = BASE_URL % email
        self.token = oauth.Token(oauth_token, oauth_token_secret)
        self.consumer = oauth.Consumer(settings.OAUTH2_CONSUMER_KEY,
                                       settings.OAUTH2_CONSUMER_SECRET
                                       )
        self.imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
        self.loggedIn = False
        
        self.mailboxes = gmail_mailboxes.gmail_mailboxes(self)
        self.messages = gmail_messages.gmail_messages(self)
        
    def login (self):
        self.imap_server.authenticate(self.url, self.consumer, self.token)
        self.loggedIn = True
    
    def logout (self):
        self.imap_server.close()
        self.loggedIn = False
        

        
if __name__ == '__main__':
    #import getpass
    gmail = gmail_imap('youremail@gmail.com',
                       'your_oauth_token',
                       'your_oauth_token_secret')
    
    gmail.mailboxes.load()
    print gmail.mailboxes
    
    gmail.messages.process("INBOX")
    print gmail.messages
  
    for msg in gmail.messages[0:2]:
        message = gmail.messages.getMessage(msg.uid)
        print message
        print message.Body
    
    gmail.logout()