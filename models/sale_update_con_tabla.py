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
import time
from odoo import api, fields, models
#libreria para enviar correos electronicos
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#libreria para generar archivos PDF
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter, cm
from reportlab.pdfgen import canvas

#libreria para adjuntar archivos
from email.mime.base import MIMEBase
from email import encoders

#libreria para manejar archivos
import os

from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO

class egas_correo_ventas(models.Model):
    _name='egas.correo.ventas'
    _description='Guarda el correo al que se guardara cuando se confirme un pedido de ventas'

    name= fields.Char('Nombre', size=100, required=True)
    correo_electronico= fields.Char('Correo electronico', size=100, required=True)

egas_correo_ventas()


class SaleOrderUpdate(models.Model):
    _inherit='sale.order'

    def genera_pdf(self):

        #ruta actual del archivo que se esta ejecutando
        ruta = (os.path.dirname(os.path.abspath(__file__)))
        nueva_ruta = ruta[0:len(ruta) - 6]

        fecha=time.strftime("%d/%m/%Y")

        filtro = [('order_id', '=', self.id)]
        campos = ['name', 'product_uom_qty', 'price_unit', 'price_subtotal', 'price_tax']
        consulta = self.env['sale.order.line'].search_read(filtro, campos)

        cliente_obj=self.env['res.partner'].browse(int(self.partner_id))

        #valida si la carpeta existe en la ruta y si no la crea con os.mkdir()
        valida=os.path.exists(nueva_ruta+'archivos')
        if valida==False:
            os.mkdir(nueva_ruta+'archivos')

        # se define donde y como se llamara el archivo a crear y su tamaño de hoja
        archivo=canvas.Canvas(nueva_ruta +'archivos/'+self.name+'.pdf', pagesize=letter)
        archivo.setLineWidth(.3)    #tamaño de linea
        archivo.setFont('Helvetica', 12)    #formato y tamaño de letra

        #se agregan los logos
        archivo.drawImage(nueva_ruta+'logo/odoo11.png', 30, 750, width=80, height=35)
        archivo.drawImage(nueva_ruta+'logo/smartqs.png', 490, 680, width=85, height=50)

        #se agregan los datos
        archivo.drawString(500, 750, fecha)
        archivo.line(30, 748, 580, 748)

        archivo.drawString(30, 703, 'Pedido # ')
        archivo.drawString(90, 703, self.name)

        archivo.drawString(30, 688, 'Cliente ')
        archivo.drawString(90, 688, cliente_obj.name)

        styles=getSampleStyleSheet()

        #Estilos de los titulos de la tabla
        titulo_tabla=styles['Normal']
        titulo_tabla.fontSize=12
        titulo_tabla.aligment= TA_CENTER
        titulo_tabla.fontName = 'Helvetica'

        descripcion=Paragraph('<b>Descripcion</b>',titulo_tabla)
        cantidad=Paragraph('<b>Cantidad</b>',titulo_tabla)
        precio=Paragraph('<b>Precio</b>',titulo_tabla)
        impuestos=Paragraph('<b>Impuestos</b>',titulo_tabla)
        importe=Paragraph('<b>Importe</b>',titulo_tabla)

        data=[]
        data.append([descripcion,
                     cantidad,
                     precio,
                     impuestos,
                     importe
                     ])

        # Estilos del cuerpo de la tabla
        cuerpo_tabla=styles['BodyText']
        cuerpo_tabla.fontSize=10

        high=600
        for con in consulta:
            lista_dato=[con['name'],con['product_uom_qty'],con['price_unit'],con['price_tax'],con['price_subtotal']]
            data.append(lista_dato)
            high=high-10

        width, height=letter
        tabla=Table(data, colWidths=[9.5 * cm, 2.4 * cm, 1.9 * cm, 2.6 * cm, 2.2 * cm])
        tabla.setStyle(TableStyle([
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ]))

        aux=len(consulta)*10
        high=high-aux

        # Establecemos el tamaño de la hoja que ocupará la tabla
        tabla.wrapOn(archivo, width, high)

        # Definimos la coordenada donde se dibujará la tabla
        tabla.drawOn(archivo, width, height)
        archivo.showPage()

        archivo.save()
        return nueva_ruta #devuelve la ruta para buscar el pdf y adjuntarlo al correo

    def _action_confirm(self): # self tiene los datos del objeto actual
        #ejemplos de como acceder a la inf.:
        #self.name, self.amount_total

        #ruta para encontrar el pdf
        nueva_ruta=self.genera_pdf()

        #obtiene una lista con todos los correos
        correos=[]
        lista_correo=self.env['egas.correo.ventas'].search([])
        for lista in lista_correo:
            correos.append(lista.correo_electronico)

        #credenciales del correo que se usara para generar el correo
        user='crmegas@smartqs.com'
        passw='egascrm1'

        #parametros del correo
        remitente=user
        destinatario=correos
        asunto="EGASMART SA DE CV SO (Ref %s)" % self.name
        mensaje="""Estimado(a) Alejandro <br/> <br/>
                Aqui encontrará la confirmación de orden <b>{}</b> por un monto de <b>{} MXN</b> de EGASMART SA DE CV. <br/> <br/>
                Saludos""".format(self.name, self.amount_total)

        #host y puerto
        gmail= smtplib.SMTP('smtp.gmail.com: 587')

        #protocolo utilizado por gmail
        gmail.starttls()

        #credenciales
        gmail.login(user, passw)

        # se crea la instancia del objeto del mensaje
        header= MIMEMultipart()

        # formato o tipo del mensaje, en este caso es HTML
        mensaje = MIMEText(mensaje, 'html')  # Content-type:text/html
        header.attach(mensaje)

        #se agrega el archivo que se adjuntara
        archivo=MIMEBase('appication', 'octet-stream')
        archivo.set_payload(open(nueva_ruta+'archivos/'+self.name+'.pdf').read())#se abre y se lee el archivo
        encoders.encode_base64(archivo) #archivo se codifica en base 64 para poder enviarlo
        archivo.add_header('Content-Disposition', 'attachment; filename="%s"' % self.name +'.pdf')#nombre que se le dara al archivo
        header.attach(archivo)#se agrega el archivo al correo

        # se crea la cabecera del correo
        header['Subject']=asunto
        header['From']=remitente

        #envia multiples correos
        for dest in destinatario:

            #Enviar email
            gmail.sendmail(header['From'], dest, header.as_string())

        #Cerrar la conexion SMTP
        gmail.quit()

        return super(SaleOrderUpdate, self)._action_confirm()



SaleOrderUpdate()