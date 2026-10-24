# RethinkMCTS Trace Viewer

Local, read-only web viewer for saved search artifacts. It shows the persisted
search tree and ordered events for a selected run/model/dataset/problem. It does
not call an LLM, execute generated candidates, or modify benchmark artifacts.

Run from the project root:

```powershell
.\venv\Scripts\python.exe -m tools.trace_viewer.server
```

Open <http://127.0.0.1:8765>. Stop with `Ctrl+C`.

The viewer reads `outputs/rethinkmcts/<run>/<model>/<dataset>/<problem>/`.
The current event log records events such as selection, expansion, evaluation,
Rethink, LLM request metadata and completion. It can only display information
that was persisted by that run; missing per-step detail is not reconstructed.
