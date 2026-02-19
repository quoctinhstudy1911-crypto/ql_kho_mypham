# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class mp_stock_document_line(osv.osv):
    _name = 'mp.stock.document.line'
    _columns = {
        'document_id': fields.many2one('mp.stock.document', 'Phieu'),
        'product_id': fields.many2one('mp.product', 'San pham'),
        'quantity': fields.float('So luong'),
    }

mp_stock_document_line()
