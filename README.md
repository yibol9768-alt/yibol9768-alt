# Hi, I’m Yibo Liu 👋

### AI agents · Evaluation · Research tools

I build tools to make AI agents **useful, inspectable, and measurable** — from retrieval and research workflows to reproducible benchmarks and interactive evaluation. I also contribute correctness fixes and regression tests to open-source LLM inference engines.

B.Sc. student in Information and Computing Science at **Beijing University of Posts and Telecommunications (BUPT)**, graduating in 2027. **Admitted to the master’s program at BUPT’s School of Computer Science, starting in 2027.** Open to remote AI / agent engineering and research internships.

[LinkedIn](https://www.linkedin.com/in/yibo-liu-aa327a44b/) · [Deep Research Arena](https://deepresearcharena.com) · [Play LLM Arcade](https://llm-arcade.pages.dev/)

---

## Merged open-source contributions

| Project | Contribution |
| :--- | :--- |
| **SGLang** | [**#44861 — Deterministic ModelOpt FP8 on SM12x**](https://github.com/sgl-project/sglang/pull/44861). Keep outputs batch-invariant across cold prefill and prefix-cache hits, with regression coverage for CUDA Graph replay and edge cases. **Merged.** |
| **vLLM** | [**#67469 — Bound warmup and CUDA Graph sizes**](https://github.com/vllm-project/vllm/pull/67469). Cap token counts to `max_num_seqs × max_model_len`, keeping dummy warmup batches within the real batch limit. **Merged.** |

[All merged public PRs](https://github.com/pulls?q=is%3Apr+author%3Ayibol9768-alt+is%3Amerged+is%3Apublic) · [Open public PRs](https://github.com/pulls?q=is%3Apr+author%3Ayibol9768-alt+is%3Aopen+is%3Apublic)

## Selected projects

| Project | What to explore |
| :--- | :--- |
| **[Deep Research Arena](https://github.com/yibol9768-alt/deep-research-arena)** | A team project for evaluating deep-research agents in controlled web sandboxes. Citation reachability and quote matching complement pairwise quality judgments and Bradley–Terry / Elo ranking. **[Live arena →](https://deepresearcharena.com)** |
| **[ScholarMind](https://github.com/yibol9768-alt/ScholarMind)** | A research-workflow application with nine modules, live progress updates, traceable execution, pause/resume controls, and human review. Built with **FastAPI, SQLAlchemy, WebSocket, React, and TypeScript**. |
| **[LLM Arcade](https://github.com/yibol9768-alt/llm-arcade)** | Playable artifacts for evaluating models and coding harnesses. Visitors can try the results, submit full rankings, and vote in anonymous A/B comparisons. **[Try the arcade →](https://llm-arcade.pages.dev/)** |
| **[ReadTimeMemory](https://github.com/yibol9768-alt/ReadTimeMemory)** | Core implementations for stateful agent memory, evidence retrieval and reranking, with recorded development results. Previously named `stateful-memory`; one project, one repository. |

More research code: [HybridAttn](https://github.com/yibol9768-alt/HybridAttn) · [CEDAR](https://github.com/yibol9768-alt/CEDAR).

## Engineering focus

**Python · PyTorch · FastAPI · asyncio · SQLAlchemy · React · TypeScript · Docker · Git**

My interests include agent evaluation, retrieval and grounding, research-workflow orchestration, and reliable tool/API integration. I care about reproducible results, clear failure modes, and interfaces that people can actually use.

---

**Looking for a collaborator or intern?** Reach out on [LinkedIn](https://www.linkedin.com/in/yibo-liu-aa327a44b/). I’m particularly interested in teams building AI agents, evaluation infrastructure, and research tools.
