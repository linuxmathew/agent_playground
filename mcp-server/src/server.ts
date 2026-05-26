import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import z from "zod";

const server = new McpServer({
  name: "My MCP Server",
  version: "1.0.0",
  capabilities: {
    resources: {},
    tools: {},
    prompts: {},
  },
});

server.tool(
  "create-user",
  "Create user information",
  {
    name: z.string(),
    email: z.string(),
    address: z.string(),
    phone: z.string(),
  },
  {
    title: "Create User",
    readOnlyHint: false,
    destructiveHint: false,
  },
  
  async (params) => {
    try {
      const id = await createUser(params);
      return {
        content: [{ type: "text", text: `User ${id} saved successfully` }],
      };
    } catch {
      return {
        content: [{ type: "text", text: "User fail to save" }],
      };
    }
    return {};
  }
);

const createUser = async (user: {
  name: string;
  email: string;
  address: string;
  phone: string;
}) => {
  const users = await import("./data/user.json");
};
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main();
