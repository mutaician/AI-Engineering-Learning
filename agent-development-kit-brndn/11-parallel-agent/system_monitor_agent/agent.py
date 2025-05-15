from google.adk.agents import ParallelAgent, SequentialAgent

from .sub_agents.cpu_info_agent import cpu_info_agent
from .sub_agents.disk_info_agent import disk_info_agent
from .sub_agents.memory_info_agent import memory_info_agent
from .sub_agents.synthesizer_agent import system_report_synthesizer

# --- 1. Create Parallel Agent to gather information concurrently ---
system_info_gatherer = ParallelAgent(
    name="system_info_gatherer",
    sub_agents=[cpu_info_agent, memory_info_agent, disk_info_agent],
)

# --- 2. Create Sequential Pipeline to gather info in parallel, then synthesize ---
root_agent = SequentialAgent(
    name="system_monitor_agent",
    sub_agents=[system_info_gatherer, system_report_synthesizer],
)