import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# 实例化高参数量推理引擎 (对抗博弈需依赖复杂指令遵循能力)
llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

# ==========================================
# Agent 定义区 (红蓝对抗双子星架构)
# ==========================================

structuring_agent = Agent(
    role="跨语言结构化解析引擎",
    goal="将非结构化双语合同精准切片，建立中英文本的段落级映射对齐",
    backstory="专注于跨国法律文书解析的 NLP 专家，消除语言歧义，为下游博弈提供绝对客观的文本锚点。",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

red_legal_agent = Agent(
    role="法务合规审查专家 (红方)",
    goal="基于最新国际贸易法规，深度扫描并标注合同中隐藏的不对等条款及违约责任陷阱",
    backstory="顶尖跨国企业首席法务官，极其严苛。善于在管辖权、不可抗力及赔偿上限条款中揪出隐性风险。",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

blue_adversary_agent = Agent(
    role="交易对手模拟专家 (蓝方)",
    goal="模拟合同起草方(对手方)立场，对红方提出的修改意见进行逻辑反驳与压力测试",
    backstory="代表利益相对方的资深国际商业律师。运用商业惯例与法律豁免条款，精准反击红方的合规指控。",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

report_agent = Agent(
    role="风险定级与报告生成主编",
    goal="收敛红蓝双方的博弈共识，输出结构化的《合同风险定级与批注报告》",
    backstory="中立的风险控制官，不偏袒任何一方。只记录经过对抗验证的实质性风险，并给出最终修改建议。",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# ==========================================
# 对抗流水线定义 (包含博弈推演逻辑)
# ==========================================

def kickoff_legal_adversarial_workflow(contract_context: str):
    task_align = Task(
        description=f"解析以下双语合同片段，建立中英文条款对齐矩阵：\n{contract_context}",
        expected_output="段落级中英对照的结构化 JSON 格式数据。",
        agent=structuring_agent
    )

    task_red_scan = Task(
        description="【红方任务】审查对齐后的文本，提取出至少 3 个潜在的不对等条款（如单方面解约权、隐性违约金），并引用国际商法(CISG)给出修改批注。",
        expected_output="带有明确法律依据的风险条款清单及红方初步修改意见。",
        agent=red_legal_agent
    )

    task_blue_refute = Task(
        description="【蓝方任务】针对红方输出的风险清单进行逐条反驳。证明现有条款符合特定行业惯例，或指出红方修改意见在商业落地上的不合理性。",
        expected_output="针对红方意见的蓝方抗辩备忘录，需包含商业逻辑维度的施压。",
        agent=blue_adversary_agent
    )

    task_final_report = Task(
        description="审查红蓝双方的辩论记录。剔除无效抗辩，对最终确认的风险进行定级（高/中/低），输出最终决策报告。",
        expected_output="一份包含风险定级、对抗记录摘要及最终修订建议的 Markdown 格式审查报告。",
        agent=report_agent
    )

    # 组装红蓝对抗智能体网络
    legal_crew = Crew(
        agents=[structuring_agent, red_legal_agent, blue_adversary_agent, report_agent],
        tasks=[task_align, task_red_scan, task_blue_refute, task_final_report],
        process=Process.sequential
    )

    return legal_crew.kickoff()

if __name__ == "__main__":
    # 模拟一段有争议的跨语言合同输入
    sample_contract = """
    Party A holds the right to terminate this agreement at any time without prior notice.
    甲方有权随时终止本协议，且无需提前通知。
    Any dispute shall be submitted to the exclusive jurisdiction of the courts in [Party A's Country].
    任何争议应提交至【甲方所在国】法院专属管辖。
    """
    print("--- 启动跨语言对抗式审查流 ---")
    result = kickoff_legal_adversarial_workflow(sample_contract)
    print("\n--- 最终输出研报 ---")
    print(result)