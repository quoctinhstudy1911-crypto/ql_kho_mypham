# -*- coding: utf-8 -*-
from osv import osv, fields
import logging

_logger = logging.getLogger(__name__)


class mp_stock_document(osv.osv):
    _name = 'mp.stock.document'

    _columns = {
        'name': fields.char(u'Số phiếu', required=True),
        'date': fields.date(u'Ngày', required=True),
        'type': fields.selection(
            [('in', u'Nhập'), ('out', u'Xuất')],
            u'Loại',
            required=True
        ),
        'state': fields.selection(
            [('draft', u'Nhập liệu'), ('done', u'Hoàn tất')],
            u'Trạng thái'
        ),
        'line_ids': fields.one2many(
            'mp.stock.document.line',
            'document_id',
            u'Chi tiết phiếu'
        ),
    }

    _sql_constraints = [
        ('name_unique',
         'unique(name)',
         u'Số phiếu không được trùng!')
    ]

    _defaults = {
        'state': 'draft',
        'name': '/',
    }

    # =====================================================
    # TÍNH TỒN KHO
    # =====================================================
    def _get_product_qty(self, cr, uid, product_id, context=None):

        qty = 0.0
        line_obj = self.pool.get('mp.stock.document.line')

        line_ids = line_obj.search(cr, uid, [
            ('product_id', '=', product_id),
            ('document_id.state', '=', 'done')
        ], context=context)

        for line in line_obj.browse(cr, uid, line_ids, context=context):

            if line.document_id.type == 'in':
                qty += line.quantity
            else:
                qty -= line.quantity

        return qty

    # =====================================================
    # HOÀN TẤT PHIẾU
    # =====================================================
    def action_done(self, cr, uid, ids, context=None):

        for doc in self.browse(cr, uid, ids, context=context):

            if not doc.line_ids:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Phiếu không có sản phẩm!'
                )

            if doc.type == 'out':

                for line in doc.line_ids:

                    current_qty = self._get_product_qty(
                        cr, uid, line.product_id.id, context
                    )

                    if line.quantity > current_qty:

                        raise osv.except_osv(
                            u'Âm kho!',
                            u'Sản phẩm %s chỉ còn %s'
                            % (line.product_id.name, current_qty)
                        )

        self.write(cr, uid, ids, {'state': 'done'}, context=context)

        return True

    # =====================================================
    # KHÔNG CHO SỬA KHI DONE
    # =====================================================
    def write(self, cr, uid, ids, vals, context=None):

        if isinstance(ids, (int, long)):
            ids = [ids]

        for doc in self.browse(cr, uid, ids, context=context):

            if doc.state == 'done':

                raise osv.except_osv(
                    u'Không được sửa!',
                    u'Phiếu đã hoàn tất không thể sửa.'
                )

        return super(mp_stock_document, self).write(
            cr, uid, ids, vals, context=context
        )

    # =====================================================
    # KHÔNG CHO XÓA
    # =====================================================
    def unlink(self, cr, uid, ids, context=None):

        if isinstance(ids, (int, long)):
            ids = [ids]

        for doc in self.browse(cr, uid, ids, context=context):

            if doc.state == 'done':

                raise osv.except_osv(
                    u'Không được xóa!',
                    u'Phiếu đã hoàn tất không thể xóa.'
                )

            if doc.line_ids:

                raise osv.except_osv(
                    u'Lỗi tham chiếu',
                    u'Không thể xóa phiếu vì còn %s dòng liên quan.'
                    % len(doc.line_ids)
                )

        return super(mp_stock_document, self).unlink(
            cr, uid, ids, context=context
        )

    # =====================================================
    # CREATE - SINH MÃ TỰ ĐỘNG
    # =====================================================
    def create(self, cr, uid, vals, context=None):

        # kiểm tra dòng chi tiết
        for cmd in vals.get('line_ids', []):

            if isinstance(cmd, (list, tuple)) and cmd[0] == 0:

                line_vals = cmd[2] or {}

                try:
                    qty = float(line_vals.get('quantity', 0))
                except:
                    raise osv.except_osv(
                        u'Lỗi',
                        u'Số lượng không hợp lệ'
                    )

                if qty <= 0:

                    raise osv.except_osv(
                        u'Lỗi',
                        u'Số lượng phải lớn hơn 0'
                    )

        # kiểm tra loại phiếu
        if not vals.get('type'):

            raise osv.except_osv(
                u'Lỗi',
                u'Phải chọn loại phiếu.'
            )

        # sinh số phiếu
        if not vals.get('name') or vals.get('name') == '/':

            seq_code = 'mp.stock.document.%s' % vals.get('type')

            seq_obj = self.pool.get('ir.sequence')

            while True:

                seq = seq_obj.get(cr, uid, seq_code, context=context)

                if not seq:

                    raise osv.except_osv(
                        u'Lỗi',
                        u'Không lấy được sequence.'
                    )

                exist = self.search(
                    cr, uid,
                    [('name', '=', seq)],
                    context=context
                )

                if not exist:
                    break

            vals['name'] = seq

        return super(mp_stock_document, self).create(
            cr, uid, vals, context=context
        )


mp_stock_document()