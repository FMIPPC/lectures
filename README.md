# Spring 2026 CS336 lectures

This repository contains the lecture materials for Stanford's Language Modeling from Scratch (CS336).

## Executable lectures

These are named `lecture_XX.py`.

### Setup

Install `uv` and Node.js (with npm). From the repository root:

        uv sync
        git clone https://github.com/percyliang/edtrace
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

To build for the main website from PowerShell at the repository root:

        $env:VITE_EDTRACE_BASE_DIR = "/lectures/"
        $env:VITE_EDTRACE_DIST_DIR = (Get-Location).Path
        npm --prefix=edtrace/frontend run build

Commit the generated `index.html` and `assets`, along with any updated traces
and cached images, before pushing.

## Non-executable lectures

These are named `lecture_XX.pdf`.
