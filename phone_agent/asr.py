"""Realtime speech recognition client based on DashScope ASR."""

import signal
import time
from dataclasses import dataclass


@dataclass
class RealtimeASRConfig:
    """Configuration for DashScope realtime ASR."""

    model: str = "fun-asr-realtime"
    format: str = "pcm"
    sample_rate: int = 16000
    channels: int = 1
    block_size: int = 3200
    semantic_punctuation_enabled: bool = False
    api_key: str | None = None
    websocket_url: str | None = "wss://dashscope.aliyuncs.com/api-ws/v1/inference"


class RealtimeASRClient:
    """Realtime microphone ASR wrapper."""

    def __init__(self, config: RealtimeASRConfig | None = None):
        self.config = config or RealtimeASRConfig()

    def transcribe_once(self) -> str:
        """Start realtime recognition and stop by Ctrl+C."""
        try:
            import dashscope
            import pyaudio
            from dashscope.audio.asr import (
                Recognition,
                RecognitionCallback,
                RecognitionResult,
            )
        except ImportError as e:
            raise RuntimeError(
                "Missing dependencies. Please install: pip install dashscope pyaudio"
            ) from e

        if self.config.api_key:
            dashscope.api_key = self.config.api_key
        if self.config.websocket_url:
            dashscope.base_websocket_api_url = self.config.websocket_url

        state: dict[str, object] = {
            "mic": None,
            "stream": None,
            "sentences": [],
            "last_text": "",
            "request_id": "",
            "error": None,
            "stopping": False,
            "stopped": False,
        }

        class Callback(RecognitionCallback):
            def on_open(self) -> None:
                print("RecognitionCallback open.")
                mic = pyaudio.PyAudio()
                stream = mic.open(
                    format=pyaudio.paInt16,
                    channels=self_outer.config.channels,
                    rate=self_outer.config.sample_rate,
                    input=True,
                )
                state["mic"] = mic
                state["stream"] = stream

            def on_close(self) -> None:
                print("RecognitionCallback close.")
                stream = state.get("stream")
                mic = state.get("mic")
                if stream is not None:
                    try:
                        stream.stop_stream()
                    except Exception:
                        pass
                    try:
                        stream.close()
                    except Exception:
                        pass
                if mic is not None:
                    try:
                        mic.terminate()
                    except Exception:
                        pass
                state["stream"] = None
                state["mic"] = None

            def on_complete(self) -> None:
                print("RecognitionCallback completed.")

            def on_error(self, message) -> None:
                request_id = getattr(message, "request_id", "")
                msg_text = getattr(message, "message", "Unknown ASR error")
                print("RecognitionCallback task_id: ", request_id)
                print("RecognitionCallback error: ", msg_text)
                state["error"] = f"{request_id}: {msg_text}"

            def on_event(self, result: RecognitionResult) -> None:
                sentence = result.get_sentence()
                if isinstance(sentence, dict) and "text" in sentence:
                    text = str(sentence["text"]).strip()
                    if text:
                        print("RecognitionCallback text: ", text)
                        state["last_text"] = text
                    state["request_id"] = result.get_request_id()
                    if RecognitionResult.is_sentence_end(sentence):
                        if text:
                            state["sentences"].append(text)
                        print(
                            "RecognitionCallback sentence end, request_id:%s, usage:%s"
                            % (
                                result.get_request_id(),
                                result.get_usage(sentence),
                            )
                        )

        self_outer = self
        callback = Callback()

        recognition = Recognition(
            model=self.config.model,
            format=self.config.format,
            sample_rate=self.config.sample_rate,
            semantic_punctuation_enabled=self.config.semantic_punctuation_enabled,
            callback=callback,
        )

        def _stop_recognition() -> None:
            if state["stopped"]:
                return
            state["stopped"] = True
            recognition.stop()
            print("Recognition stopped.")
            print(
                "[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}".format(
                    recognition.get_last_request_id(),
                    recognition.get_first_package_delay(),
                    recognition.get_last_package_delay(),
                )
            )

        previous_handler = signal.getsignal(signal.SIGINT)

        def signal_handler(sig, frame):
            # Mark stopping first; main loop/finally will handle stop gracefully.
            print("Ctrl+C pressed, stop recognition ...")
            state["stopping"] = True

        signal.signal(signal.SIGINT, signal_handler)
        recognition.start()
        print("Press 'Ctrl+C' to stop recording and recognition...")

        try:
            while not state["stopping"]:
                stream = state.get("stream")
                if stream is None:
                    time.sleep(0.05)
                    continue
                data = stream.read(self.config.block_size, exception_on_overflow=False)
                try:
                    recognition.send_audio_frame(data)
                except Exception as e:
                    # Benign race: Ctrl+C may stop recognition while one more frame is sent.
                    if state["stopping"] and "stopped" in str(e).lower():
                        break
                    raise
                if state["error"]:
                    break
        except KeyboardInterrupt:
            state["stopping"] = True
        finally:
            signal.signal(signal.SIGINT, previous_handler)
            _stop_recognition()

        if state["error"]:
            raise RuntimeError(f"ASR failed: {state['error']}")

        text = " ".join(state["sentences"]).strip()
        if not text:
            text = str(state["last_text"]).strip()
        return text
