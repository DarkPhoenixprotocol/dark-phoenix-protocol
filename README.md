---
title: Dark Phoenix Protocol
emoji: 🔥
colorFrom: red
colorTo: yellow
sdk: gradio
sdk_version: 5.20.0
app_file: app.py
pinned: false
license: apache-2.0
---

# Dark Phoenix Protocol

A free, open-source image-to-video generator for anime-style art. Upload an image,
describe the motion, and get a short animated clip back. No API key, no payment --
built to run on Hugging Face's free **ZeroGPU** hardware.

Model used: [`engineerA314/Wan2.1-Fun-V1.1-1.3B-InP-Diffusers`](https://huggingface.co/engineerA314/Wan2.1-Fun-V1.1-1.3B-InP-Diffusers)
(Apache-2.0, based on Alibaba's open Wan2.1 video model).

## How to deploy this for free

### Step 1 -- Keep the code on GitHub
Push these three files (`app.py`, `requirements.txt`, `README.md`) to a GitHub
repository of your own, so you have version history and a backup.

### Step 2 -- Create a free Hugging Face Space
The actual video generation needs a GPU, which GitHub Pages cannot provide --
Hugging Face Spaces gives one for free instead:

1. Go to https://huggingface.co/new-space
2. Pick a name (e.g. `dark-phoenix-protocol`), choose **Gradio** as the SDK
3. Under **Space hardware**, select **ZeroGPU** (free tier, no card required for personal use)
4. Create the Space, then upload `app.py`, `requirements.txt`, and `README.md`
   (drag-and-drop in the "Files" tab, or `git push` -- a Space is just a git repo)

### Step 3 (optional) -- Auto-sync from your GitHub repo
If you want your GitHub repo to be the source of truth and auto-deploy to the
Space on every push, add this GitHub Actions workflow at
`.github/workflows/sync-to-hf.yml` in your GitHub repo:

```yaml
name: Sync to Hugging Face Space
on:
  push:
    branches: [main]
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Push to Hugging Face Space
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          git remote add space https://user:$HF_TOKEN@huggingface.co/spaces/YOUR_USERNAME/dark-phoenix-protocol
          git push --force space main
```

Replace `YOUR_USERNAME` with your Hugging Face username, and add a
`HF_TOKEN` secret in your GitHub repo settings (create the token at
https://huggingface.co/settings/tokens with "write" access).

## Design

The interface uses a "phoenix" color theme -- deep black-red background with
ember-orange and gold gradients -- defined via custom CSS inside `app.py`
(the `PHOENIX_CSS` variable). Edit the color variables at the top of that
block to adjust the palette.

## Notes

- This runs on a **shared** free GPU pool, so generation can take a few minutes
  and you may occasionally hit a queue during busy times.
- The 1.3B model is lighter and faster than the full 14B Wan2.1 model, which
  makes it a better fit for the free ZeroGPU quota -- quality is good but not
  at the level of paid services like Kling or Runway.
- Clips are short (about 1-3 seconds) at 480p. You can raise `num_frames` or
  resolution in `app.py`, but that increases generation time and may exceed
  the free GPU time limit per request.
