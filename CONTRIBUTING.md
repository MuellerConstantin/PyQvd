# How to Contribute

Thank you for your interest in contributing to **PyQVD**!

This document describes the contribution guidelines for the PyQVD project.  
It defines the rules for participation and explains how the project is organized and maintained.
By contributing to PyQVD, you agree to follow the processes and conventions outlined here to ensure a
consistent, high-quality, and collaborative development workflow.

## Semantic Versioning

PyQvd uses [Semantic Versioning](https://semver.org/) to manage its version numbers. Patch versions
address critical defects, minor versions add functionality or other non-breaking changes, and major
versions include breaking changes.

> [!NOTE]
> Dropping support for an end-of-life Python version is not considered a breaking change.
> As long as the public API remains unchanged, such support changes may be released in a minor version.
> This follows common practice in the Python ecosystem and is aligned with
> [PEP 440](https://peps.python.org/pep-0440/).

## Branch Organization

All active development for the upcoming version takes place on the `main` branch.  
We aim to keep `main` in a stable and releasable state at all times, with all tests passing.

As long as the project remains within the same major version, `main` represents the current and next minor
release. Changes merged into `main` must be compatible with the latest stable release and must not introduce
breaking changes. At any point, a new minor version can be released directly from the tip of `main`.

When development of a new major version begins, the current state of `main` for the previous major version is
branched off into a dedicated maintenance branch (for example, `release/v1`). This release branch is used for
continued development, bug fixes, and maintenance of the older, still-supported major version, while `main`
moves on to the next major version.

## Project Language

English is the official language of the project.

Please use English for:
- Source code (variable names, class names, function names)
- Code comments and documentation
- Commit messages
- GitHub issues, pull requests, and discussions

This ensures consistency and makes the project accessible to a wider, international audience.

## Bugs, Feature Requests, and Discussions

All communication related to bugs, feature requests, and project-related discussions is handled through
**GitHub Issues** in this repository.

Please open an issue to:
- Report a bug
- Propose a new feature or enhancement
- Discuss potential changes or improvements
- Ask questions related to the project’s behavior or roadmap

When reporting bugs, include as much relevant information as possible, such as the affected version, steps to
reproduce the issue, and expected versus actual behavior.

Feature requests should clearly describe the problem they aim to solve and, if possible, propose an approach
or use case. This helps maintainers evaluate the request and discuss potential solutions.

Using GitHub Issues as the central exchange format ensures transparency, traceability, and a shared
understanding of decisions and progress.

## Commit Messages

We follow a structured commit message convention inspired by the [Angular Commit Message Guidelines](https://github.com/angular/angular/blob/main/contributing-docs/commit-message-guidelines.md).
This helps keep our history readable, supports automated changelog generation, and ensures consistency
across contributions.

Each commit message consists of a header, a body, and a footer. See [Angular Commit Message Guidelines](https://github.com/angular/angular/blob/main/contributing-docs/commit-message-guidelines.md) for details.

```
<header>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

### Header

A typical commit message header consists of a **type**, optional **scope**, and a concise **description**,
for example:

```
<type>(<scope>): <short summary>
```

#### Type

In contrast to the Angular project, this project uses its own types. The following types are used:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests or correcting existing tests
- `build`: Changes that affect the build system or external dependencies
- `revert`: Reverts a previous commit
- `perf`: A code change that improves performance

#### Scope

The scope is an optional field that specifies the part of the application that is changed by this commit.
Most of the time, this may not be necessary. Possible values are: 

- `core`: The core functionality of the application
- `io`: I/O related changes

#### Short Summary

The short summary is a one-line description of the commit. It should use the imperative voice in the
present and not end with a period. It may not exceed 50 characters.

### Body

The body contains an optional more detailed description of the commit, typically including one up to
five short sentences. It should explain the main purpose of the change and any relevant background
information.

### Footer

The footer contains any additional information, such as breaking changes, references to issues, or
other relevant information.

## Sending a Pull Request

The maintainers actively review incoming pull requests. Each pull request will be reviewed and may be
merged, require changes, or be closed with an explanation.

Some changes, especially those affecting public APIs, may require additional internal adjustments
or further discussion, which can result in longer review times. We strive to provide timely feedback
and keep contributors informed throughout the review process.

To keep reviews efficient and changes easy to understand, pull requests should be as small and focused
as possible. Each pull request should address a single problem or concern. Unrelated changes (for example tooling changes or unrelated documentation updates) should be split into separate pull requests.

## License

Contributions to this project are made under the MIT License. By contributing to this project, you
consent to the terms of the license.
