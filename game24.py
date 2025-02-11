import re
from collections import deque
from typing import List, Set, Dict, Optional

import yaml
from openai import OpenAI

import game24_prompts as prompts


class Game24Solver:

    def __init__(self):
        with open("config.yaml", encoding='utf-8') as file:
            config = yaml.safe_load(file)
            self.client = OpenAI(
                base_url=config['ai']['endpoint'],
                api_key=config['ai']['api_key']
            )

            # 模型配置修正（使用正确参数名）
            self.model_params = {
                "model": config['ai']['model'],
                "temperature": 0,
                "max_tokens": 512,
                "stream": False,
            }


    def solve(self, numbers: List[int]) -> Dict:
        print(f"开始求解 24 点: {numbers}")

        queue = deque([{
            "numbers": numbers,
            "steps": []
        }])

        visited: Set[str] = set()

        while queue:
            current = queue.popleft()
            numbers_key = ",".join(map(str, sorted(current["numbers"])))

            if numbers_key in visited:
                print(f"跳过重复组合：{numbers_key}")
                continue
            visited.add(numbers_key)

            self._print_current_state(current)

            if len(current["numbers"]) <= 3:
                # 修正参数传递
                eval_result = self._evaluate_state(
                    current["numbers"],
                    current["steps"]  # 添加steps参数
                )
                if eval_result:
                    return eval_result

            print("寻找下一步想法...")
            next_steps = self._generate_proposals(current["numbers"])
            print(f"提出{len(next_steps)}个可能的想法：")
            for i, step in enumerate(next_steps, 1):
                print(f"  {i}. {step['operation']} = {step['result']} (剩余: {' '.join(map(str, step['remaining']))})")

            for step in next_steps:
                queue.append({
                    "numbers": step["remaining"],
                    "steps": current["steps"] + [step["operation"]]
                })

        return {"success": False, "reason": "No solution found"}

    def _generate_proposals(self, numbers: List[int]) -> List[Dict]:
        prompt = self._create_propose_prompt(numbers)
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                **self.model_params
            )
            return self._parse_proposals(response.choices[0].message.content)
        except Exception as e:
            print(f"API Error: {str(e)}")
            return []

    def _evaluate_state(self, numbers: List[int], steps: List[str]) -> Optional[Dict]:
        """评估当前数字状态"""
        print("对想法进行可行性评估...")

        prompt = self._create_evaluate_prompt(numbers)
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                **self.model_params
            )
            reason = response.choices[0].message.content
        except Exception as e:
            print(f"API Error: {str(e)}")
            return None

        # 修正打印格式
        print_reason = (reason
                        .replace("\\(", "(")
                        .replace("\\)", ")")
                        .replace("\\times", "*")
                        .replace("/", "÷")
                        .replace("\\[", "[")
                        .replace("\approx", "≈"))
        print(f"评估过程：\n{print_reason}")

        if "BINGO" in reason.upper():
            print("😄 找到确定解法！")
            return {
                "success": True,
                "steps": steps,
                "reason": reason,
                "final": numbers
            }
        elif "IMPOSSIBLE" in reason.upper():
            print("该组合无法得到24，跳过")
            return None

    def _print_current_state(self, current: Dict) -> None:
        """打印当前状态信息"""
        print(f"当前的想法：{' '.join(map(str, current['numbers']))}")
        if current["steps"]:
            print(f"已执行步骤：{' -> '.join(current['steps'])}")

    def _parse_proposals(self, proposal_text: str) -> List[Dict]:
        steps = []
        lines = proposal_text.split("\n")
        pattern = re.compile(
            r"^\d+\.\s*.+?((\d+)\s*[+\-*/]\s*(\d+))\s*=\s*(\d+).+?\s*\(left:\s*(.+)\)",
            re.IGNORECASE | re.MULTILINE
        )
        while lines:
            line = lines.pop(0)
            for match in pattern.finditer(line):
                try:
                    steps.append({
                        "operation": match.group(1).strip(),
                        "result": int(match.group(4)),
                        "remaining": list(map(int, match.group(5).replace(',', ' ').split()))
                    })
                except ValueError:
                    continue

        return steps

    def _create_evaluate_prompt(self, numbers: List[int]) -> str:
        """创建评估模板"""
        return prompts.evaluate_prompt.format(input={" ".join(map(str, numbers))})

    def _create_propose_prompt(self, numbers: List[int]) -> str:
        """创建提议提示模板"""
        return prompts.propose_prompt.format(input={" ".join(map(str, numbers))})