# -*- coding: utf-8 -*-
from osv import osv, fields

class mp_stock_document_line(osv.osv):
    _name = 'mp.stock.document.line'

    _columns = {
        'document_id': fields.many2one(
            'mp.stock.document',
            'Phiếu',
            required=True
        ),
        'product_id': fields.many2one(
            'mp.product',
            'Sản phẩm',
            required=True
        ),
        'quantity': fields.float(
            'Số lượng',
            required=True
        ),
        'note': fields.char(
            'Ghi chú'
        ),
    }

    # ==========================================
    # RÀNG BUỘC: SỐ LƯỢNG PHẢI > 0
    # ==========================================
    def _check_quantity_positive(self, cr, uid, ids, context=None):
        for line in self.browse(cr, uid, ids, context=context):
            if line.quantity <= 0:
                return False
        return True

    _constraints = [
        (_check_quantity_positive,
         u'So lượng phải lớn hơn 0',
         ['quantity'])
    ]
    _sql_constraints = [
    ('unique_product_per_document',
     'unique(document_id, product_id)',
     u'Mỗi sản phẩm chỉ được xuất hiện 1 lần trong phiếu!')
    ]
    # ==========================================
    # KHÔNG CHO SỬA KHI PHIẾU DONE
    # ==========================================
    def write(self, cr, uid, ids, vals, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]

        for line in self.browse(cr, uid, ids, context=context):
            if line.document_id.state == 'done':
                raise osv.except_osv(
                    u'Lỗi!',
                    u'Không được sửa dòng phiếu đã hoàn tất!'
                )

        return super(mp_stock_document_line, self).write(cr, uid, ids, vals, context=context)

    # ==========================================
    # KHÔNG CHO XÓA
    # ==========================================
    def unlink(self, cr, uid, ids, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]

        for line in self.browse(cr, uid, ids, context=context):
            if line.document_id.state == 'done':
                raise osv.except_osv(
                    u'Lỗi!',
                    u'Không được xóa dòng phiếu đã hoàn tất!'
                )

        return super(mp_stock_document_line, self).unlink(cr, uid, ids, context=context)

    # ==========================================
    # KHÔNG CHO THÊM DÒNG VÀO PHIẾU DONE
    # ==========================================
    def create(self, cr, uid, vals, context=None):
        if vals.get('document_id'):
            doc = self.pool.get('mp.stock.document').browse(
                cr, uid, vals.get('document_id'), context=context
            )
            if doc and doc.state == 'done':
                raise osv.except_osv(
                    u'Lỗi!',
                    u'Không được thêm dòng phiếu đã hoàn tất!'
                )

        return super(mp_stock_document_line, self).create(cr, uid, vals, context=context)

mp_stock_document_line()