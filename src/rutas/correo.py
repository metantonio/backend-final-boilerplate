import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')

@app.route('/correo', methods=["POST"])
def enviarCorreo():
    smtp_address = 'smtp.gmail.com'
    smtp_port = 465 #SSL

    print(EMAIL)
    body = request.get_json()
    mensaje = body["mensaje"]
    destinatario = body["para"]
    asunto = body["asunto"]

    print(mensaje, destinatario, asunto)
    message = MIMEMultipart('alternative') #json, #text #application/pdf
    message["Subject"] = asunto
    message["From"] = EMAIL
    message["To"] = destinatario

    html = ''' 
    <html>
    <body>
    <h1>Estimado Usuario:''' + destinatario+ '''   </h1>

    </body>
    </html>

    '''
    asunto_text = "hola"
    #creando elemento MIMEText
    text_mime = MIMEText(asunto_text, 'plain')
    html_mime = MIMEText(html, 'html')

    #adjunta los MIMEText al MIMEMultipart
    message.attach(text_mime)
    message.attach(html_mime)

    email_address = EMAIL
    email_password = PASSWORD
    #Conectamos al puerto 465 de gmail para enviar el correo
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
        server.login(email_address, email_password)
        server.sendmail(email_address, destinatario, message.as_string())



    return jsonify('"ok: correo Enviado"'), 200