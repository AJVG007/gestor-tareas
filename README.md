# Task Manager API

A Django REST Framework API for managing tasks.

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with the following variables:

   ```env
   SECRET_KEY=your_secret_key
   NAME=your_db_name
   USER=your_db_user
   PASSWORD=your_db_password
   HOST=your_db_host
   PORT=your_db_port
   ```

6. Run migrations: `python manage.py migrate`
7. Create a superuser: `python manage.py createsuperuser`
8. Run the server: `python manage.py runserver`

## API Endpoints

### User Endpoints

- **Register**: `POST /users/register/`
  - Request Body:

    ```json
    {
      "username": "your_username",
      "email": "your_email@example.com",
      "password": "your_password"
    }
    ```

- **Login**: `POST /users/login/`
  - Request Body:

    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```

  - Response: Sets HTTP-only cookies for JWT authentication

- **User Details**: `GET /users/details/`
  - Requires authentication via JWT cookie

### Task Endpoints

- **List Tasks**: `GET /tareas/list/`
  - Requires authentication via JWT cookie
  - Returns all tasks owned by the authenticated user

- **Create Task**: `POST /tareas/create/`
  - Requires authentication via JWT cookie
  - Request Body:

    ```json
    {
      "title": "Task Title",
      "description": "Task Description",
      "completed": false
    }
    ```

  - Validation: Title must be at least 3 characters long

- **Task Detail/Update/Delete**: `GET/PUT/DELETE /tareas/detail/<task_id>/`
  - Requires authentication via JWT cookie
  - Only the owner can update or delete their own tasks
  - For PUT requests, use the same format as the create endpoint

- **Filter Completed Tasks**: `GET /tareas/filter/completed/`
  - Requires authentication via JWT cookie
  - Returns all completed tasks owned by the authenticated user

## Running Tests

Run the tests with:

`python manage.py test`
