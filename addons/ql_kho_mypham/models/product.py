# -*- coding: utf-8 -*-
from osv import osv, fields
from tools.translate import _

class mp_product(osv.osv):
    _name = 'mp.product'
    _description = u'Sản phẩm mỹ phẩm'
    _order = 'code'

    # ========================
    # CẤU TRÚC DỮ LIỆU
    # ========================
    _columns = {

        'code': fields.char(
            u'Mã sản phẩm',
            required=True,
            size=64
        ),

        'name': fields.char(
            u'Tên sản phẩm',
            required=True,
            size=128
        ),

        'category_id': fields.many2one(
            'mp.category',
            u'Danh mục',
            required=True
        ),

        'active': fields.boolean(u'Còn kinh doanh'),

        'note': fields.text(u'Mô tả'),

        'image': fields.binary(u'Hình ảnh'),
        'image_filename': fields.char(u'Tên file ảnh'),
    }

    _defaults = {
        'active': True,
        'code': '/',   # 👈 cực kỳ quan trọng
    }

    # ========================
    # CHUẨN HÓA TÊN
    # ========================
    def _normalize_name(self, name):
        name = (name or '').strip().title()
        if not name:
            raise osv.except_osv(
                _(u'Lỗi dữ liệu'),
                _(u'Tên sản phẩm không được để trống!')
            )
        return name

    # ========================
    # CREATE
    # ========================
    def create(self, cr, uid, vals, context=None):

        # Nếu code là '/' thì sinh sequence
        if vals.get('code', '/') == '/':
            vals['code'] = self.pool.get('ir.sequence').get(
                cr, uid, 'mp.product'
            ) or '/'

        if 'name' in vals:
            vals['name'] = self._normalize_name(vals['name'])

        return super(mp_product, self).create(cr, uid, vals, context=context)

    # ========================
    # WRITE
    # ========================
    def write(self, cr, uid, ids, vals, context=None):
        if 'name' in vals:
            vals['name'] = self._normalize_name(vals['name'])

        return super(mp_product, self).write(cr, uid, ids, vals, context=context)

    # ========================
    # UNIQUE CODE
    # ========================
    _sql_constraints = [
        ('code_unique', 'unique(code)', u'Mã sản phẩm đã tồn tại!')
    ]

    # ========================
    # KHÔNG CHO XÓA NẾU ĐÃ PHÁT SINH
    # ========================
    def unlink(self, cr, uid, ids, context=None):
        line_obj = self.pool.get('mp.stock.document.line')

        for product in self.browse(cr, uid, ids, context=context):
            line_ids = line_obj.search(
                cr, uid,
                [('product_id', '=', product.id)],
                context=context
            )

            if line_ids:
                raise osv.except_osv(
                    _(u'Không thể xóa!'),
                    _(u'Sản phẩm "%s" đã phát sinh giao dịch kho.') % product.name
                )

        return super(mp_product, self).unlink(cr, uid, ids, context=context)

mp_product()