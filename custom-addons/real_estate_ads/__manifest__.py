{
    "name": "Real Estate Ads",
    "version": "1.0",
    "website": "https://www.albertolacerda.com",
    "author": "Alberto Lacerda",
    "description": """
        Real Estate module to show available properties
    """,
    "category": "Sales",
    "depends": [],
    "demo": [
        # 'demo/property_tag.xml'
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/property_view.xml',
        'views/property_type_view.xml',
        'views/property_tag_view.xml',
        'views/property_offer_view.xml',
        'views/menu_items.xml',


        # Data Files
        'data/property_type.xml',
        # 'data/estate.property.type.csv',
        'demo/property_tag.xml',
        'data/property.xml'
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}