# -*- coding: utf-8 -*-
from osv import osv, fields

class mp_product(osv.osv):
    _name = 'mp.product'
    _columns = {
        'name': fields.char('Ten my pham', required=True),
        # thêm quan hệ
        'category_id': fields.many2one('mp.category', 'Danh muc'),
    }
mp_product()