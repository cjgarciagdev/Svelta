import smtplib
from email.message import EmailMessage
from config.email_config import EMAIL_SENDER, EMAIL_PASSWORD

def send_recovery_code(to_email, code):
    """
    Envía un correo electrónico con el código de recuperación.
    Retorna True si fue exitoso, False si falló.
    """
    if not EMAIL_SENDER or "ejemplo" in EMAIL_SENDER:
        print("[AVISO] El correo de envío no ha sido configurado en config/email_config.py")
        return False
        
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Código de Recuperación - Censo INCES'
        msg['From'] = EMAIL_SENDER
        msg['To'] = to_email
        
        cuerpo = f"""
        Hola,
        
        Has solicitado recuperar tu contraseña en el sistema Censo INCES.
        
        Tu código de verificación de 6 dígitos es:
        
        {code}
        
        Si no solicitaste esto, puedes ignorar este correo.
        
        Atentamente,
        El equipo del INCES.
        """
        
        msg.set_content(cuerpo)
        
        # Conectar al servidor SMTP de Gmail
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        
        # Eliminar espacios de la contraseña por si los copiaron así
        clean_password = EMAIL_PASSWORD.replace(" ", "")
        
        server.login(EMAIL_SENDER, clean_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error al enviar correo de recuperación: {e}")
        return False
