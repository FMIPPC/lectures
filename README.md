# Parallel Programming for LLMs

The course moves from language model fundamentals through GPU programming,
parallelism, scaling, evaluation, data, and post-training.

## Lecture guide

Follow the lectures in order. Interactive lectures are recorded walkthroughs
you can step through in your browser; PDF lectures open slide decks. You do
not need to install anything or have a GPU to view them.

| Lecture | Topic | Materials |
| --- | --- | --- |
| 1 | Course overview and tokenization | [Interactive lecture](https://fmippc.github.io/lectures/?trace=lecture_01), [Python source](lecture_01.py) |
| 2 | Resource accounting | [Interactive lecture](https://fmippc.github.io/lectures/?trace=lecture_02), [Python source](lecture_02.py) |
| 3 | LM architecture and hyperparameters | [PDF slides](https://fmippc.github.io/lectures/lecture_03.pdf) |
| 4 | Attention alternatives and mixtures of experts | [PDF slides](https://fmippc.github.io/lectures/lecture_04.pdf) |
| 5 | GPUs | [PDF slides](https://fmippc.github.io/lectures/lecture_05.pdf) |
| 6 | GPU benchmarking, profiling, and Triton kernels | [Interactive lecture](https://fmippc.github.io/lectures/?trace=lecture_06), [Python source](lecture_06.py) |
| 7 | Multi-GPU parallelism | [Interactive lecture](https://fmippc.github.io/lectures/?trace=lecture_07), [Python source](lecture_07.py) |
| 8 | Parallelism basics | [PDF slides](https://fmippc.github.io/lectures/lecture_08.pdf) |
| 9 | Scaling laws: basics | [PDF slides](https://fmippc.github.io/lectures/lecture_09.pdf) |
| 10 | Inference | [Interactive lecture](https://fmippc.github.io/lectures/?trace=lecture_10), [Python source](lecture_10.py) |
| 11 | Scaling: case study and details | [PDF slides](https://fmippc.github.io/lectures/lecture_11.pdf) |
| 12 | Evaluation | [Interactive lecture](https://fmippc.github.io/lectures/?trace=lecture_12), [Python source](lecture_12.py) |
| 13 | Data I | [Interactive lecture](https://fmippc.github.io/lectures/?trace=lecture_13), [Python source](lecture_13.py) |
| 14 | Data II | [Interactive lecture](https://fmippc.github.io/lectures/?trace=lecture_14), [Python source](lecture_14.py) |
| 15 | After pretraining (mid-/post-training) | [PDF slides](https://fmippc.github.io/lectures/lecture_15.pdf) |
| 16 | Post-training II: reinforcement learning from verifiable rewards | [PDF slides](https://fmippc.github.io/lectures/lecture_16.pdf) |
| 17 | Multimodal models | [Interactive lecture](https://fmippc.github.io/lectures/?trace=lecture_17), [Python source](lecture_17.py) |

## Labs

Enrolled students may use computing resources at the Advanced Computing Center
at the University of Bucharest (ACC-UB) during scheduled labs. Instructors
will provide access details for those sessions.

## Executable lectures

These are named `lecture_XX.py`.

### Setup

Install `uv` and Node.js (with npm). From the repository root:

        uv sync
        git clone https://github.com/percyliang/edtrace
        git -C edtrace apply ..\edtrace-branding.patch
        npm --prefix=edtrace/frontend ci

On Windows, Git may check out `edtrace/frontend/public/var` and
`edtrace/frontend/public/images` as ordinary files instead of symlinks. If
they contain `../../../var` and `../../../images`, respectively, replace them
with directory junctions (PowerShell, from the repository root):

        Remove-Item .\edtrace\frontend\public\var, .\edtrace\frontend\public\images
        New-Item -ItemType Junction -Path .\edtrace\frontend\public\var -Target (Resolve-Path .\var).Path
        New-Item -ItemType Junction -Path .\edtrace\frontend\public\images -Target (Resolve-Path .\images).Path

### Record and view a lecture

From the repository root, record lesson 1 with:

        uv run python -X utf8 -m edtrace.execute -m lecture_01

This writes `var/traces/lecture_01.json` and caches downloaded images in
`var/files`.

To view the recording locally:

        npm --prefix=edtrace/frontend run dev

Open `http://localhost:5173/?trace=lecture_01` (or use the port shown by Vite
if 5173 is already in use).

Lectures 6 and 7 require Linux with CUDA-enabled PyTorch and Triton. On that
machine, record their viewer traces with:

        uv run python -X utf8 -m edtrace.execute -m lecture_06
        uv run python -X utf8 -m edtrace.execute -m lecture_07

The Lecture 7 viewer trace follows rank 0 and skips multiprocessing. To
regenerate the linked output from real multi-GPU execution, run it directly:

        uv run python -X utf8 lecture_07.py > var/traces/lecture_07_stdout.txt 2>&1

On CUDA machines, direct execution uses four GPUs when available, or two when
only two or three are visible. At least two visible GPUs are required.

To build for the main website from PowerShell at the repository root:

        $env:VITE_EDTRACE_BASE_DIR = "/lectures/"
        $env:VITE_EDTRACE_DIST_DIR = (Get-Location).Path
        npm --prefix=edtrace/frontend run build

Commit the generated `index.html` and `assets`, along with any updated traces
and cached images, before pushing.

The public lecture links above use GitHub Pages deployed from the `main`
branch's root directory.

## Non-executable lectures

These are named `lecture_XX.pdf`.

## Acknowledgments

This course adapts material from [Stanford CS336](https://cs336.stanford.edu/).

The hands-on GPU lectures and labs in this course are made possible by
high-performance computing resources and technical support from the Advanced
Computing Center at the University of Bucharest (ACC-UB).

For usage and access information, see the
[ACC-UB user guide](https://unibuc-dtd.github.io/advanced-computing-center-user-guide/).
