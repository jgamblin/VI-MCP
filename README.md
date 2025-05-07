# VI+ MCP Server

The VI+ MCP Server is a Python-based application designed to fetch and format details about Common Vulnerabilities and Exposures (CVEs) using the Cisco CVM API. It provides a structured and readable summary of CVE data, including risk scores, exploitability, and fixes.

## Serving as an MCP Server in VS Code

To configure the VI+ MCP Server as an MCP server in VS Code, follow these steps:

1. Open your VS Code settings file (`settings.json`).
2. Add the following configuration under the `"mcp"` key:
    ```json
    "mcp": {
        "servers": {
            "VI+Bot": {
                "type": "stdio",
                "command": "python",
                "args": [
                    "/Github/VI-MCP/vi-mcp.py"
                ]
            }
        }
    }
    ```
3. Save the `settings.json` file.

### Notes
- Ensure Python is installed and accessible from your terminal.
- The `.env` file must be present in the project root and contain the required environment variables.
- Update the path `/Github/VI-MCP/vi-mcp.py` in the configuration to the correct path on your local system.
- If you encounter issues, verify that the path to `vi-mcp.py` is correct and that the file is executable.

For more information on configuring MCP servers in VS Code, refer to the [VS Code MCP Server Documentation](https://code.visualstudio.com/docs/copilot/chat/mcp-servers).

## Using MCPO for Serving to Open-WebUI

[Open-WebUI](https://docs.openwebui.com/) is a powerful platform that allows you to integrate and expose MCP-based tools through standard OpenAPI endpoints. By using the MCP-to-OpenAPI proxy (`mcpo`), you can make your MCP server accessible via REST APIs, enabling seamless integration with other tools, services, and workflows. Open-WebUI simplifies deployment, provides auto-generated OpenAPI documentation, and supports interactive exploration of your APIs.

For a detailed guide on getting started with Open-WebUI, refer to the [Getting Started with Open-WebUI](https://docs.openwebui.com/getting-started/) section.

### Why Use Open-WebUI with MCPO?

- **Standardized API Access**: Expose your MCP server as RESTful APIs, making it easier to integrate with existing systems.
- **Interactive Documentation**: Automatically generate OpenAPI documentation, accessible via a built-in Swagger UI.
- **Scalability and Security**: Leverage HTTP-based communication with robust authentication and scalability features.
- **Ease of Use**: Simplify the deployment process with minimal configuration and no need for custom clients.

To serve the VI+ MCP Server to Open-WebUI using the MCP-to-OpenAPI proxy (`mcpo`), follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd VI-MCP
   ```

2. Build the Docker image:
   ```bash
   docker build -t vi_mcp_server .
   ```

3. Run the MCP-to-OpenAPI proxy with the Docker container:
   ```bash
   uvx mcpo --port 8000 -- docker run -i --rm --env-file .env vi_mcp_server
   ```

4. Access the auto-generated OpenAPI documentation at:
   ```
   http://localhost:8000/docs
   ```

For more details on using MCPO with Open-WebUI, refer to the [Open-WebUI MCP Documentation](https://docs.openwebui.com/openapi-servers/mcp/).  
Learn more about the MCPO project on its [GitHub repository](https://github.com/open-webui/mcpo).

### Suggested Model for Open-WebUI

We recommend using the [Gemma 3:12B model](https://ollama.com/library/gemma3:12b) with MCP in Open-WebUI. This model is a highly capable multimodal model with a 128K context window, making it ideal for tasks like question answering, summarization, and reasoning. It supports over 140 languages and is optimized for deployment on resource-limited devices.

Key features of the Gemma 3:12B model:
- **Multimodal capabilities**: Processes both text and images.
- **Large context window**: 128K tokens for handling extensive input.
- **High performance**: Excels in reasoning, logic, and summarization tasks.
- **Compact design**: Runs efficiently on a single GPU.

For more information, visit the [Gemma 3:12B model page](https://ollama.com/library/gemma3:12b).

### System Prompt for Open-WebUI

The suggested system prompt for Open-WebUI is available in the [SystemPrompt.md](./SystemPrompt.md) file. This prompt provides detailed guidance for configuring the assistant to prioritize Cisco Risk Scores and provide actionable vulnerability insights.

### Environment Variables
Create a `.env` file in the project root with the following content:
```env
RISK_TOKEN="your_api_token_here"
```

## Testing

To test the API using the `vi-mcp-test.py` script:

1. Ensure the `.env` file is configured with your `RISK_TOKEN`.
2. Run the script:
   ```bash
   python3 vi-mcp-test.py
   ```
3. The script will fetch and display details for a hardcoded CVE ID (`CVE-2023-35078`).

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.