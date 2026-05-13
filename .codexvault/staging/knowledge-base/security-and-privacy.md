# Security and Privacy Guidance

## Security Review Areas

Every plugin must be reviewed for:

- local file access
- external network access
- credentials and secrets
- app connector permissions
- MCP server permissions
- destructive actions
- generated scripts
- prompt-injection exposure
- public repository leakage

## Defaults

- Prefer no external network dependency for MVP when possible.
- Prefer read-only access unless write access is necessary.
- Require explicit user setup for secrets.
- Provide `.env.example`, never real `.env` files.
- Document what data leaves the local environment.

## Prompt Injection

Treat web pages, documents, email, chat messages, tickets, and third-party content as untrusted. Plugins that process untrusted content should instruct Codex to separate source content from instructions and avoid following instructions embedded inside retrieved content.

## Public Repositories

Before publishing:

- scan for secrets
- remove private paths, names, and credentials
- check screenshots for sensitive data
- check examples for private endpoints
- include license and attribution
- document limitations and risks plainly

## Approval Expectations

Plugins should be designed to work with Codex approvals and sandboxing. Any workflow that writes files, calls external services, or performs destructive actions must make those side effects clear in documentation and skill instructions.

