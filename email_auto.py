import imaplib
import base64
import os
import email

attachment_dir = 'C:/Users/diwas/OneDrive/Desktop/Attachments'

FROM_EMAIL ='bidoceantest@gmail.com'
FROM_PWD = '@12345abcde'
SMTP_SERVER='imap.gmail.com'
port=993
mail = imaplib.IMAP4_SSL(SMTP_SERVER)
mail.login(FROM_EMAIL,FROM_PWD)
mail.select('inbox')
type, data = mail.search(None, 'ALL')
mail_ids = data[0]

id_list = mail_ids.split() 
print(len(id_list))
first_email_id = int(id_list[0])
latest_email_id = int(id_list[-1])

def get_attachments(msg):
    for part in msg.walk():
        if part.get_content_maintype()=='multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()

        if bool(fileName):
            filePath = os.path.join(attachment_dir, fileName)
            with open(filePath,'wb') as f:
                f.write(part.get_payload(decode=True))

def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None,True)


for i in range(1,len(id_list)):
    typ, data = mail.fetch(mail_ids.split()[i], '(RFC822)' )
    raw_email = data[0][1]
    
    raw_email_string = raw_email.decode('utf-8')
    raw = email.message_from_bytes(data[0][1])
    b = email.message_from_string(raw_email_string)
    from_email = b['from']
    to_email = b['to']
    subject_email=b['subject']

    print('From:'+from_email)
    print('To:'+to_email)
    print('Subject:'+str(subject_email)) 
    print(get_body(raw))
    get_attachments(raw)
        
    
    if b.get_content_maintype() == 'multipart':
        continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            filePath = os.path.join(fileName)
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
            subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
            print('Downloaded "{file}" from email titled "{subject}" with UID {uid}.'.format(file=fileName, subject=subject, uid=latest_email_uid.decode('utf-8')))
