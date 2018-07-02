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

    def _action_confirm(self): # self tiene los datos del objeto actual
        #ejemplos de como acceder a la inf.:
        #self.name, self.amount_total

        print('Esto sera para el correo.....')

        #se busca el detalle del presupuesto y se trae toda la inf.
        #de los objetos (para extraerlos utilizar un 'for')
        filtro = [('order_id', '=', self.id)]
        prueba = self.env['sale.order.line'].search(filtro)
        print(prueba, 'solo con filtro')
        for algo in prueba:
            print(algo.name, algo.id, 'Extrayendo la inf. con el for')

        #se busca el detalle del presupuesto, pero de campos especificos
        #y los devuelve en un diccionario
        super_filtro = ['name', 'price_unit', 'product_uom_qty']
        con_super_filtro = self.env['sale.order.line'].search_read(filtro, super_filtro)
        print(con_super_filtro, 'con super filtros')

        # credenciales del correo que se usara para generar el correo
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

        # se crea la instancia del objeto del mensaje
        header= MIMEMultipart()

        # se crea la cabecera del correo
        header['Subject']=asunto
        header['From']=remitente
        header['To']=destinatario

        # formato o tipo del mensaje, en este caso es HTML
        mensaje= MIMEText(mensaje, 'html') #Content-type:text/html
        header.attach(mensaje)

        #Enviar email
        gmail.sendmail(header['From'], header['To'], header.as_string())

        #Cerrar la conexion SMTP
        gmail.quit()

        print('DEBERIA DE HABER ENVIADO EL CORREO')

        return super(SaleOrderUpdate, self)._action_confirm()

SaleOrderUpdate()