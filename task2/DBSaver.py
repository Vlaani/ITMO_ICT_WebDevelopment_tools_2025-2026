import sys
import os
from pathlib import Path

root_dir = Path(os.getcwd()).parent / 'app'
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from typing import Any
from sqlmodel import select

from models.product import Product
from models.attribute import Attribute
from models.attribute_name import AttributeName
from models.property_name import PropertyName
from models.property import Property
from models.variant import Variant
from AutoDBDict import AutoDBDict
from db.db import get_session

to_db = AutoDBDict()

to_db.set_stmt(Product, lambda obj: select(Product).where(Product.name == obj.name))
to_db.set_stmt(AttributeName, lambda obj: select(AttributeName).where(AttributeName.name == obj.name))
to_db.set_stmt(
    Attribute,
    lambda obj: select(Attribute).where(
        Attribute.attribute_name_id == obj.attribute_name_id,
        Attribute.value == obj.value,
    ),
)
to_db.set_stmt(PropertyName, lambda obj: select(PropertyName).where(PropertyName.name == obj.name))
to_db.set_stmt(
    Property,
    lambda obj: select(Property).where(
        Property.property_name_id == obj.property_name_id,
        Property.value == obj.value,
        Property.attribute_id == obj.attribute_id,
    ),
)
to_db.set_stmt(Variant, lambda obj: select(Variant).where(Variant.product_id == obj.product_id))

async def save_to_db(data: dict[str, Any]):
    print('Попытка сохранить данные')
    id_to_att_prop = {}

    with get_session() as session:
        if not 'subject' in data['data']['result']['GLOBAL_DATA']['globalData']:
            return
        product_db = to_db.add_to_db(Product(name=data['data']['result']['GLOBAL_DATA']['globalData']['subject']), session)
        
        for att in data['data']['result']['PRODUCT_PROP_PC']['showedProps']:
            if 'attrName' in att:
                an = to_db.add_to_db(AttributeName(name=att['attrName']), session)
                to_db.add_to_db(Attribute(attribute_name_id=an.id, value=att['attrValue']), session)

        for prop in data['data']['result']['SKU']['skuProperties']:
            an = to_db.add_to_db(AttributeName(name=prop['skuPropertyName']), session)
            for val in prop['skuPropertyValues']:
                a = to_db.add_to_db(Attribute(attribute_name_id=an.id, value=val['propertyValueName']), session)
                id_to_att_prop[f'{prop['skuPropertyId']}:{val['propertyValueIdLong']}'] = (a, [])
                if "propertySizeChartInfo" in val:
                    for p in val["propertySizeChartInfo"]:
                        pn = to_db.add_to_db(PropertyName(name=p['name']), session)
                        id_to_att_prop[f'{prop['skuPropertyId']}:{val['propertyValueIdLong']}'][1].append((pn.id, p['value']))
        
        variants = {}

        for key, val in data['data']['result']['PRICE']['skuIdStrPriceInfoMap'].items():
            variants[key] = {"price": float(val['salePriceString'][:-2].replace(" ", "").replace(',', '.'))}

        for path in data['data']['result']['SKU']['skuPaths']:
            variants[path['skuIdStr']]['attributes'] = []
            att_combination = path['path'].split(";")
            for seq in att_combination:
                variants[path['skuIdStr']]['attributes'].append(id_to_att_prop[seq][0])

            var = to_db.add_to_db(Variant(product_id=product_db.id, price=int(variants[path['skuIdStr']]['price']), stock=path['skuStock'], attributes=variants[path['skuIdStr']]['attributes']), session)

            for seq in att_combination:
                if len(id_to_att_prop[seq][1]) != 0:
                    for prop in id_to_att_prop[seq][1]:
                        to_db.add_to_db(Property(property_name_id=prop[0], attribute_id=id_to_att_prop[seq][0].id, variant_id=var.id, value=prop[1]), session)
                    
            print(f"Variant: {var}")

        session.commit()
