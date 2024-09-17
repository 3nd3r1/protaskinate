<h1 align="center">ProTaskinate</h1>

<p align="center">
    <a href="https://codecov.io/gh/3nd3r1/protaskinate" > 
     <img src="https://codecov.io/gh/3nd3r1/protaskinate/graph/badge.svg?token=RtLrKFFSOO"/> 
    </a>
    <a href="https://github.com/3nd3r1/protaskinate/actions/workflows/main.yml" > 
     <img src="https://github.com/3nd3r1/protaskinate/actions/workflows/main.yml/badge.svg"/> 
    </a>
</p>

<p align="center">
<strong>ProTaskinate</strong> is a project management tool (like Jira) designed to help teams efficiently manage tasks, projects, and deadlines.
</p>

<p align="center">
    <a href="https://protaskinate-page.host.ender.fi/">Live Demo</a>
    .
    <a href="https://github.com/3nd3r1/protaskinate/releases/latest">Latest Release</a>
</p>

## Key Features:
- **Task Management**: Create, assign, and track tasks with due dates, priorities, and progress statuses.
- **Kanban Board**: Visualize and manage tasks across different stages (To Do, In Progress, Done).
- **Project Organization**: Organize tasks within specific projects for better clarity and tracking.
- **User Roles**: Assign roles (Admin/User) with different access permissions.
- **Comments and Collaboration**: Leave comments on tasks for better communication between team members.
- **Activity Log**: Track task updates and project changes in real time.
- **Visualization**: Easily create charts (E.g. burndown chart) to visualize your project.

## Tech Stack:
- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Frontend**: HTML/CSS/JavaScript

## Running Locally:

### With Docker:
1. Clone the repository:
```bash
git clone https://github.com/3nd3r1/protaskinate.git
cd protaskinate
```
2. Run docker-compose:
```bash
docker compose up
```

### Without Docker:
1. Clone the repository:
```bash
git clone https://github.com/3nd3r1/protaskinate.git
cd protaskinate
```
2. Install dependencies:
```bash
poetry install
```

3. Update the `.env` file with your database credentials:
4. Generate a secret key:
```bash
poetry run invoke generate-secret-key
```
5. Create schema and populate the database:
```bash
poetry run invoke create-schema
peotry run invoke populate-db
```
6. Run the application in development mode:
```bash
poetry run invoke dev
```
7. Open your browser and navigate to `http://localhost:5000`

## Weekly Report

### Välipalautus 2 - 2024-09-17

The project is progressing well. Testing has not yet been started so the coverage is poor. The project has a good structure and the code is clean. Many core features have been completed, more information can be found in the [changelog](docs/changelog.md). The project is available in production on [protaskinate-page.host.ender.fi](https://protaskinate-page.host.ender.fi/).
