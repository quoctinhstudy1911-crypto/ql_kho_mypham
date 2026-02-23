# -*- coding: utf-8 -*-
from osv import osv, fields
from tools.translate import _


class mp_category(osv.osv):
    _name = 'mp.category'
    _description = u'Danh mục mỹ phẩm'
    _order = 'name asc'

    # ========================
    # CỘT DỮ LIỆU
    # ========================

    _columns = {
        'name': fields.char(u'Tên danh mục', required=True, size=128),
        'description': fields.text(u'Mô tả'),
        'active': fields.boolean(u'Còn sử dụng'),
    }

    _defaults = {
        'active': True,
    }

    # ========================
    # CHUẨN HÓA DỮ LIỆU
    # ========================

    def _normalize_name(self, name):
        name = (name or '').strip().title()
        if not name:
            raise osv.except_osv(
                _(u'Lỗi dữ liệu'),
                _(u'Tên danh mục không được để trống!')
            )
        return name

    def create(self, cr, uid, vals, context=None):
        if 'name' in vals:
            vals['name'] = self._normalize_name(vals['name'])
        return super(mp_category, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        if 'name' in vals:
            vals['name'] = self._normalize_name(vals['name'])
        return super(mp_category, self).write(cr, uid, ids, vals, context=context)

    # ========================
    # RÀNG BUỘC TOÀN VẸN
    # ========================
        # - Tên danh mục phải duy nhất (case-insensitive)
        # - Không phụ thuộc trạng thái active
    def _check_name_unique(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids, context=context):
            if not rec.name:
                continue

            cr.execute("""
                SELECT id FROM mp_category
                WHERE lower(name)=lower(%s)
                AND id!=%s
            """, (rec.name, rec.id))

            if cr.fetchone():
                return False

        return True

    _constraints = [
        (_check_name_unique, u'Tên danh mục đã tồn tại!', ['name']),
    ]

    # ========================
    # KHÔNG CHO XÓA NẾU ĐÃ SỬ DỤNG
    # ========================
        # Không cho phép xóa danh mục nếu đang được sử dụng bởi sản phẩm.
            # Đảm bảo dữ liệu không bị mồ côi và giữ tính toàn vẹn hệ thống.
    def unlink(self, cr, uid, ids, context=None):
        product_obj = self.pool.get('mp.product')

        for category in self.browse(cr, uid, ids, context=context):
            product_ids = product_obj.search(
                cr, uid,
                [('category_id', '=', category.id)],
                context=context
            )

            if product_ids:
                raise osv.except_osv(
                    _(u'Không thể xóa!'),
                    _(u'Danh mục "%s" đang được sử dụng bởi sản phẩm.') % (category.name or u'')
                )

        return super(mp_category, self).unlink(cr, uid, ids, context=context)


mp_category()