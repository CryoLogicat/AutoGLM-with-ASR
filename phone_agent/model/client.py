"""Model client for AI inference using OpenAI-compatible API."""

import json
import time
from dataclasses import dataclass, field
from typing import Any

from openai import OpenAI

from phone_agent.config.i18n import get_message


@dataclass
class ModelConfig:
    """Configuration for the AI model."""
    base_url: str = "https://api-inference.modelscope.cn/v1"
    api_key: str = "EMPTY"
    model_name: str = "Qwen/Qwen3.5-397B-A17B"
    max_tokens: int = 3000
    temperature: float = 0.0
    top_p: float = 0.85
    frequency_penalty: float = 0.2
    extra_body: dict[str, Any] = field(default_factory=dict)
    lang: str = "cn"


@dataclass
class ModelResponse:
    """Response from the AI model."""
    thinking: str
    action: str
    raw_content: str
    time_to_first_token: float | None = None
    time_to_thinking_end: float | None = None
    total_time: float | None = None


class ModelClient:
    """Client for interacting with OpenAI-compatible models."""

    def __init__(self, config: ModelConfig | None = None):
        self.config = config or ModelConfig()
        self.client = OpenAI(base_url=self.config.base_url, api_key=self.config.api_key)

    def request(self, messages: list[dict[str, Any]]) -> ModelResponse:
        start_time = time.time()
        time_to_first_token = None
        time_to_thinking_end = None
        first_token_received = False

        # 尝试开启各种模型的思考模式参数
        eb = dict(self.config.extra_body or {})
        eb.setdefault("enable_thinking", True)
        eb.setdefault("include_usage", True)

        stream = self.client.chat.completions.create(
            messages=messages,
            model=self.config.model_name,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
            frequency_penalty=self.config.frequency_penalty,
            extra_body=eb,
            stream=True,
        )

        raw_content = ""
        raw_reasoning = ""
        buffer = ""
        action_markers = ["finish(message=", "do(action="]
        in_action_phase = False

        for chunk in stream:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta

            # 1. 处理专门的推理字段 (reasoning_content)
            r_piece = getattr(delta, "reasoning_content", None) or getattr(delta, "reasoning", None)
            if r_piece:
                if not first_token_received:
                    time_to_first_token = time.time() - start_time
                    first_token_received = True
                raw_reasoning += str(r_piece)
                print(str(r_piece), end="", flush=True)

            # 2. 处理普通内容字段 (content)
            c_piece = getattr(delta, "content", None)
            if c_piece is not None:
                if not first_token_received:
                    time_to_first_token = time.time() - start_time
                    first_token_received = True
                
                raw_content += c_piece
                if in_action_phase:
                    continue

                buffer += c_piece
                marker_found = False
                for marker in action_markers:
                    if marker in buffer:
                        thinking_part = buffer.split(marker, 1)[0]
                        if thinking_part.strip():
                            print(thinking_part, end="", flush=True)
                        print()
                        in_action_phase = True
                        marker_found = True
                        time_to_thinking_end = time.time() - start_time
                        break
                
                if marker_found:
                    continue

                # 检查是否可能是 marker 的一部分，防止断字
                is_p = any(marker.startswith(buffer[-len(marker):]) for marker in action_markers)
                if not is_p:
                    print(buffer, end="", flush=True)
                    buffer = ""

        if buffer and not in_action_phase:
            print(buffer, end="", flush=True)

        total_time = time.time() - start_time
        thinking, action = self._parse_response(raw_content)
        
        # 如果有专门的推理内容，覆盖解析出来的 thinking
        if raw_reasoning.strip():
            thinking = raw_reasoning.strip()

        # 打印性能指标
        print(f"\n{'-'*50}\nTTFT: {time_to_first_token:.3f}s | Total: {total_time:.3f}s\n{'-'*50}")

        return ModelResponse(
            thinking=thinking,
            action=action,
            raw_content=raw_content,
            time_to_first_token=time_to_first_token,
            time_to_thinking_end=time_to_thinking_end,
            total_time=total_time,
        )

    def _parse_response(self, content: str) -> tuple[str, str]:
        """解析内容为 (思考, 动作)"""
        if "finish(message=" in content:
            p = content.split("finish(message=", 1)
            return p[0].strip(), "finish(message=" + p[1]
        if "do(action=" in content:
            p = content.split("do(action=", 1)
            return p[0].strip(), "do(action=" + p[1]
        if "<answer>" in content:
            p = content.split("<answer>", 1)
            t = p[0].replace("<think>", "").replace("</think>", "").strip()
            a = p[1].replace("</answer>", "").strip()
            return t, a
        return "", content


class MessageBuilder:
    @staticmethod
    def create_system_message(content: str):
        return {"role": "system", "content": content}

    @staticmethod
    def create_user_message(text: str, image_base64: str = None):
        c = []
        if image_base64:
            c.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}})
        c.append({"type": "text", "text": text})
        return {"role": "user", "content": c}

    @staticmethod
    def create_assistant_message(content: str):
        return {"role": "assistant", "content": content}

    @staticmethod
    def remove_images_from_message(msg: dict):
        if isinstance(msg.get("content"), list):
            msg["content"] = [i for i in msg["content"] if i.get("type") == "text"]
        return msg

    @staticmethod
    def build_screen_info(app: str, **extra):
        return json.dumps({"current_app": app, **extra}, ensure_ascii=False)
