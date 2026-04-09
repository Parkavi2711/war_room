class CoordinatorAgent:
    """
    Coordinator Agent

    - Collects outputs from all agents
    - Extracts intent (Proceed / Pause / Roll Back) from agent analyses
    - Synthesizes a final, explainable decision
    """

    def synthesize(self, agent_outputs: list) -> dict:
        rationales = []
        decisions = []

        for output in agent_outputs:
            agent_name = output.get("agent", "Unknown")
            analysis_text = output.get("analysis", "")

            # Store rationale
            rationales.append({
                "agent": agent_name,
                "analysis": analysis_text
            })

            # Normalize analysis text
            analysis_lower = analysis_text.lower()

            # Detect decision intent
            if "roll back" in analysis_lower or "rollback" in analysis_lower:
                decisions.append("Roll Back")
            elif "pause" in analysis_lower:
                decisions.append("Pause")
            elif "proceed" in analysis_lower:
                decisions.append("Proceed")

        # Resolve final decision
        if "Roll Back" in decisions:
            final_decision = "Roll Back"
        elif decisions.count("Pause") >= 1:
            final_decision = "Pause"
        else:
            final_decision = "Proceed"

        # Confidence score (simple and defensible)
        confidence_score = round(
            len(decisions) / max(len(agent_outputs), 1),
            2
        )

        return {
            "decision": final_decision,
            "rationale": rationales,
            "confidence_score": confidence_score
        }