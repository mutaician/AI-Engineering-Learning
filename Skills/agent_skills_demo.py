import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

# List Anthropic-managed Skills
skills = client.beta.skills.list(
    source="anthropic",
    betas=["skills-2025-10-02"]
)

# for skill in skills.data:
#     print(f"{skill.id}: {skill.display_title}")

# # Create a message with the PowerPoint Skill
# response = client.beta.messages.create(
#     model="claude-sonnet-4-5-20250929",
#     max_tokens=4096,
#     betas=["code-execution-2025-08-25", "skills-2025-10-02"],
#     container={
#         "skills": [
#             {
#                 "type": "anthropic",
#                 "skill_id": "pptx",
#                 "version": "latest"
#             }
#         ]
#     },
#     messages=[{
#         "role": "user",
#         "content": "Create a presentation about AGI with 5 slides"
#     }],
#     tools=[{
#         "type": "code_execution_20250825",
#         "name": "code_execution"
#     }]
# )

# print(response.content)
# The response for powerpoint skill is in powerpoint-skill-respnse.txt

# # Extract file ID from response
# file_id = None
# for block in response.content:
#     if block.type == 'tool_use' and block.name == 'code_execution':
#         # File ID is in the tool result
#         for result_block in block.content:
#             if hasattr(result_block, 'file_id'):
#                 file_id = result_block.file_id
#                 break

# if file_id:
#     # Download the file
#     file_content = client.beta.files.download(
#         file_id=file_id,
#         betas=["files-api-2025-04-14"]
#     )

file_content = client.beta.files.download(
    file_id="file_011CWrXL4SDuHbY2QxV7o4Tx",
    betas=["files-api-2025-04-14"]
)
# Save to disk
with open("AGI.pptx", "wb") as f:
    file_content.write_to_file(f.name)

print(f"Presentation saved to AGI.pptx")