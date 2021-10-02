# multi-dimen-product
> Simple api that works with multidimensional product variants

## Endpoints
- GET  `products`
- POST `products`

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
            "Spicy",
            "Salty"
          ],
        },
        {
          "name": "Size",
          "options": [
            "Small",
            "Medium", 
            "Large"
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
  "name": "Test Chips",
  "attributes": [
    {
      "name": "Flavor",
      "options": [
        "Spicy",
        "Salty"
      ]
    },
    {
      "name": "Size",
      "options": [
        "Small",
        "Medium",
        "Large"
      ]
    }
  ]
}
```

Success Response Example:

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