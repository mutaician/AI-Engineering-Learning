from google.adk.agents import LoopAgent, SequentialAgent

from .subagents.post_generator import initial_post_generator
from .subagents.post_refiner import post_refiner
from .subagents.post_reviewer import post_reviewer

# create refinement loop agent
refinement_loop = LoopAgent(
    name="PostRefinementLoop",
    max_iterations=10,
    sub_agents=[post_reviewer, post_refiner],
    description="Iteratively reviews and refines a Linkedin post until quality requirements are met"
)

root_agent = SequentialAgent(
    name="LinkedInPostGeneratorPipeline",
    sub_agents=[initial_post_generator, refinement_loop],
    description="Generate and refines a LinkedIn post through an iterative process"
)