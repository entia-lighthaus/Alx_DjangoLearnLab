# Django Access Control Setup

This project uses Django's Groups and Permissions system to manage user access.

## Permissions Added
- `can_view`: View articles
- `can_create`: Create new articles
- `can_edit`: Edit existing articles
- `can_delete`: Delete articles

## Groups Configured
- Viewers
- Editors
- Admins

## Usage
Assign users to groups via admin or shell. Views are protected with `@permission_required` decorators.




# 📚 LibraryProject

LibraryProject is a beginner-friendly Django project created to manage and store information about books in a virtual library. This project is part of the **Alx_DjangoLearnLab** and serves as an introduction to Django's architecture, development environment, and workflow.

## 🛠️ Project Purpose

The goal of this project is to:
- Set up a Django development environment.
- Learn how to structure a Django project.
- Understand how to run and interact with the development server.
- Explore the default files Django provides.

## 📦 Features (To be Implemented)

- Add and store book information (title, author, publication date, etc.)
- View a list of all stored books.
- Search for books by title or author.
- Simple admin interface for managing the library.

## 🧱 Project Structure

