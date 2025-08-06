# Advanced API Project

## Views

This project uses Django REST Framework generic views to manage Book data via a RESTful API.

### Endpoints

| Method | URL                     | Description                | Auth Required |
|--------|--------------------------|----------------------------|---------------|
| GET    | /api/books/             | List all books             | No            |
| GET    | /api/books/<id>/        | Retrieve single book       | No            |
| POST   | /api/books/create/      | Create new book            | Yes           |
| PUT    | /api/books/<id>/update/ | Update existing book       | Yes           |
| DELETE | /api/books/<id>/delete/ | Delete a book              | Yes           |

### Permissions

- `IsAuthenticated`: Required for create, update, and delete operations.
- `AllowAny`: For list and detail views.

### Serializer Validation

- `publication_year` is validated to ensure it is not in the future.




### BookListView API Features

- **Filter books by title, author, or year:**
  `/api/books/?publication_year=2022`
- **Search for books by title or author name:**
  `/api/books/?search=Chinua`
- **Order books by title or publication year:**
  `/api/books/?ordering=title`
