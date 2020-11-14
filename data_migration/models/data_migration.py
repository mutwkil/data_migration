'''
Created on Aug 27, 2017

@author: Mutwkil Faisal
'''
from odoo import models, fields, api, _
import xmlrpc.client
from odoo.exceptions import UserError



class DataMigration(models.Model):
    _name = "data.migration"

    db_url = fields.Char('DB connection')
    db_name = fields.Char('DB Name')
    db_user = fields.Char('DB user')
    db_pass = fields.Char('DB password')

    # model_name = fields.Char('Model Name')
    model_name = fields.Many2one('ir.model')
    fields_list = fields.Char('Fields')
    db1_fields = fields.One2many('data.migration.db1.fields', 'data_migration', 'db1 fields')
    domain = fields.Char('Domain')
    get_inactive = fields.Boolean('Archived Data')

    _rec_name = 'model_name'

    def quote(s):
        """Returns quoted PO term string, with special PO characters escaped"""
        assert r"\n" not in s, "Translation terms may not include escaped newlines ('\\n'), please use only literal newlines! (in '%s')" % s
        return '"%s"' % s.replace('\\', '\\\\') \
            .replace('"', '\\"') \
            .replace('\n', '\\n"\n"')

    def get_models(self):
        models = self.env['ir.model'].browse('model')

    def test(self):
        self.db1_fields = [(5, 0, 0)]
        unwanted_columns = [
            'message_follower_ids', 'message_needaction',
            'message_channel_ids', 'message_partner_ids', 'message_unread',
            'message_ids', 'message_last_post', 'message_is_follower',
            'display_name', 'create_uid', '__last_update', 'message_needaction_counter',
            'write_date', 'write_uid', 'create_date', 'message_unread_counter']
        try:
            common_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.db_url))
            models_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.db_url))
            # version_db1 = common_1.version()
            # print('Details of db_1', version_db1)
            print('fff >> ', [self.fields_list])
            print('---333--', type(fields), fields)
            uid_db1 = common_1.authenticate(self.db_name, self.db_user, self.db_pass, {})
            db_1_obj = models_1.execute_kw(self.db_name, uid_db1, self.db_pass, self.model_name.model, 'search_read',
                                           [[]],
                                           {'fields': [], 'limit': 1})
            print('............', db_1_obj[0])
            # for iii in db_1_obj[0].keys():
            #     if iii not in unwanted_columns:
            #         self.db1_fields = [(0, 0, {'name': iii, 'type': type()})]
            for mm in self.env['ir.model'].search([('model', '=', str(self.model_name.model))]):
                for iii in mm.field_id:
                    if iii.name not in unwanted_columns:
                        self.db1_fields = [(0, 0, {'name': iii.name, 'type': iii.ttype})]
        except Exception:
            raise UserError(_('Connection unsuccessfull  !'))


    def connect(self):
        # fields = self.fields_list.split(",")
        bad_chars = [';', ':', '!', "*", '&', "\'", '	']
        print('--------', self.db1_fields.ids)
        ll_list = []
        for f_name in self.db1_fields:
            if f_name.is_active:
                ll_list.append(f_name.name)

        # ll_list.append('sequence_id')
        # ll_list.append('invoice_reference_type')
        # ll_list.append('invoice_reference_model')
        # ll_list.append('date')
        # ll_list.append('fields_id')
        # ll_list.append('company_id')

        print('lstttt >>>>>>>>>>>>>>>>>>>>>', ll_list)

        common_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.db_url))
        models_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.db_url))
        # version_db1 = common_1.version()
        # print('Details of db_1', version_db1)
        print('fff >> ', [self.fields_list])
        print('---333--', type(fields), fields)
        print('domain-------------->', self.domain)
        domain = self.domain
        # domain = domain.split(',')
        uid_db1 = common_1.authenticate(self.db_name, self.db_user, self.db_pass, {})
        if not self.get_inactive:
            db_1_obj = models_1.execute_kw(self.db_name, uid_db1, self.db_pass, self.model_name.model, 'search_read',
                                           [[]],
                                           {'fields': ll_list})
            # ['id','not in',(1,2,3,4,5)]
            # ['id', '>', 3]
        else:
            db_1_obj = models_1.execute_kw(self.db_name, uid_db1, self.db_pass, self.model_name.model, 'search_read',
                                           [[['active', '=', False]]],
                                           {'fields': ll_list})

        for rec in db_1_obj:
            model_name = str(self.model_name.model).replace('.', '_')
            lsst_ids = []
            for ifield in self.db1_fields:
                if ifield.is_active == True:
                    if ifield.type in ['many2one']:
                        a = {4: 3, 24: 17, 26: 4, 6: 5, 7: 9, 21: 12, 23: 16, 15: 11, 9: 15, 19: 8, 8: 13, 17: 6,
                             20: 10, 22: 18, 25: 14, 3: 2, 18: 7, 2: 1}

                        if rec[ifield.name]:
                            if ifield.name == 'user_type_id':
                                result = a[rec[ifield.name][0]]
                                lsst_ids.append(str(result))
                            else:
                                lsst_ids.append(str(rec[ifield.name][0]))
                        else:
                            lsst_ids.append(str('null'))
                    elif ifield.type in ['selection']:
                        lsst_ids.append("\'" + str(rec[ifield.name]) + "\'")
                    elif ifield.type in ['char', 'text', 'date']:
                        if not rec[ifield.name]:
                            lsst_ids.append(str('null'))
                        else:
                            result = str(rec[ifield.name])
                            for i in bad_chars:
                                result = result.replace(i, '')
                            lsst_ids.append("\'" + result + "\'")
                    else:
                        lsst_ids.append(str(rec[ifield.name]))
            print('PPPP >> ', lsst_ids)
            t = '1-1-2020'
            # f = 'no'
            # lsst_ids.append(str(100))
            # lsst_ids.append("\'" + t + "\'")
            # lsst_ids.append("\'" + f + "\'")
            # lsst_ids.append(str(1))
            # lsst_ids.append(str(1))
            query = "INSERT INTO {} ({}) VALUES ({})".format(
                (model_name),
                ", ".join(name for name in ll_list),
                ", ".join(name for name in lsst_ids),
            )

            print('+++++++++++++++++++++++++++++++++++++++++', query)
            result = self._cr.execute(query)

    class DataMigration(models.Model):
        _name = "data.migration.db1.fields"

        name = fields.Char('name')
        is_active = fields.Boolean('active')
        data_migration = fields.Many2one('data.migration')
        type = fields.Char('Type')
