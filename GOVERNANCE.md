# Governance

**Status:** Interim (single maintainer). This will change as contributors join.

## Roles
| Role | Responsibility |
| --- | --- |
| **Maintainer** | Reviews and merges changes; decides on proposals until a maintainer group exists. Currently: the project founder. |
| **Contributor** | Anyone who opens an issue, a proposal or a pull request. |

## How decisions are made
- **Editorial changes** (typos, clarity, examples): any maintainer may merge.
- **Framework or spec changes** (new or changed practices, document kinds, resolution states, schema fields): open a proposal issue, allow at least 14 days for comment, then the maintainer decides and records the decision in the CHANGELOG.
- **Breaking spec changes** after v1.0 will require a new major version.

## Versioning
- The framework and the spec are versioned separately (`docs/` vs. `spec/`).
- Spec versions appear in every document's `osc:` field.

## Principles for the project
- Vendor-neutral: no document may require a commercial product.
- Interoperate before inventing: prefer referencing or contributing to existing open specs.
- Evidence before novelty: claims of contribution must point to the research landscape.

## Path forward
When there are enough independent contributors, the project intends to:
1. form a small maintainer group from at least two organizations;
2. consider contributing SMF to a neutral foundation (for example, the LF AI & Data Foundation's sandbox stage). This is an option, not a commitment.
