# BigBrain Phase 11 Implementation Task List
<!-- PLAN:TEMPLATE v1 -->
<!-- PLAN:SOURCE .github/plan/_phase-task-template.md -->


## Goal

Add pluggable backends for distilled entities/relationships and vector retrieval so BigBrain can run beyond SQLite for larger deployments.

Target backends:
- PostgreSQL + pgvector
- Neo4j
- Qdrant
- Weaviate
- Pinecone

---

## Scope Boundaries

### In scope
- backend abstraction for distilled storage and retrieval
- PostgreSQL + pgvector implementation as the primary production backend
- connector implementations for Neo4j, Qdrant, Weaviate, and Pinecone
- config/schema updates for backend selection and credentials
- migration path from SQLite
- parity tests and benchmark harness

### Out of scope
- replacing SQLite as default local/dev backend
- cloud provisioning automation for all providers
- UI/dashboard work

---

## Recommended Implementation Order

1. Define storage interfaces and capability matrix
2. Implement PostgreSQL + pgvector backend
3. Add vector-store adapters (Qdrant, Weaviate, Pinecone)
4. Add graph adapter (Neo4j) for relationship-centric traversal
5. Add migration tooling and dual-write validation
6. Add test matrix and performance benchmark docs

---

## Workstream A - Backend Contracts

### Tasks
- [ ] Define `EntityStore` and `VectorStore` interfaces
- [ ] Define capability flags (filtering, hybrid search, graph traversal)
- [ ] Add backend selection config contract
- [ ] Add error taxonomy for backend failures

### Suggested files
- `src/bigbrain/kb/backends/base.py`
- `src/bigbrain/config.py`
- `config/example.yaml`

---

## Workstream B - PostgreSQL + pgvector

### Tasks
- [ ] Implement relational entity/relationship persistence
- [ ] Implement vector index and semantic retrieval
- [ ] Add migrations/bootstrap SQL
- [ ] Add integration tests for CRUD + ANN retrieval

### Suggested files
- `src/bigbrain/kb/backends/postgres_pgvector.py`
- `tests/test_kb_postgres_pgvector.py`

---

## Workstream C - Graph + Vector Connectors

### Tasks
- [ ] Implement Neo4j relationship adapter
- [ ] Implement Qdrant adapter
- [ ] Implement Weaviate adapter
- [ ] Implement Pinecone adapter
- [ ] Normalize metadata/provenance mapping across connectors

### Suggested files
- `src/bigbrain/kb/backends/neo4j_store.py`
- `src/bigbrain/kb/backends/qdrant_store.py`
- `src/bigbrain/kb/backends/weaviate_store.py`
- `src/bigbrain/kb/backends/pinecone_store.py`

---

## Workstream D - Pipeline Integration

### Tasks
- [ ] Route distill persistence through backend interfaces
- [ ] Route RAG retrieval through selected backend
- [ ] Preserve incremental distill semantics across backends
- [ ] Add backend-aware CLI diagnostics/status

### Suggested files
- `src/bigbrain/distill/pipeline.py`
- `src/bigbrain/rag/retriever.py`
- `src/bigbrain/cli.py`

---

## Workstream E - Migration, Validation, and Docs

### Tasks
- [ ] Add SQLite -> backend migration command(s)
- [ ] Add consistency checks (counts, hashes, spot-query parity)
- [ ] Add benchmark harness and baseline report
- [ ] Update README + AGENTS with backend setup guides

### Suggested files
- `src/bigbrain/kb/migrate.py`
- `tests/test_backend_migration.py`
- `docs/backends.md`

---

## Definition of Done for Phase 11

- [ ] backend interfaces are stable and documented
- [ ] PostgreSQL + pgvector backend is production-ready
- [ ] Neo4j, Qdrant, Weaviate, and Pinecone adapters are functional
- [ ] distill + RAG pipelines run with selectable backends
- [ ] migration from SQLite is validated
- [ ] benchmark and parity tests pass in CI matrix


---

## Recommended First Commit Slice

### Slice 0
- TODO
