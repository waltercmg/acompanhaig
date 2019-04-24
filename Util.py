# encoding=utf8  
# coding=UTF-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def enviarEmail(destinatario, titulo, conteudo):
        #print destinatario
        me = "alertai@serpro.gov.br"
        you = destinatario
        msg = MIMEMultipart('alternative')
        msg['Subject'] = titulo
        msg['From'] = me
        msg['To'] = you

        html = "<html><head><meta charset=\"UTF-8\"></head><body>"+\
               conteudo +\
        	   "</p></body></html>"


        text = ""        
        part1 = MIMEText(text, 'plain', 'utf-8')
        part2 = MIMEText(html, 'html',  'utf-8')

        msg.attach(part1)
        msg.attach(part2)

        s = smtplib.SMTP('localhost')

        s.sendmail(me, you, msg.as_string())  



