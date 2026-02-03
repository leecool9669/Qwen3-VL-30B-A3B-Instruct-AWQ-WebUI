"""Qwen3-VL-30B-A3B-Instruct-AWQ WebUI（演示版）
默认 stub 模式，不加载模型，仅展示前端与输出格式。支持图片+文本输入。
"""
from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, List, Optional, Tuple

import gradio as gr


def _stub_vision_language(
    image: Optional[Any],
    user_text: str,
    system_prompt: str,
    max_new_tokens: int,
    temperature: float,
) -> Tuple[str, Dict[str, Any]]:
    has_image = image is not None
    answer = (
        "（演示输出：未加载真实模型权重）\n\n"
        "本界面用于展示 Qwen3-VL 视觉-语言模型的交互流程。"
        f"当前输入：{'图像 + 文本' if has_image else '仅文本'}。\n\n"
        f"用户问题：{user_text or '(未输入文字)'}\n\n"
        "示例回答（stub）：\n"
        "1）视觉编码：对输入图像进行特征提取与对齐；\n"
        "2）多模态融合：将视觉特征与文本 token 在统一空间中建模；\n"
        "3）自回归生成：基于上下文逐 token 生成回复。"
    )
    metrics = {
        "mode": "stub",
        "model_id": "Qwen3-VL-30B-A3B-Instruct-AWQ",
        "has_image": has_image,
        "max_new_tokens": max_new_tokens,
        "temperature": temperature,
        "ts_ms": int(time.time() * 1000),
    }
    return answer, metrics


def run_chat(
    chat_history: List[List[str]],
    image: Optional[Any],
    user_text: str,
    system_prompt: str,
    max_new_tokens: int,
    temperature: float,
) -> Tuple[List[List[str]], str, str]:
    chat_history = chat_history or []
    if not user_text.strip() and image is None:
        return chat_history, "", "{}"
    answer, metrics = _stub_vision_language(
        image=image,
        user_text=user_text.strip(),
        system_prompt=system_prompt.strip(),
        max_new_tokens=max_new_tokens,
        temperature=temperature,
    )
    prompt_display = "[图像 + 文本]" if image is not None else user_text
    chat_history = chat_history + [[prompt_display, answer]]
    return chat_history, "", json.dumps(metrics, ensure_ascii=False, indent=2)


def build_demo() -> gr.Blocks:
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="gray",
        font=["ui-sans-serif", "system-ui", "Segoe UI", "PingFang SC", "Microsoft YaHei"],
    )
    with gr.Blocks(title="Qwen3-VL-30B-A3B-Instruct-AWQ WebUI", theme=theme) as demo:
        gr.Markdown(
            "# Qwen3-VL-30B-A3B-Instruct-AWQ WebUI（演示）\n\n"
            "本界面用于**可视化展示**视觉-语言模型（VLM）的交互流程与结果。"
            "支持上传图片与文本输入，默认 **stub 模式**：不加载模型权重，仅展示前端与输出格式。"
        )
        with gr.Row(equal_height=True):
            with gr.Column(scale=5):
                chatbot = gr.Chatbot(label="对话记录", height=420)
                image_in = gr.Image(label="上传图片（可选）", type="filepath")
                user_text = gr.Textbox(
                    label="用户输入",
                    placeholder="输入问题或指令（可配合上方图片进行多模态问答）…",
                    lines=3,
                )
                run_btn = gr.Button("生成 / 推理", variant="primary")
                clear_btn = gr.Button("清空对话")
            with gr.Column(scale=4):
                gr.Markdown("## 推断配置\n本演示为 stub 模式，参数仅用于界面展示。")
                system_prompt = gr.Textbox(
                    label="系统指令",
                    value="你是一个多模态助手，能够理解图像与文本并给出准确、有帮助的回答。",
                    lines=2,
                )
                max_new_tokens = gr.Slider(16, 1024, value=256, step=1, label="max_new_tokens")
                temperature = gr.Slider(0.0, 2.0, value=0.7, step=0.05, label="temperature")
                metrics_out = gr.Code(label="运行指标（JSON）", value="{}", language="json")
        run_btn.click(
            fn=run_chat,
            inputs=[chatbot, image_in, user_text, system_prompt, max_new_tokens, temperature],
            outputs=[chatbot, user_text, metrics_out],
        )
        user_text.submit(
            fn=run_chat,
            inputs=[chatbot, image_in, user_text, system_prompt, max_new_tokens, temperature],
            outputs=[chatbot, user_text, metrics_out],
        )
        clear_btn.click(fn=lambda: ([], "{}"), inputs=[], outputs=[chatbot, metrics_out])
        gr.Markdown("### 说明\n本 WebUI 仅提供界面与 stub 输出，不会自动下载或加载模型。")
    return demo


if __name__ == "__main__":
    os.environ.setdefault("GRADIO_ANALYTICS_ENABLED", "False")
    build_demo().launch(server_name="127.0.0.1", server_port=int(os.environ.get("PORT", "7865")))
