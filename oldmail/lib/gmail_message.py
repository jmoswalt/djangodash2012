class gmail_message:

    def __init__(self):
        self.id = None
        self.uid = None
        self.flags = None
        self.mailbox = None
        self.date = None

        self.From = None
        self.To = None
        self.Subject = '( no subject )'
        self.Body = None

    def __repr__(self):
        str = "<gmail_message:  ID: %s  UID: %s Flags: %s Date: %s \n" % (self.id, self.uid, self.flags, self.date)
        str += "from: %s to: %s subject: %s >" % (self.From, self.To, self.Subject)
        return str
