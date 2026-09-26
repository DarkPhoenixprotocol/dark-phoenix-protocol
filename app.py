"""
Dark Phoenix Protocol
Free, open-source image-to-video generator built for Hugging Face Spaces (ZeroGPU).
Model: engineerA314/Wan2.1-Fun-V1.1-1.3B-InP-Diffusers (Apache-2.0, based on Wan2.1)
No API key, no payment required -- runs on Hugging Face's free shared GPU pool.
"""

import os
import tempfile

import gradio as gr
import spaces
import torch
from diffusers import WanImageToVideoPipeline
from diffusers.utils import export_to_video

MODEL_ID = "engineerA314/Wan2.1-Fun-V1.1-1.3B-InP-Diffusers"
WIDTH = 832
HEIGHT = 480

ANIME_SUFFIX = ", anime style, cel shading, vibrant colors, smooth animation, high quality, detailed"
NEGATIVE_PROMPT = (
    "static, still, blurred, low quality, distorted, deformed, watermark, "
    "text, subtitles, extra limbs, bad anatomy, ugly, low resolution"
)

PHOENIX_CSS = """
:root {
    --phoenix-bg: #120604;
    --phoenix-panel: #1d0b06;
    --phoenix-ember: #ff5a1f;
    --phoenix-gold: #ffb020;
    --phoenix-crimson: #c81e3a;
    --phoenix-ink: #fff1e6;
}
.gradio-container {
    background: radial-gradient(circle at 20% 0%, rgba(200,30,58,0.25), transparent 45%),
                radial-gradient(circle at 85% 15%, rgba(255,176,32,0.18), transparent 40%),
                var(--phoenix-bg) !important;
    color: var(--phoenix-ink) !important;
}
#phoenix-title h1 {
    background: linear-gradient(120deg, var(--phoenix-gold), var(--phoenix-ember), var(--phoenix-crimson));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    font-weight: 800;
    letter-spacing: .02em;
}
.gr-button-primary, button.primary {
    background: linear-gradient(120deg, var(--phoenix-crimson), var(--phoenix-ember), var(--phoenix-gold)) !important;
    border: none !important;
    color: #1a0500 !important;
    font-weight: 700 !important;
}
.block, .form, .panel {
    background: var(--phoenix-panel) !important;
    border: 1px solid rgba(255,90,31,0.25) !important;
}
"""

print("Loading Wan2.1 image-to-video pipeline... this happens once at startup.")
pipe = WanImageToVideoPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16)
pipe.to("cuda")
print("Model loaded.")


@spaces.GPU(duration=120)
def generate_video(image, prompt, num_frames, seed):
    if image is None:
        raise gr.Error("Please upload an image first.")

    prompt = (prompt or "").strip()
    if not prompt:
        prompt = "gentle natural movement, subtle motion"
    full_prompt = prompt + ANIME_SUFFIX

    image = image.convert("RGB").resize((WIDTH, HEIGHT))

    generator = torch.Generator(device="cuda")
    seed = int(seed) if seed else 0
    if seed > 0:
        generator = generator.manual_seed(seed)

    output = pipe(
        image=image,
        prompt=full_prompt,
        negative_prompt=NEGATIVE_PROMPT,
        height=HEIGHT,
        width=WIDTH,
        num_frames=int(num_frames),
        num_inference_steps=30,
        guidance_scale=5.0,
        generator=generator,
    )

    out_path = os.path.join(tempfile.gettempdir(), "dark_phoenix_output.mp4")
    export_to_video(output.frames[0], out_path, fps=16)
    return out_path


with gr.Blocks(title="Dark Phoenix Protocol", css=PHOENIX_CSS) as demo:
    with gr.Column(elem_id="phoenix-title"):
        gr.Markdown(
            """
            # 🔥 Dark Phoenix Protocol
            Upload an anime-style image, describe the motion you want, and generate a short video.
            Powered by the free, open-source **Wan2.1** model -- runs on Hugging Face's free
            **ZeroGPU** pool. No API key, no payment needed.

            First run may take a minute or two while the Space wakes up and loads the model.
            """
        )

    with gr.Row():
        with gr.Column():
            image_input = gr.Image(label="Source image", type="pil")
            prompt_input = gr.Textbox(
                label="Describe the motion",
                placeholder="e.g. the character slowly blinks, hair blowing in the wind",
                lines=2,
            )
            with gr.Accordion("Advanced settings", open=False):
                frames_input = gr.Slider(
                    label="Number of frames (more = longer clip, slower generation)",
                    minimum=17,
                    maximum=49,
                    step=8,
                    value=33,
                )
                seed_input = gr.Number(label="Seed (0 = random)", value=0)
            generate_btn = gr.Button("Ignite the Video", variant="primary")

        with gr.Column():
            video_output = gr.Video(label="Result")

    generate_btn.click(
        fn=generate_video,
        inputs=[image_input, prompt_input, frames_input, seed_input],
        outputs=video_output,
    )

    gr.Markdown(
        """
        ---
        Free & open source. This runs on a shared free GPU pool, so if many people are using it
        at once you may see a queue -- that's normal, just wait or try again shortly.
        """
    )

demo.queue(max_size=20).launch()
