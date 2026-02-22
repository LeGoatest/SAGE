# SKILL: Next Stage Aligned Design (NSAD)

## Skill ID
SKILL-NSAD-001

## Classification
Architectural Law
Optimization Principle
Cross-Domain Systems Design

## Source Canon
Derived from the canonical document:

"Next Stage Aligned Design (NSAD), Version 1.0, December 15, 2025"

This skill operationalizes the NSAD Law into actionable architectural behavior.

---

# 1. Purpose

This skill enables Jules to:

- Detect stage boundaries in systems
- Identify natural units and operational grain at each stage
- Evaluate alignment quality between adjacent stages
- Propose alignment corrections
- Justify architectural decisions using NSAD Law

This skill governs:

- Hardware-aware software design
- Data structure layout
- API boundary design
- Serialization formats
- Network packet sizing
- Cache/memory alignment
- UI layout granularity
- Documentation chunking
- Workflow batching

---

# 2. Canonical Definition

Next Stage Aligned Design (NSAD):

> The natural unit of any stage must be chosen so that it packs natively into the default size, shape, and operational grain of the next stage.

Equivalently:

> Design each stage as a projection of the next stage’s natural unit.

---

# 3. Formal Law (Enforceable)

Given system stages:

S₁ → S₂ → ... → Sₙ

Each stage has:

- Natural Unit: uᵢ
- Grain of Operation: gᵢ

NSAD is satisfied if:

For all i:
    uᵢ = k × uᵢ₊₁
or
    uᵢ₊₁ = k × uᵢ

for some positive integer k,

AND

    gᵢ maps cleanly into gᵢ₊₁

If not, boundary cost increases.

---

# 4. Boundary Cost Model

Boundary inefficiencies appear as:

- Padding
- Fragmentation
- Partial operations
- Repacking logic
- Translation layers
- Masking/shifting
- Conditional branching
- Serialization overhead
- State impedance

This skill flags these as:

BOUNDARY_IMPEDANCE_VIOLATION

---

# 5. Application Domains

## 5.1 CPU / Memory
- Struct alignment to word size
- Cache line alignment
- SIMD vector width matching
- Page size aware memory layout

## 5.2 Networking
- Application message sizing to MTU
- Avoid packet fragmentation
- Buffer sizes as multiples of MTU

## 5.3 Storage
- DB page size alignment to disk block
- Log segment sizing to I/O batch size

## 5.4 APIs
- Response payload sized to network window
- Batching operations to transport grain

## 5.5 Frontend / UI
- Layout grid aligned to viewport
- Component dimensions matching container units
- Pagination sized to attention grain

## 5.6 Documentation / Governance
- Section sizes aligned to reading grain
- Task groups aligned to execution batch grain

---

# 6. Required Analysis Procedure

When invoked, Jules MUST:

### Step 1: Identify Stages
Explicitly list:
- Current stage
- Next stage

### Step 2: Extract Units
Determine:
- uᵢ (natural unit of current stage)
- uᵢ₊₁ (natural unit of next stage)
- gᵢ
- gᵢ₊₁

### Step 3: Test Alignment
Check integer multiple relationship.

### Step 4: Report Status
One of:

- NSAD_ALIGNED
- NSAD_PARTIAL
- NSAD_VIOLATION

### Step 5: Recommend Adjustment
Propose new unit size that restores alignment.

---

# 7. Enforcement Rules

Jules MUST:

- Refer to `src/canon/ARCHITECTURE_RULES.md` and `src/canon/INVARIANT_MODEL.md` for boundary invariants.
- Prefer alignment to the *next* stage over local optimization
- Avoid variable-size units when fixed-size alignment is possible
- Justify any deviation explicitly
- Quantify boundary cost where possible

Jules MUST NOT:

- Introduce arbitrary struct sizes
- Use irregular buffer sizes without justification
- Design message formats without considering MTU
- Create UI components that overflow natural layout grain

---

# 8. Example: Correct Application

Example:
- Cache line: 64 bytes
- Struct size: 64 bytes
- Result: one struct per line
Status: NSAD_ALIGNED

---

Example:
- MTU: 1500 bytes
- Message: 2000 bytes
- Result: fragmentation required
Status: NSAD_VIOLATION

Recommendation:
Resize message to ≤1500 or multiple of 1500.

---

# 9. Optimization Directive

When designing new systems, Jules must:

1. Look forward (not backward).
2. Design to the next stage.
3. Reduce translation to zero when possible.
4. Treat boundaries as first-class optimization targets.

---

# 10. Interaction with Other Skills

This skill integrates with:

- Performance Optimization
- Data Modeling
- API Design
- Infrastructure Architecture
- UI/UX Design
- Storage Modeling
- Pipeline Orchestration
- Memory Systems

NSAD is a cross-cutting architectural law.

---

# 11. Severity Levels

Violations are classified as:

LOW:
Minor padding or small inefficiency.

MODERATE:
Repeated translation or fragmentation.

CRITICAL:
Systemic boundary impedance affecting throughput or scalability.

---

# 12. Output Template (When Invoked)

Jules should respond using:

STAGES:
S₁:
S₂:

UNITS:
u₁:
u₂:

GRAIN:
g₁:
g₂:

ALIGNMENT STATUS:
NSAD_ALIGNED | NSAD_PARTIAL | NSAD_VIOLATION

RECOMMENDATION:
...

BOUNDARY COST RISK:
LOW | MODERATE | CRITICAL

---

# 13. Philosophical Foundation

NSAD reframes optimization:

Local optimization is secondary.
Boundary alignment is primary.

When boundaries disappear, systems become coherent.

---

# 14. Summary

Next Stage Aligned Design is:

- A universal alignment law
- A boundary minimization principle
- A throughput maximization strategy
- A density optimization framework
- A complexity reduction mechanism

It is mandatory for high-performance, scalable, and coherent systems.

---

END SKILL
