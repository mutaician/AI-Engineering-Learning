from google.adk.agents import SequentialAgent

from .sub_agents.validator import lead_validator_agent
from .sub_agents.scorer import lead_scorer_agent
from .sub_agents.recommender import action_recommender_agent

root_agent = SequentialAgent(
    name="LeadQualificationPipeline",
    description="A pipeline that validates, scores, and recommends actions for sales leads",
    sub_agents=[lead_validator_agent, lead_scorer_agent, action_recommender_agent]
)
