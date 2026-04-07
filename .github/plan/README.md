# Plan Docs Maintenance

## Phase Tasklist Template Sync

Use the shared template and sync utility to keep all phase tasklist docs aligned.

- Template source: `.github/plan/_phase-task-template.md`
- Sync script: `.github/plan/sync_phase_task_templates.py`

### Check drift

```powershell
python .github/plan/sync_phase_task_templates.py
```

### Apply sync updates

```powershell
python .github/plan/sync_phase_task_templates.py --write
```

