# multi_agent_system.py
import random
from typing import List

class Message:
    def __init__(self, sender_id: int, content: dict):
        self.sender_id = sender_id
        self.content = content

class Environment:
    def __init__(self):
        self.state = {
            "tasks": [random.randint(1, 10) for _ in range(5)],
            "completed": []
        }

    def get_state(self):
        return self.state

    def complete_task(self, agent_id, task_value):
        self.state["completed"].append((agent_id, task_value))
        self.state["tasks"].remove(task_value)

class Agent:
    def __init__(self, agent_id: int):
        self.agent_id = agent_id
        self.knowledge = {}
        self.inbox: List[Message] = []

    def perceive(self, env_state):
        self.knowledge["tasks"] = env_state["tasks"]

    def receive(self, messages: List[Message]):
        self.inbox.extend(messages)

    def communicate(self):
        if not self.knowledge.get("tasks"):
            return None
        chosen_task = min(self.knowledge["tasks"])
        return Message(self.agent_id, {"proposal": chosen_task})

    def decide(self):
        proposals = {}
        for msg in self.inbox:
            proposals[msg.sender_id] = msg.content["proposal"]
        self.inbox.clear()

        if not proposals:
            return None

        best_agent = min(proposals, key=lambda k: proposals[k])
        if best_agent == self.agent_id:
            return proposals[self.agent_id]
        return None

class Coordinator:
    def __init__(self, agents, env):
        self.agents = agents
        self.env = env

    def step(self):
        env_state = self.env.get_state()

        for agent in self.agents:
            agent.perceive(env_state)

        messages = []
        for agent in self.agents:
            msg = agent.communicate()
            if msg:
                messages.append(msg)

        for agent in self.agents:
            agent.receive(messages)

        for agent in self.agents:
            action = agent.decide()
            if action:
                print(f"Agent {agent.agent_id} executes task {action}")
                self.env.complete_task(agent.agent_id, action)
                break

def main():
    env = Environment()
    agents = [Agent(i) for i in range(3)]
    coordinator = Coordinator(agents, env)

    step = 0
    while env.state["tasks"]:
        print(f"\n=== Step {step} ===")
        print("Remaining tasks:", env.state["tasks"])
        coordinator.step()
        step += 1

    print("\nCompleted tasks:")
    print(env.state["completed"])

if __name__ == "__main__":
    main()
