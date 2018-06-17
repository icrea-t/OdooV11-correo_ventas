# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2013 Egas - www.egas.com.mx
#    All Rights Reserved.
###############Credits######################################################
#    Coded by: Edgar Gustavo gustavo.hernandez@smartqs.com
#    Planified by: Edgar Gustavo
#    Finance by: Egas.
#    Audited by: Edgar Gustavo
############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models
#libreria para enviar correos electronicos
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class egas_correo_ventas(models.Model):
    _name='egas.correo.ventas'
    _description='Guarda el correo al que se guardara cuando se confirme un pedido de ventas'

    name= fields.Char('Nombre', size=100, required=True)
    correo_electronico= fields.Char('Correo electronico', size=100, required=True)

egas_correo_ventas()


class SaleOrderUpdate(models.Model):
    _inherit='sale.order'

    def _action_confirm(self):
        print('Esto sera para el correo.....')

        # # create message object instance
        # msg = MIMEMultipart()
        #
        # message = "Thank you"
        #
        # # setup the parameters of the message
        # password = "Vicky186"
        # msg['From'] = "gustavo.hernandez@smartqs.com"
        # msg['To'] = "gustavo.hernandez@smartqs.com"
        # msg['Subject'] = "Subject,SOY EL ASUNTO"
        #
        # # add in the message body
        # msg.attach(MIMEText(message, 'plain'))
        #
        # # create server
        # server = smtplib.SMTP('smtp.gmail.com: 587')
        #
        # server.starttls()
        #
        # # Login Credentials for sending the mail
        # server.login(msg['From'], password)
        #
        # # send the message via the server.
        # server.sendmail(msg['From'], msg['To'], msg.as_string())
        #
        # server.quit()


        user='gustavo.hernandez@smartqs.com'
        passw='Vicky186'

        remitente="gustavo.hernandez@smartqs.com"
        destinatario="gustavo.hernandez@smartqs.com"
        asunto="SOY EL ASUNTO"
        mensaje="SOY EL MENSAJE Y YO SOY <b>NEGRITAS</b>"

        #host y puerto
        gmail= smtplib.SMTP('smtp.gmail.com: 587')

        #protocolo utilizado por gmail
        gmail.starttls()

        #credenciales
        gmail.login(user, passw)

        #depuracion, se le envia de parametro true que es 1
        gmail.set_debuglevel(1)

        header= MIMEMultipart()
        header['Subject']=asunto
        header['From']=remitente
        header['To']=destinatario

        mensaje= MIMEText(mensaje, 'plain') #Content-type:text/html
        header.attach(mensaje)

        #Enviar email
        #gmail.sendmail(remitente, destinatario, header.as_string())
        gmail.sendmail(remitente, destinatario, mensaje)

        #Cerrar la conexion SMTP
        gmail.quit()

        print('DEBERIA DE HABER ENVIADO EL CORREO')

        return super(SaleOrderUpdate, self)._action_confirm()

SaleOrderUpdate()