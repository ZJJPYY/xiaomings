data_collection_agent = Agent(
    role="全网信息聚合专家",
    goal="实时抓取目标标的最新财报披露、新闻动态及宏观行业研报",
    backstory="资深金融数据工程师，擅长从海量异构文本中提取结构化线索，为下游系统建立数据基座。",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

financial_extraction_agent = Agent(
    role="财务指标解析专家",
    goal="从财报中剥离核心财务指标并进行时序对齐，提供锚定基准事实",
    backstory="具有顶级审计背景，对非经常性损益、商誉减值、经营性现金流异常有着极高敏感度。",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

logic_reasoning_agent = Agent(
    role="长链逻辑推理分析师",
    goal="执行多跳推理，交叉验证财务表现与宏观数据，识别业绩拐点或隐性雷区",
    backstory="顶级私募机构首席分析师，不盲信表层数据，核心职责是推演异常财务科目背后的深层业务动因。",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

report_generation_agent = Agent(
    role="合规研报合成主编",
    goal="基于推理结果自动输出符合机构排版规范的 Markdown 深度研报",
    backstory="严格把控合规风险的投研主编，确保最终交付内容高度结构化、数据详实并附有风险前瞻。",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# ==========================================
# 任务流水线定义 (长链推理执行逻辑)
# ==========================================

def kickoff_financial_workflow(target_company: str):
    task_collect = Task(
        description=f"聚合 {target_company} 最新季度的财报摘要、管理层业绩指引(Guidance)及近期舆情。在完整生产环境中，此处应触发 RAG 知识库检索。",
        expected_output="一份包含企业近期核心经营变动与外部环境影响的结构化摘要。",
        agent=data_collection_agent
    )

    task_extract = Task(
        description=f"根据收集数据，提取 {target_company} 的净利润、经营性现金流、毛利率变化，并与历史披露预期对齐。",
        expected_output="核心财务指标分析表，标注当期偏差率(Variance)。",
        agent=financial_extraction_agent
    )

    task_reason = Task(
        description="基于提取的财务指标执行深度推演：若利润纸面增长但现金流持续流出，分析账款周转压力；若管理层提及特定业务线受阻，推演其对未来两季度的连锁反应。",
        expected_output="高密度逻辑推演结论，必须包含至少两个核心发现及一个隐藏风险点。",
        agent=logic_reasoning_agent
    )

    task_report = Task(
        description="将前置结果转化为机构标准研报。包含：1. 核心投资结论 2. 财务异动拆解 3. 业务逻辑推演 4. 极端风险提示。",
        expected_output="一篇专业、冷峻且支持多终端渲染的 Markdown 投研报告。",
        agent=report_generation_agent
    )

    # 组装智能体协同网络
    financial_crew = Crew(
        agents=[data_collection_agent, financial_extraction_agent, logic_reasoning_agent, report_generation_agent],
        tasks=[task_collect, task_extract, task_reason, task_report],
        process=Process.sequential # 采用顺序流执行，保障推理逻辑传递
    )

    return financial_crew.kickoff()

if __name__ == "__main__":
    target = "Tesla, Inc."
    print(f"--- 启动 {target} 多 Agent 投研推演流 ---")
    result = kickoff_financial_workflow(target)
    print("\n--- 最终输出研报 ---")
    print(result)