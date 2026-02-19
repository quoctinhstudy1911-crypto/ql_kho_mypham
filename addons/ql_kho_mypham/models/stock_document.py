# -*- coding: utf-8 -*-
from osv import osv, fields

class mp_stock_document(osv.osv):
    _name = 'mp.stock.document'
    _columns = {
        'name': fields.char('So phieu'),
        
        # thêm thông tin nghiệp vụ
        'date': fields.date('Ngay'),
        'type': fields.selection([('in','Nhap'),('out','Xuat')],'Loai'),
        'state': fields.selection([('draft','Nhap lieu'),('done','Hoan tat')],'Trang thai'),

        # quan hệ quan trọng nhất
        'line_ids': fields.one2many('mp.stock.document.line','document_id','Chi tiet'),
    }
mp_stock_document()