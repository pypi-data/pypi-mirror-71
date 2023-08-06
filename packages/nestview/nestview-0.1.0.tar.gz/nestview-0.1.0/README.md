# NestView

Explore nested structures in Python at various levels of granularity.

# Examples

from nestview import nestview

```python
    from nestview import nestview


    nested_struct = {
        "orders": [
            {
                "id": "id1",
                "quantity": 43,
                "product": {
                    "id": "prodId1",
                    "name": "Prod 1",
                    "desc": "Description",
                },
            },
            {
                "id": "id2",
                "quantity": 12,
                "product": {
                    "id": "prodId1",
                    "name": "Prod 1",
                    "desc": "Description",
                },
            },
            {
                "id": "id3",
                "quantity": 3,
                "product": {
                    "id": "prodId2",
                    "name": "Prod 2",
                    "desc": "Description",
                },
            },
            {
                "id": "id4",
                "quantity": 2,
                "product": {
                    "id": "prodId1",
                    "name": "Prod 1",
                    "desc": "Description",
                },
            },
            {
                "id": "id5",
                "quantity": 4,
                "product": {
                    "id": "prodId1",
                    "name": "Prod 1",
                    "desc": "Description",
                },
            },
        ]
    }


    print(nestview(nested_struct))
```

gives

    {'orders': '[25]'}

For the same structure with more details:

    print(nestview(nested_struct, level=2))

gives

    {'orders': ['{5}', '{5}', '{5}', '{5}', '{5}']}