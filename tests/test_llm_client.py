import unittest
from unittest.mock import patch

from core import llm_client


class LlmClientTests(unittest.TestCase):
    @patch("core.llm_client.get_llm_settings", return_value=("http://localhost:1234", "Luna"))
    @patch("core.llm_client.get_llm_provider", return_value="openai")
    @patch("core.llm_client.requests.post")
    def test_text_call_uses_openai_endpoint(self, post, _provider, _settings):
        response = post.return_value
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "choices": [{"message": {"content": "hello"}}]
        }

        result = llm_client.call_llm_text("hi")
        self.assertEqual(result, "hello")
        self.assertEqual(post.call_args.args[0], "http://localhost:1234/v1/chat/completions")

    @patch("core.llm_client.get_llm_settings", return_value=("http://localhost:11434", "llama3.2"))
    @patch("core.llm_client.get_llm_provider", return_value="ollama")
    @patch("core.llm_client.requests.post")
    def test_text_call_reads_ollama_response(self, post, _provider, _settings):
        response = post.return_value
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "message": {"content": "hello"}
        }

        result = llm_client.call_llm_text("hi")
        self.assertEqual(result, "hello")
        self.assertEqual(post.call_args.args[0], "http://localhost:11434/api/chat")


    @patch("core.llm_client.get_llm_settings", return_value=("http://localhost:1234", "Luna"))
    @patch("core.llm_client.get_llm_provider", return_value="openai")
    @patch("core.llm_client.requests.post")
    def test_call_llm_normalizes_tool_calls(self, post, _provider, _settings):
        response = post.return_value
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "choices": [{
                "message": {
                    "content": "done",
                    "tool_calls": [{
                        "id": "call-1",
                        "function": {
                            "name": "click",
                            "arguments": "{\"x\": 10, \"y\": 20}"
                        }
                    }]
                }
            }]
        }

        result = llm_client.call_llm([{"role": "user", "content": "click"}])
        self.assertEqual(result["content"], "done")
        self.assertEqual(result["tool_calls"][0]["function"]["name"], "click")
        self.assertEqual(result["tool_calls"][0]["function"]["arguments"], {"x": 10, "y": 20})


    @patch("core.llm_client.get_llm_settings", return_value=("http://localhost:1234", "Luna"))
    @patch("core.llm_client.get_llm_provider", return_value="openai")
    @patch("core.llm_client.requests.post")
    def test_call_llm_handles_invalid_tool_arguments(self, post, _provider, _settings):
        response = post.return_value
        response.raise_for_status.return_value = None
        response.json.return_value = {"choices": [{"message": {"content": "", "tool_calls": [{"function": {"name": "x", "arguments": "{bad"}}]}}]}
        result = llm_client.call_llm([{"role": "user", "content": "x"}])
        self.assertEqual(result["tool_calls"][0]["function"]["arguments"], {})

if __name__ == "__main__":
    unittest.main()
