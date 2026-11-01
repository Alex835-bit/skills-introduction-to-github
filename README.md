# Multi-Agent 协同决策系统

## 核心痛点
- 单Agent决策瓶颈
- 信息孤岛
- 动态环境适应差
- 扩展性不足

## 核心逻辑流
感知 → 通信 → 协同决策 → 执行

### 多Agent协作
- Proposal机制
- 冲突消解（最优任务优先）

### 是否包含长链推理
当前版本不包含长链推理，属于多轮短链协同决策

## 运行方式
```bash
python multi_agent_system.py
```
