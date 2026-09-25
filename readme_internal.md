# H100 lecture runs

This repository is public. Replace the SSH placeholders locally; do not commit
the server address, account name, or SSH credentials.

## Connect from Windows PowerShell

We used a configured SSH key and verified host key, with the account that can
see four H100s:

```powershell
$gpuTarget = "<four-gpu-user>@<gpu-host>"
ssh -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=yes $gpuTarget
```

## Run Lecture 7 on the server

The prepared checkout is `~/lectures-four-gpu-5b41f7c`. Its `.venv` has
Python 3.12, CUDA-enabled `torch==2.11.0`, and `edtrace==0.1.15`. In the
remote Linux shell, confirm four GPUs are visible and idle, then run:

```bash
cd ~/lectures-four-gpu-5b41f7c
nvidia-smi --query-gpu=index,name,memory.used,utilization.gpu --format=csv,noheader
.venv/bin/python -c 'import torch; assert torch.cuda.device_count() == 4'
tmp=$(mktemp var/traces/lecture_07_stdout.XXXXXX.tmp)
if .venv/bin/python -X utf8 lecture_07.py > "$tmp" 2>&1; then
    mv "$tmp" var/traces/lecture_07_stdout.txt
else
    tail -n 50 "$tmp"
    exit 1
fi
```

Run one copy at a time (process-group port 15623). This records real
four-rank NCCL, data-parallel, and tensor-parallel output; the pipeline
example still uses two ranks.

## Check the output

```bash
.venv/bin/python - <<'PY'
from pathlib import Path

output = Path("var/traces/lecture_07_stdout.txt").read_text()
assert "world_size=4" in output
for operation in ("[all_reduce]", "[reduce_scatter]", "[data_parallelism]", "[tensor_parallelism]"):
    assert all(f"{operation} Rank {rank}:" in output for rank in range(4))
print("Four H100 ranks recorded")
PY
```

This was a lecture run and output check, not a `pytest` suite. The Lecture 6
and 7 viewer JSON traces were recorded separately using one H100 each;
neither benefits from four GPUs. No Modal run was used.
