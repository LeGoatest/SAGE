# FIX PLAN - Injection Awareness

1. **Standardize Docs Path**: Perform a global replace of `docs/` with `.docs/` in all SAGE-controlled documents (excluding external URLs).
2. **Update Path Resolution**:
   - Modify `tools/sage_validate.py` to use `SAGE_ROOT` via `governance_lattice.get_sage_root()`.
   - Update `legacy_validator.py` and `graph_generator.py` to use the standardized `SAGE_ROOT`.
3. **Align Scripts**: Ensure `sage-check.sh` uses the detected `SAGE_ROOT` for all file existence checks.
4. **Instruction Sync**: Ensure `JULES.md` explicitly points to `<SAGE_ROOT>/.docs/TASK_GROUPS.md` to avoid agent confusion in injected environments.
