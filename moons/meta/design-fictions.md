# Design Fictions as Agent Specifications

Design fictions — fictional scenarios where a non-existing idea becomes real — served a dual role in Saturn. They were created as speculative narratives for discussion (their traditional purpose), but empirically turned out to function as specification documents for LLMs. When Claude reads a design fiction, it doesn't interpret it as speculation. It treats it as a vision that can be broken down into implementable specs.

This was discovered, not planned. Joey fed the fictions to Claude and it just worked — the agent reverse-engineered the narratives into protocol requirements. No prior work has been found supporting this use of design fictions with LLMs.

## Characters

Three fictional characters and one corporation anchor Saturn's design fictions:

- **Derek** — software engineer, self-proclaimed "home network wizard." Represents a technically proficient integrator who has configured Saturn on their network. His scenarios defined the sysadmin experience.
- **Mira** — Derek's non-technical sister. Visits Derek's network and gets AI features (captions on a photo app) without paying or configuring anything. She just joined the network. Her scenarios defined the end-user experience and grounded the zero-config claim.
- **Jordan** — developer who leaked his company's API key from a Saturn server. His scenario directly inspired the beacon system: ephemeral keys provisioned on the network that expire after a short window. Created after Derek and Mira.
- **Megalink** — fictional corporation that created the system that becomes Saturn. Provides the corporate/deployment context.

## What the fictions produced

The three characters mapped directly to Saturn's three audience types (sysadmin, app developer, end user), which in turn drove:
- Different documentation sections (user guide vs. integrator guide)
- Different cognitive walkthrough personas in evaluation
- The understanding that Derek does more work so Mira does none (asymmetric complexity trade-off, Claim 2)

The fictions live in the `fiction/` directory of the Saturn GitHub repository.

## Methodological significance

Design fictions are established in HCI and debate. Their use as LLM specification input is novel — the author found no prior academic work supporting this practice. This makes it a methodological contribution worth documenting in the thesis appendix.
