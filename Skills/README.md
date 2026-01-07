# Agent Skills 

- modular capabilities that extend claude's functionality
has instructions metadata and optional resources(scripts, templates)

#### Why 
skills are reusable filesystem-based resources that provide an agent with domain-specific expertise

#### Skill content

Level 1: Metadata (always loaded)
name + description in YAML 

Level 2: Instructions (loaded when triggered)
main body, has precedural knowledge - workflows, best practices and guidance 

Level 3: Resources and code (Loaded when needed)
instructions + code + resources

This repo seems to have a good examples: https://github.com/anthropics/skills/tree/main/skills 