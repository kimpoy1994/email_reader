from email import policy
from email.parser import BytesParser

class EmailReader:
    """Creates an object for email parsing"""

    def __init__(self):
        self.emailPath = ""
        self.subjectField = ""
        self.fromField = ""
        self.toField = ""
        self.htmlBody = ""
        self.textBody = ""
        self.replyTo = ""
        self.returnPath = ""
    
    def readEmail(self,emailPath):
        """Reads an email for parsing"""
        f = open(emailPath,"rb")
        self.msg = BytesParser(policy=policy.default).parse(f)
        f.close()

    def getFrom(self,mode="address"):
        """Gets the from field.
        :param mode: what type of way in getting the from field
        address -> Returns only the address
        name -> Returns only the name
        full -> Returns both the name and address
        """
        fromField = self.msg["From"]
        if mode=="full":
            return fromField
        elif mode=="address":
            if "<" in fromField:
                temp = fromField.split("<")[-1][:-1]
                return temp
            else:
                return ""
                
        elif mode=="name":
            if "<" in fromField:
                temp = fromField.split("<")[0]
                return temp.strip()
            else:
                return ""
        else:
            raise Exception("Parameter is undefined!\nAvailable options are only: \"address\", \"name\", and \"full\"")

    def getSubject(self):
        """Gets the subject field"""
        return self.msg["Subject"]

    def getReplyTo(self):
        """Gets the Reply-To field"""
        return self.msg["Reply-To"]
    
    def getReturnPath(self):
        """Gets the Return-Path field"""
        return self.msg["Return-Path"]

    def getHeader(self,header=""):
        """Gets any header"""
        if header=="":
            return ""
        else:
            try:
                return self.msg[header]
            except:
                return ""
        
    def getBody(self,mode="all"):
        """Gets the body.
        :param mode: what type of way in getting the email's body.
        all -> Returns both html and text
        html -> Returns only the html
        text -> Returns only the text
        """
        htmlBody = ""
        textBody = ""
        if self.msg.is_multipart():
            # Iterate for each part and check if it's the "body" part, text or html
            for part in self.msg.walk():
            # Check if its HTML and it is not an attachment
                if part.get_content_type() == "text/html" and part.get_content_disposition() != "attachment":
                    # Store the part in "s" variable in standard latin-1 encoding
                    self.htmlBody = part.get_payload(decode=True).decode('ISO-8859-1')
                    htmlBody = self.htmlBody
                    # Since this is in HTML format, we need to strip all the HTML tags, we use BeautifulSoup
                    # For plain text and not an attachment
                if part.get_content_type() == "text/plain" and part.get_content_disposition() != "attachment":
                    # Place the text part to "s" variable in standard latin-1 encoding
                    self.textBody = part.get_payload(decode=True).decode('ISO-8859-1')
                    textBody = self.textBody
        
        if mode == "all":
            return htmlBody,textBody
        elif mode == "html":
            return htmlBody
        elif mode == "text":
            return textBody



