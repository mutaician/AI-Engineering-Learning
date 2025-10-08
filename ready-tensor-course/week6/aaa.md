# Agent Authoring Assistant system

- system that help authors have easy time writing and sharing AI projects

### key elements

A clear, compelling title
Relevant tags for search and discovery
A concise TL;DR summary
A visually engaging hero image
A handful of references to provide additional context

## Tag extraction Subsystem
- extract relevant tags

1. Gazetteer-based: A simple, rule-based method that scans the text for known terms from a predefined list (our gazetteer).
2. NER-based: A named entity recognition model using spaCy to extract proper nouns and technical terms from the text.
3. LLM-based: A prompt-driven method where the model suggests tags based on its understanding of the content.

* real-world systems aren't build made of agents
* they are composed of traditional ml models, rule-based components, business logic, and AI agentic AI layered where it makes sense

### implementation
A Start node that fans out to three parallel extraction methods:
One using a simple gazetteer lookup
One using spaCy’s NER model
One using an LLM-based extraction method
An Aggregation node that collects the results and uses an LLM to select the top n final tags.
An End node to close out the workflow.

### From Design to Decisions

## System Design and Architecture
What architectural pattern does this follow? - fan out fan graph , map-reduce pattern
Why did we use three extraction methods instead of one? - not everything needs to be a prompt. gazetter is fast and rule-based, spacy brings proven ML capabilities, LLM adds flexible reasoning
Why not just do everything in a single LLM call? - You'd lose control, explainability and reusability

## Agentic Thinking
How many agents did we use in this system? - 0, everything is deterministic and direct
So… is this even agentic? - yes but not "give the agent a goal and let it run"
Why didn’t we use agents to call the tools? - no real decision to make
If we didn’t use agents, why did we even create and register tools? - to leave the door open for more improvement and reusability

## LLMs, Tools & Reasoning
How many LLM-powered steps are there? - 2, extracting entities and aggregating from all methods 
What’s the role of reasoning in this system, if any? - llm based extractor doesn't need to understand what makes a good tag and that involves some reasoning

## Improvements & Production Readiness
Is this graph flexible? Could we swap components easily? - Yes 
What would it take to make this production-ready?: 
    Deduplication and normalization of tags
    Better handling of synonyms and variants (e.g. “AI” vs “artificial intelligence”)
    Thresholds or filters for relevance
    Human-in-the-Loop for tag validation
    Evaluation metrics to measure tag quality
What improvements could we try next?: 
    Use a multi-class text classifier to improve tag classification
    Try fine-tuning spaCy or adding your own gazetteer terms
    Add a verification step or reflection agent to improve tag quality
    Implement semantic de-duplication
    Experiment with reasoning strategies


