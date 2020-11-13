'''
Created on Aug 27, 2017

@author: Mutwkil Faisal
'''
from odoo import models, fields, api, _
import xmlrpc.client


class UpdateScreen(models.Model):
    _name = "update.screen"

    field1 = fields.Integer('Field 1')
    field2 = fields.Integer('Field 2')
    field3 = fields.Char('Field3')
    field4 = fields.Boolean('Field4')
    field5 = fields.Text('Field5')
    date = fields.Date('Date')
    date2 = fields.Datetime('Date2')
    date3 = fields.Datetime('Date3')
