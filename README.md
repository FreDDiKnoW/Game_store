# GameStore — Online PC Games Store
## Frontend - https://github.com/FreDDiKnoW/Game_store-FrontEND
GameStore is a simple online store for PC video games. The site allows users to browse and search games, view detailed game pages, browse developers and publishers, register and log in, maintain a personal profile with order history, store games in a cart, and place simplified orders (no payment step in this phase). The project will be a single repository containing a backend REST API (e.g., Django REST Framework / FastAPI / Express) and a separate frontend client.

## Major features (scope for initial weeks)

 - Public catalog of games with filtering, searching and sorting
 - Game detail page
 - Developer and publisher pages (list and detail)
 - User registration & login (JWT or session-based)
 - User profile with order history
 - Cart: add/remove items, view cart
 - Simple checkout: convert cart into an order
 - Admin endpoints for adding/updating/deleting games, developers, publishers (protected)
 - Static pages: About / Contacts / Delivery & Returns

## Endpoints

### --> Register
- Purpose: Register a new user.
- Method: POST
- Request body:
```
{
  "email": "user@example.com",
  "username": "gamer123",
  "password": "StrongPassword!",
  "first_name": "Andrew",
  "last_name": "Krow"
}
```
Response:

201 Created + created user 

```
{
  "id": 12,
  "email": "user@example.com",
  "username": "gamer123",
  "first_name": "Andrew",
  "last_name": "Krow",
  "created_at": "2025-09-29T12:00:00Z"
}
```
### --> Login

- Purpose: Obtain auth token (JWT) or start session.
- Method: POST
- Request body:
```
{
  "username": "gamer123",
  "password": "StrongPassword!"
}
```
Response:

200 OK
```
{
    "access": "<jwt-access-token>",
    "refresh": "<jwt-refresh-token>",
    "user": {
        "id": 12,
        "username": "gamer123",
        "email": "user@example.com"
    }
}
```

### Games (catalog)
- Purpose: List games with search, filter, sorting and pagination.
- Method: GET
- Query params (examples):
<details>
<summary>Click to expand query params</summary>

- `q` — full-text search against title and short description  
- `developer` — developer id or slug  
- `publisher` — publisher id or slug  
- `genre` — genre id or slug (can repeat)  
- `released_before` / `released_after` — ISO dates  
- `min_price` / `max_price`  
- `min_rating` / `max_rating`  

</details>

Response 200 OK (paginated):
```
{
  "count": 4,
  "next": "...",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Minecraft",
      "slug": "minecraft",
      "short_description": "A pixel survival game...",
      "price": 39.99,
      "currency": "USD",
      "released_at": "2009-11-05",
      "rating": 4.7,
      "developer": { "id": 3, "name": "Mojang" },
      "genres": [ {"id":2, "name":"Adventure"} ],
      "cover_url": "minecraft.jpg"
    }
  ]
}
```
### -->Add new game
- Purpose: Create a new game (admin only).
- Method: POST
- Request body (example):
```
{
  "title": "New Game",
  "slug": "new-game",
  "short_description": "description",
  "description": "Full description...",
  "price": 45.10,
  "currency": "USD",
  "released_at": "2025-01-15",
  "developer_id": 3,
  "publisher_id": 4,
  "genre_ids": [1,2],
  "platforms": ["Windows"],
  "stock": 999
}
```
Response: 201 Created with created game object.

### --> Detail page
- Purpose: Game detail page.
- Method: GET
- Response 200 OK:
```
{
  "id": 1,
  "title": "Space Raiders II",
  "slug": "space-raiders-ii",
  "description": "Long HTML/Markdown description...",
  "price": 19.99,
  "currency": "USD",
  "released_at": "2024-11-05",
  "developer": { "id": 3, "name": "Nebula Games", "slug": "nebula-games" },
  "publisher": { "id": 4, "name": "AstroPub" },
  "genres": [ {"id":2, "name":"RPG"} ],
  "screenshots": ["..."],
  "rating": 4.5,
  "stock": 123
}
```
PUT/PATCH (admin only)
DELETE (admin only)
