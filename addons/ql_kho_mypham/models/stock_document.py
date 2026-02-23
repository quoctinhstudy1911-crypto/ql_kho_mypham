# -*- coding: utf-8 -*-
from osv import osv, fields

class mp_stock_document(osv.osv):
    _name = 'mp.stock.document'

    _columns = {
        'name': fields.char('Số phiếu', required=True),
        'date': fields.date('Ngày', required=True),
        'type': fields.selection(
    [('in','Nhập'),('out','Xuất')],
    'Loại',
    required=True
),
        'state': fields.selection([('draft','Nhập liệu'),('done','Hoàn tất')],'Trạng thái'),
        'line_ids': fields.one2many('mp.stock.document.line','document_id','Chi tiet'),
    }

    _sql_constraints = [
    ('name_unique',
     'unique(name)',
     u'Số phiếu không được trùng!')
]
    _defaults = {
        'state': 'draft',
    }

    def _get_product_qty(self, cr, uid, product_id, context=None):
        qty = 0.0
        line_obj = self.pool.get('mp.stock.document.line')

        line_ids = line_obj.search(cr, uid, [
            ('product_id','=',product_id),
            ('document_id.state','=','done')
        ], context=context)

        for line in line_obj.browse(cr, uid, line_ids, context=context):
            if line.document_id.type == 'in':
                qty += line.quantity
            else:
                qty -= line.quantity

        return qty

    def action_done(self, cr, uid, ids, context=None):
        for doc in self.browse(cr, uid, ids, context=context):
            if not doc.line_ids:
                raise osv.except_osv(u'Lỗi', u'Phiếu không có sản phẩm!')

            if doc.type == 'out':
                for line in doc.line_ids:
                    current_qty = self._get_product_qty(cr, uid, line.product_id.id, context)
                    if line.quantity > current_qty:
                        raise osv.except_osv(
                            u'Âm kho!',
                            u'Sản phẩm %s chỉ còn %s' % (line.product_id.name, current_qty)
                        )

        self.write(cr, uid, ids, {'state':'done'}, context=context)
        return True
    
    def write(self, cr, uid, ids, vals, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
            
        for doc in self.browse(cr, uid, ids, context=context):
            if doc.state == 'done':
                raise osv.except_osv(
                    u'Không được sửa!',
                    u'Phiếu đã hoàn tất không thể sửa.'
                )
        return super(mp_stock_document, self).write(cr, uid, ids, vals, context=context)

    def unlink(self, cr, uid, ids, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
            
        for doc in self.browse(cr, uid, ids, context=context):
            if doc.state == 'done':
                raise osv.except_osv(
                    u'Không được xóa!',
                    u'Phiếu đã hoàn tất không thể xóa.'
                )
        return super(mp_stock_document, self).unlink(cr, uid, ids, context=context)

mp_stock_document()