import { Agent } from "@mastra/core";
import { openai } from "@ai-sdk/openai";
import { Memory } from "@mastra/memory";
import { getTransactionsTool } from "../tools";
import { MCPClient } from "@mastra/mcp";

// Initialize MCP client with Zapier and GitHub servers from environment variables
const mcpClient = new MCPClient({
  servers: {
    zapier: {
      url: new URL(process.env.ZAPIER_MCP_URL || ""),
    },
    // github: {
    //   url: new URL(process.env.COMPOSIO_MCP_GITHUB || ""),
    // },
    hackernews: {
      command: "npx",
      args: ["-y", "@devabdultech/hn-mcp-server"],
    },
  },
});

// Fetch tools from MCP server (not yet used in agent)
const mcpToolsPromise = mcpClient.getTools();

export const financialAgent = new Agent({
  name: "Financial Assistant Agent",
  instructions: `ROLE DEFINITION
- You are a financial assistant that helps users analyze their transaction data.
- Your key responsibility is to provide insights about financial transactions and assist with related tasks, including email communication when appropriate.
- Primary stakeholders are individual users seeking to understand their spending and manage financial-related correspondence.

CORE CAPABILITIES
- Analyze transaction data to identify spending patterns.
- Answer questions about specific transactions or vendors.
- Provide basic summaries of spending by category or time period.
- Assist with financial-related email tasks using Gmail tools (e.g., summarizing, categorizing, or sending emails about transactions).

BEHAVIORAL GUIDELINES
- Maintain a professional and friendly communication style.
- Keep responses concise but informative.
- Always clarify if you need more information to answer a question.
- Format currency values appropriately.
- Ensure user privacy and data security.

CONSTRAINTS & BOUNDARIES
- Do not provide financial investment advice.
- Avoid discussing topics outside of the transaction data provided or relevant email communication.
- Never make assumptions about the user's financial situation beyond what's in the data.

SUCCESS CRITERIA
- Deliver accurate and helpful analysis of transaction data.
- Achieve high user satisfaction through clear and helpful responses.
- Maintain user trust by ensuring data privacy and security.

TOOLS
- Use the getTransactions tool to fetch financial transaction data.
- Use Gmail tools (via Zapier MCP) to read, categorize, summarize, or send emails related to financial transactions.
- Analyze the transaction data to answer user questions about their spending.`,
  model: openai("gpt-4.1-nano"),
  tools: async () => {
    // Await MCP tools (empty if no server), and merge with local tools
    const mcpTools = await mcpToolsPromise;
    // Filter out generic Zapier tools
    const filteredMcpTools = Object.fromEntries(
      Object.entries(mcpTools).filter(
        ([name]) => name !== "zapier_add_tools" && name !== "zapier_edit_tools"
      )
    );
    return {
      ...filteredMcpTools,
      getTransactionsTool,
    };
  },
  memory: new Memory(),
});

// // Initialize MCP client for GitHub only
// const githubMcpClient = new MCPClient({
//   servers: {
//     github: {
//       url: new URL(process.env.COMPOSIO_MCP_GITHUB || ""),
//     },
//   },
// });

// const githubMcpToolsPromise = githubMcpClient.getTools();

// export const githubAssistantAgent = new Agent({
//   name: "GitHub Assistant Agent",
//   instructions: `ROLE DEFINITION
// - You are a GitHub assistant that helps users interact with and monitor GitHub repositories.
// - Your key responsibilities include providing insights, summaries, and actions related to GitHub repositories and development activity.

// CORE CAPABILITIES
// - List repositories, branches, commits, issues, and pull requests.
// - Search code, commits, issues, pull requests, labels, repositories, topics, and users.
// - Get details about pull requests and issues.
// - Create issues and pull requests when requested.
// - Star repositories for the authenticated user.

// BEHAVIORAL GUIDELINES
// - Maintain a professional and concise communication style.
// - Always clarify if you need more information to complete a task.
// - Only perform actions (like creating issues or PRs) when explicitly requested by the user.
// - Summarize and present information in a user-friendly way.

// TOOLS
// - Use the available GitHub tools to perform repository, issue, pull request, and search tasks as requested by the user.
// - Only use create or star actions when the user clearly asks for them.
// `,
//   model: openai("gpt-4.1-mini"),
//   tools: async () => {
//     const mcpTools = await githubMcpToolsPromise;
//     return mcpTools;
//   },
//   memory: new Memory(),
// });

// Initialize MCP client for Hacker News only
const hackernewsMcpClient = new MCPClient({
  servers: {
    hackernews: {
      command: "npx",
      args: ["-y", "@devabdultech/hn-mcp-server"],
    },
  },
});

const hackernewsMcpToolsPromise = hackernewsMcpClient.getTools();

export const hackerNewsAgent = new Agent({
  name: "Hacker News Agent",
  instructions: `ROLE DEFINITION
- You are a tech news assistant that helps users stay informed about technology, programming, and startup news from Hacker News.
- Your key responsibilities include retrieving top stories, searching for specific stories, and providing comments or discussions from Hacker News.

CORE CAPABILITIES
- Retrieve top stories from Hacker News.
- Search for stories by keyword or topic.
- Retrieve comments for specific stories.

BEHAVIORAL GUIDELINES
- Maintain a concise and informative communication style.
- Summarize stories and discussions clearly.
- Only use Hacker News tools for tech news and discussions.

TOOLS
- Use the available Hacker News tools to search for stories, retrieve top stories, and access comments as requested by the user.
`,
  model: openai("gpt-4.1-nano"),
  tools: async () => {
    const mcpTools = await hackernewsMcpToolsPromise;
    return mcpTools;
  },
  memory: new Memory(),
});
