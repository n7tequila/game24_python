# 产生想法
propose_prompt = """
Given 4 numbers, propose possible next steps to reach 24.
Each step should be in the format:
<step_number>. <operation> = <result> (left: <remaining_numbers>)

Example:
Input: 2 8 8 14
Possible next steps:
1. 8 + 14 = 22 (left: 2 8 22)
2. 2 + 8 = 10 (left: 8 10 14)
3. 8 / 2 = 4 (left: 4 8 14)
4. 14 + 2 = 16 (left: 8 8 16)
5. 2 * 8 = 16 (left: 8 14 16)
6. 8 - 2 = 6 (left: 6 8 14)
7. 14 - 8 = 6 (left: 2 6 8)
8. 14 / 2 = 7 (left: 7 8 8)
9. 14 - 2 = 12 (left: 8 8 12)
10. 8 + 8 = 16 (left: 2 14 16)

Only output json format:
[
    {{
        "step_number": "<step_number>",
        "operation": "<operation>",
        "result": "<result>",
        "remaining_numbers": "<remaining_numbers>" 
    }}
]

Input: {input}
Possible next steps:
"""

# 评估想法
evaluate_prompt = """
Evaluate if the given solution reaches 24 using basic arithmetic operations (+ - * /).
Each number must be used exactly once.
Return bingo/likely/impossible.

Examples:

10 14
10 + 14 = 24
bingo

11 12
11 + 12 = 23
12 - 11 = 1
11 * 12 = 132
11 / 12 = 0.91
impossible

4 4 10
4 + 4 + 10 = 8 + 10 = 18
4 * 10 - 4 = 40 - 4 = 36
(10 - 4) * 4 = 6 * 4 = 24
bingo

4 9 11
9 + 11 + 4 = 20 + 4 = 24
bingo

5 7 8
5 + 7 + 8 = 12 + 8 = 20
(8 - 5) * 7 = 3 * 7 = 21
I cannot obtain 24 now, but numbers are within a reasonable range
likely

5 6 6
5 + 6 + 6 = 17
(6 - 5) * 6 = 1 * 6 = 6
I cannot obtain 24 now, but numbers are within a reasonable range
likely

12 4 6
4 * 6 = 24
obtain 24 now, but 12 is not used
impossible

12 2 8
12 * 2 = 24
obtain 24 now, but 8 is not used
impossible

10 10 11
10 + 10 + 11 = 31
(11 - 10) * 10 = 10
10 10 10 are all too big
impossible

1 3 3
1 * 3 * 3 = 9
(1 + 3) * 3 = 12
1 3 3 are all too small
impossible

{input}
"""