# multi-dimen-product
> Simple api that works with multidimensional product variants

## Endpoints
- GET  `\api\products`
- POST `\api\products`

### GET `products`

Request Payload: N/A

Success Response Example: 

```
{
	"status": "success",
	"data": [
		{
			"name": "Example Chips",
			"attributes": [
				{
					"name": Flavor",
					"options": [
						{
							"name": "Spicy",
						},
						{
							"name": "Salty"
						}
					],
				},
				{
					"name": "Size",
					"options": [
						{
							"name": "Small"
						},
						{
							"name": "Medium"
						},
						{
							"name": "Large"
						}
					]
				}
			]
		},
		{
			"name": "One Variant Snack",
			"attributes": []
		}
	]
}
```

### POST `products`

Request Payload:

```
{
	"name": "Example Chips",
	"attributes": [
		{
			"name": "Flavor",
			"options": [
				{
					"name": "Spicy"
				},
				{
					"name": "Salty"
				}
			]
		},
		{
			"name": "Size",
			"options": [
				{
					"name": "Small"
				},
				{
					"name": "Medium"
				},
				{
					"name": "Large"
				}
			]
		}
	]
}
```

Success Response Example:

> Note, duplicate products are allowed, BUT duplicate options for a single attribute or duplicate attributes for a single product are not allowed

```
{
	"status": "success",
	"data": []
}
```

Fail Response Example:

```
{
	"status": "error",
	"errorMessage": "Name of product cannot be empty"
}
