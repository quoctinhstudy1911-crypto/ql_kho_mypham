# -*- coding: utf-8 -*-
from osv import osv, fields

class mp_category(osv.osv):
    _name = 'mp.category'
    _columns = {
        'name': fields.char('Ten danh muc', required=True),
        'description': fields.text('Mo ta'),
    }
mp_category()