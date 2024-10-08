# Changelog

ProTaskinate changelog

This format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added

- User can now have one of the following roles for each project: `reader`, `writer`, `admin`
    - `reader` can view tasks, view project and comment to a task
    - `writer` can also create tasks and update/delete user's own tasks
    - `admin` can also update/delete all tasks and delete/update the project
- User can now view updated_at for all tasks user has access to
- User can now update the deadline of a task user has access to
- User can now addditionally view description, creator, role and creation date for all projects user has access to 

### Fixed

- Important buttons are now purple to fit the color scheme
- Page content has been divided into logical sections

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
