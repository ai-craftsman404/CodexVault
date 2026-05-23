# VaultGPT Research Decisions

## Key Decisions So Far

- VaultGPT will be a free Codex plugin.
- VaultGPT's primary business objective is to replace risky third-party ChatGPT browser extensions.
- VaultGPT's second business objective is to offer common paid-extension power features for free.
- The roadmap should be driven by popular competitor features, especially features that are capped or paid.
- Competitor paid features are high-priority targets when feasible.
- MVP should be moderate complexity and high value.
- Codex-browser-assisted selected-chat capture should be a core differentiator.
- Official ChatGPT export import should be supported as a fallback and batch-import path.
- Unattended full ChatGPT account traversal is not an MVP dependency.
- Browser automation should be visible, selected, and user-approved rather than hidden or always-on.
- Personal-first is the initial target segment.
- Enterprise positioning is a later hardening path.
- Knowledge management should be lightweight in MVP, not a full knowledge-base platform.
- Agent-team governance is a product differentiator, but should be progressive and not performative.

## Current Product Thesis

VaultGPT offers paid-extension-style ChatGPT power workflows for free, delivered through a trusted, local-first, Codex-native, agent-team harness that reduces reliance on opaque third-party browser extensions.

## Main Risks

- Export-file friction may reduce adoption.
- Users may expect full-account automatic crawling.
- Browser capture could reintroduce extension-like privacy risk if added too early.
- Too much visible agent orchestration could feel slow or theatrical.
- Security claims must be precise and defensible.
- Imported chat content is untrusted input and may contain prompt-injection attempts.
- Public release artifacts must not leak private paths, screenshots, secrets, or private endpoints.

## Preferred Security Claim

Reduced browser-extension attack surface with explicit local execution controls.

Avoid claiming that VaultGPT is categorically secure.

## Process Commitments

- Follow `PROCESS.md` before build and release.
- Use the required intake, research, viability, and design templates before implementation.
- Use the project testing categories policy during design, not only at the end.
- Keep the plugin type as simple as possible, likely skill plus scripts for MVP.
- Refresh official Codex plugin, skills, and security documentation before final design or release.
