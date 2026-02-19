# -*- coding: utf-8 -*-
{
    "name": "Quan Ly Kho My Pham",
    "version": "1.0",
    "author": "KimToa_QuocTinh",
    "category": "Warehouse",
    "description": """
Module quan ly kho my pham
- Danh muc
- San pham
- Phieu kho
""",

    "depends": ["base"],

    # DATA
    "init_xml": [],
    "demo_xml": [],

    # LOAD GIAO DIEN
    "update_xml": [
        "views/category_view.xml",
        "views/product_view.xml",
        "views/stock_document_view.xml",
        "views/menu.xml"
    ],

    "active": False,
    "installable": True,
}
