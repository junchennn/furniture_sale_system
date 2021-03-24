import pandas as pd
from products.models import Product


df = pd.read_csv('problem1_inventory.csv')

for index, row in df.iterrows():
    Product.objects.create(name=row['Item'], price=row['Cost'], inventory=row['Quantity'])
    print('Object{} created successfully!'.format(index))

