# Changelog

ProTaskinate changelog

This format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [v1.0.0] - 2024-10-15

### Added

- User can now have one of the following roles for each project: `reader`, `writer`, `admin`
    - `reader` can view tasks, view project and comment to a task
    - `writer` can also create tasks and update/delete user's own tasks
    - `admin` can also update/delete all tasks and delete/update the project
- User can now view updated_at for all tasks user has access to
- User can now update the deadline of a task user has access to
- User can now addditionally view description, creator, role, updated_at and created_at for all projects user has access to 
- User can now assign and de-assign roles for projects user has admin access to
- User can now create a project
- User can now view all tasks of project user has access to in a kanban board
- User can now view a project activity log if he has admin access to the project
    - Activity log shows task creation, task update, task deletion, task creation and project update
- User can view the amount of tasks assigned to the user in the dashboard

### Fixed

- Important buttons are now purple to fit the color scheme
- Page content has been divided into logical sections
- When a project is selected, the navbar shows navigations for that project
- Forms now show errors all at once instead of one by one
- Added length restrictions to most fields
- Datetimes are now displayed according to the user's timezone

## [v0.2.0-beta] - 2024-10-01

### Added

- User is able to register
- User is able to create a task with additional fields: assignee, deadline, and description
- User is able to view all tasks with the additional fields: assignee, deadline, and description
- User is able to additionally update the assignee of a task
- User is able to delete a task
- User is able to view a task's details by clicking on it
- User is able to view all projects and their tasks
- User is able to delete a project
- User is able to view a tasks comments
- User is able to add a comment to a task

### Fixed

- User can view active page in navbar
- Protaskinate has a more consistent look and feel
- Production database should no longer be flaky
- Improved error handling

## [v0.1.0-beta] - 2024-09-17

### Added

- User is able to login and logout
- User is able to create a new task with title, status and priority
- User is able to view title, status, priority, created_at and created_by for all tasks
- User is able to update priority and status of a task
