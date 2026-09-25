# H100 lecture runs

This repository is public. Replace the SSH placeholders locally; do not commit
the server address, account names, SSH keys, or credentials.

## Connect from Windows PowerShell

SSH key authentication and a verified host key were already configured when
these runs were made. Use the account that can see four H100 GPUs:

```powershell
$gpuTarget = "<four-gpu-user>@<gpu-host>"
ssh -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=yes $gpuTarget
```

The commands below run in the **remote Linux shell** after connecting. Check
that four GPUs are visible and idle before starting a distributed run:

```bash
nvidia-smi --query-gpu=index,name,memory.total,memory.used,utilization.gpu --format=csv,noheader
```

## Environment

The four-GPU run used `~/lectures-four-gpu-5b41f7c`, an isolated checkout of
`FMIRL/lectures`. That checkout already has a `.venv` with Python 3.12,
`edtrace==0.1.15`, and CUDA-enabled `torch==2.11.0`. For a *new* account or
checkout, choose an unused directory and set it up with:

```bash
git clone --depth 1 https://github.com/FMIRL/lectures.git ~/lectures-h100
cd ~/lectures-h100
python3 -m venv .venv
.venv/bin/python -m pip install --disable-pip-version-check edtrace==0.1.15 torch==2.11.0
.venv/bin/python -m pip check
```

For a new checkout, substitute `~/lectures-h100` for
`~/lectures-four-gpu-5b41f7c` in the remaining commands.

Use the existing checkout instead of cloning again when repeating the original
run:

```bash
cd ~/lectures-four-gpu-5b41f7c
.venv/bin/python -m pip check
.venv/bin/python - <<'PY'
import torch

assert torch.cuda.device_count() == 4
assert torch.ones(2, device="cuda:3").sum().item() == 2
print(torch.__version__, torch.version.cuda, [torch.cuda.get_device_name(i) for i in range(4)])
PY
```

No Modal GPUs were used. The remote host did not have `uv`, so the runs used
the virtual environment's Python directly. `pip install .` does not work for
this repository's virtual project; install its dependencies as shown above.

## Record the four-GPU Lecture 7 demonstration

Run the Python file directly, **not** `edtrace.execute`, to exercise NCCL and
multiple processes. Run only one copy at a time: the lecture uses port 15623
on localhost for process-group setup.

```bash
cd ~/lectures-four-gpu-5b41f7c
tmp=$(mktemp var/traces/lecture_07_stdout.XXXXXX.tmp)
if .venv/bin/python -X utf8 lecture_07.py > "$tmp" 2>&1; then
    mv "$tmp" var/traces/lecture_07_stdout.txt
else
    tail -n 50 "$tmp"
    echo "Run failed; full output is in $tmp" >&2
    exit 1
fi
```

With four visible GPUs, the collective, data-parallel, and tensor-parallel
examples use ranks 0 through 3. The pipeline example intentionally uses only
two ranks. The previously published two-GPU fallback is used only when two or
three GPUs are visible.

We checked the result with:

```bash
.venv/bin/python - <<'PY'
from pathlib import Path

output = Path("var/traces/lecture_07_stdout.txt").read_text()
assert "world_size=4" in output
for operation in ("[all_reduce]", "[reduce_scatter]", "[data_parallelism]", "[tensor_parallelism]"):
    for rank in range(4):
        assert f"{operation} Rank {rank}:" in output
print("Four-rank Lecture 7 output is complete")
PY
```

This was an execution and output check, not a `pytest` test suite. The
four-GPU result is the linked `var/traces/lecture_07_stdout.txt` from commit
`9ab4d85`.

## Viewer traces and copying results back

The viewer JSON traces were recorded earlier on a separate GPU login (use the
same SSH options with that login's account placeholder), from its checkout at
`~/lectures-gpu-traces-fd546bb`:

```bash
cd ~/lectures-gpu-traces-fd546bb
CUDA_VISIBLE_DEVICES=0 .venv/bin/python -X utf8 -m edtrace.execute -m lecture_06
CUDA_VISIBLE_DEVICES=0 .venv/bin/python -X utf8 -m edtrace.execute -m lecture_07
```

Lecture 6 uses one GPU. Lecture 7's viewer trace intentionally runs rank 0
without multiprocessing; using four GPUs does not improve either JSON trace.
Both traces were checked to contain steps and the current embedded `.py`
source:

```bash
.venv/bin/python - <<'PY'
import json
from pathlib import Path

for module in ("lecture_06", "lecture_07"):
    source = Path(f"{module}.py")
    trace = json.loads(Path(f"var/traces/{module}.json").read_text())
    assert trace["steps"] and trace["steps"][-1]["stack"]
    assert trace["files"][source.name] == source.read_text()
    print(module, len(trace["steps"]), "steps")
PY
```

These viewer traces were published in commit `58f6e6b`. Lecture 6 also
generates `var/triton_gelu-ptx.txt`; inspect it for absolute compiler paths
before publishing it.

From **local PowerShell** at the repository root, copy the new distributed
output from the four-GPU login, then review and publish that file:

```powershell
$gpuTarget = "<four-gpu-user>@<gpu-host>"
scp -o BatchMode=yes -o StrictHostKeyChecking=yes "${gpuTarget}:lectures-four-gpu-5b41f7c/var/traces/lecture_07_stdout.txt" .\var\traces\lecture_07_stdout.txt
git diff --check
git add -- var\traces\lecture_07_stdout.txt
git commit -m "Record Lecture 7 distributed output on four H100s"
git push origin main
```
