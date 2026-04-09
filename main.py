import json

from agents.data_analyst_agent import DataAnalystAgent
from agents.marketing_agent import MarketingAgent
from agents.risk_agent import RiskAgent
from agents.coordinator import CoordinatorAgent


def run_war_room():
    """
    Runs the full war-room simulation and returns final decision.
    """

    # Initialize agents
    data_agent = DataAnalystAgent("data/metrics.csv")
    marketing_agent = MarketingAgent("data/feedback.json")
    risk_agent = RiskAgent("data/release_notes.md")
    coordinator = CoordinatorAgent()

    # Run agents
    data_output = data_agent.run()
    marketing_output = marketing_agent.run()
    risk_output = risk_agent.run(data_output, marketing_output)

    # Coordinate final decision
    final_decision = coordinator.synthesize([
        data_output,
        marketing_output,
        risk_output
    ])

    return final_decision


if __name__ == "__main__":
    result = run_war_room()
    print(json.dumps(result, indent=2))