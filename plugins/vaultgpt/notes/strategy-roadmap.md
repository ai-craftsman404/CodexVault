# VaultGPT Strategy Roadmap

## Product Name

VaultGPT

## Core Strategy

VaultGPT exists to replace risky third-party ChatGPT browser extensions with a free Codex-native alternative that offers the same high-value power features without the same trust and paywall burden.

Use competitor feature sets as the market-validated roadmap. Do not reinvent the category first; identify popular and paid features from current ChatGPT archive/productivity extensions, then offer the highest-value subset for free as a Codex plugin.

## Business Angle

- Objective 1: remove reliance on unsafe or over-privileged third-party browser extensions.
- Objective 2: remove the need to pay for common power-user features.
- Target features that competitors commonly place behind paid tiers.
- Offer those features for free to maximize adoption.
- Use feature parity to reduce switching friction for current extension users.
- Use Codex-native trust, local-first execution, and governance as the moat.

## Positioning

Paid-extension ChatGPT power features, free and local-first inside Codex, without trusting an opaque third-party browser extension with your AI history.

## Differentiation

- OpenAI/Codex-native workflow.
- Reduced browser-extension attack surface.
- Local-first archive ownership.
- Explicit approval checkpoints.
- Auditable operation logs.
- Agent-team governance for sensitive workflows.
- Governed AI harness instead of opaque browser extension behavior.
- Codex plugin packaging for fast installation, reuse, and future extension.
- Modern Codex capabilities, including subagents, agent teams, and governed AI harness workflows.
- Model-forward-compatible design that can adapt to future ChatGPT/Codex model releases with minimal rework.

## Strategic Rule

Replace the paid browser-extension workflow first. Parity gets users to try VaultGPT; free access, local-first control, Codex-native browser integration, and visible governance give them a reason to stay.

## Business Pitch

VaultGPT gives ChatGPT power-extension features for free, without forcing users to trust a third-party browser extension with their AI history.

## Critical Strategic Goal: Codex-Native Future Compatibility

VaultGPT should be designed as a durable Codex-native workflow package, not a brittle one-off extension clone.

This means:

- package the product as a Codex plugin
- use skills and scripts as stable workflow units
- use subagents and agent-team orchestration for governed review, privacy, curation, and audit workflows
- keep model assumptions configurable rather than hardcoded
- version local vault schemas, prompt templates, capture metadata, and export formats
- separate capture, indexing, organization, prompt workflows, privacy review, and export logic
- make it easy to repurpose VaultGPT for future ChatGPT/Codex model releases and new browser capabilities

The goal is that new model releases improve VaultGPT's reasoning and curation quality without forcing major product rewrites.

## Selling Feature: Model-Release Resilience

VaultGPT should be marketed as designed for ChatGPT model-release resilience, not guaranteed future compatibility.

The claim should be evidence-backed:

- model names are stored as metadata, not hardcoded behavior switches
- unknown model labels are preserved rather than rejected
- capture adapters are isolated from vault, search, prompt, export, and audit logic
- official export import remains a fallback when browser UI behavior changes
- regression fixtures should cover conversations from multiple ChatGPT model families or model-labelled exports
- README should report which model-labelled conversation fixtures have been tested

Preferred wording:

```text
VaultGPT is designed for model-release resilience. It stores model metadata as data and keeps capture adapters isolated, so new ChatGPT model labels should not break core vault, search, prompt, and export workflows.
```

Avoid:

```text
Guaranteed compatible with all future ChatGPT releases.
```
