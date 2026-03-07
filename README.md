<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Unlicense License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Sovereign Agent Governance Engine (SAGE)</h3>

  <p align="center">
    A formalized contract-governed multi-plane execution constitution for AI coding agents.
    <br />
    <a href=".docs/canon/ARCHITECTURE_INDEX.md"><strong>Explore the docs »</strong></a>
    &middot;
    <a href=".docs/reference/SAGE_OVERVIEW.md">View Handbook</a>
    <br />
    <br />
    <a href="BOOTSTRAP.md">Bootstrap Project</a>
    &middot;
    <a href="NEW_PROJECT.md">New Project Guide</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#core-philosophy-sovereign-systems-axioms">Core Philosophy</a></li>
        <li><a href="#advanced-governance-layer">Advanced Governance Layer</a></li>
      </ul>
    </li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#repository-structure">Repository Structure</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

SAGE is an **operating doctrine** that provides a deterministic, repository-controlled governance framework. It establishes a clear separation between architectural authority and procedural execution.

### Core Philosophy: Sovereign Systems Axioms

The framework is built on six constitutional axioms defined in `.docs/canon/SYSTEM_AXIOMS.md`:

1.  **Rule Governance**: All behavior is constrained by explicit written rules.
2.  **Spec Primacy**: Specification always precedes execution.
3.  **Determinism**: Execution must produce identical results given the same canon and spec.
4.  **Replaceability**: Components are independently replaceable without system failure.
5.  **Sovereign Boundaries**: Each component owns its authority domain.
6.  **Contractual Communication**: Cross-boundary communication occurs only through explicit contracts.

### Advanced Governance Layer

Beyond basic mechanics, SAGE enforces sophisticated organizational invariants:
- **CONTRACT_MODEL.md**: Defines explicit interfaces for cross-plane communication.
- **INVARIANT_MODEL.md**: Documents core system truths that must be preserved.
- **MUTATION_PROCESS.md**: Establishes a formal process for constitutional/canon amendments.
- **VERSION_LOCKING.md**: Ensures stability and anchors execution to specific canon states.
- **STATE_MACHINE.md**: Definitive states and transitions for the Agent.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
The Canon Compiler requires `PyYAML`:
```sh
pip install -r requirements.txt
```

### Installation
To implement SAGE in your project:

1. Refer to [BOOTSTRAP.md](BOOTSTRAP.md) to initialize governance in an existing repository.
2. Follow [NEW_PROJECT.md](NEW_PROJECT.md) if starting from scratch.
3. Ensure your agent is configured to follow the instructions in `agents/Jules/JULES.md`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

SAGE defines a strict **Governance Hierarchy**. All work must comply with the hierarchy defined in `.docs/canon/ARCHITECTURE_INDEX.md`.

1.  **.docs/canon/ARCHITECTURE_RULES.md**: The supreme law of the project.
2.  **.docs/canon/SYSTEM_AXIOMS.md**: The philosophical invariants.
3.  **.docs/reference/SAGE_OVERVIEW.md**: The Handbook. Complete structural guide.
4.  **.docs/canon/SECURITY_MODEL.md**: The trust and safety boundary.
5.  **.docs/canon/INVARIANT_MODEL.md**: The immutability layer.
6.  **.docs/canon/CONTRACT_MODEL.md**: Cross-plane communication.
7.  **.docs/canon/ARCHITECTURE_INDEX.md**: The governance registry.
8.  **.docs/canon/MUTATION_PROCESS.md**: Protocol for changing the law.
9.  **.docs/canon/VERSION_LOCKING.md**: Anchoring to specific canon states.
10. **.docs/canon/DECISIONS.md**: Architectural record.
11. **.docs/canon/TERMINOLOGY.md**: Project glossary.
12. **.docs/canon/DOC_STYLE.md**: Documentation standards.
13. **.docs/canon/WDBASIC.md**: Frontend philosophy.
14. **.docs/governance/state-machine.md**: Deterministic agent states.
15. **.docs/governance/deep-governance-mode.md**: High-risk validation loop.
16. **agents/Jules/JULES.md**: Agent operating instructions.
17. **canon/task_groups.yaml**: Permission registry.
18. **skills/SKILLS_INDEX.md**: Procedural registry.
19. **SKILL.md files**: Approved playbooks.
20. **Spec files (.jtasks)**: Specific iteration work orders.

The Agent MUST refuse any request that violates the canon or implies undocumented architectural drift. **Refusal is a sign of system integrity.**

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- REPOSITORY STRUCTURE -->
## Repository Structure

- `.docs/` -> Human-readable narrative constitution and task groups.
- `canon/` -> Machine-enforceable governance layer (Rules, Semantic, Schemas).
- `.governance/` -> SAGE Constitutional Reasoning Engine and Validators.
- `agents/Jules/` -> Agent operating instructions and modes.
- `skills/` -> Procedural skills (compliant with `agentskills.io`).
- `tools/` -> Legacy validation tooling and vibe checks.
- `.jtasks/` -> Deterministic planning and execution records.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] SAGE v3.0 Multi-Zone Architecture
- [x] Deterministic Planning Protocol (.jtasks)
- [ ] Multi-Agent Coordination Protocol
- [ ] Automated Governance Auditing
- [ ] External Contract Verification

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are welcome! Please follow the rules defined in `CONTRIBUTING.md`.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the Unlicense License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/your_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/your_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/your_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/your_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/your_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/your_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/your_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/your_username/repo_name/issues
[license-shield]: https://img.shields.io/badge/license-Unlicense-blue.svg?style=for-the-badge
[license-url]: https://github.com/your_username/repo_name/blob/master/LICENSE
