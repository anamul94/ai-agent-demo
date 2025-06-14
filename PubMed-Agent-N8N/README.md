# PubMed Agent Powered by N8N
## Example of MCP Server Integration with n8n

This repository demonstrates how to integrate a custom MCP (Multi-Component Protocol) Server with **n8n**, enabling advanced workflows such as querying the **PubMed** API for biomedical research.

<!-- ## Overview
The workflows in this repository are designed to interact with the PubMed API, a comprehensive database of biomedical and life sciences literature. They enable users to search for specific literature, retrieve metadata, and perform various analyses on the retrieved data. -->

![alt text](<Screenshot from 2025-04-14 18-53-54.png>)

## Features
- **Search PubMed**: Search for literature using keywords, authors, or other criteria.
- **Retrieve Metadata**: Retrieve metadata for a specific literature.
- **Perform Analysis**: Perform various analyses on the retrieved data.

### Getting Started
To get started with these workflows, follow these steps:
1. **Clone the Repository**: Clone this repository to your local machine 
2. **Run MCP Server**: 
```bash
cd PubMedMCP
uv venv
source venv/bin/activate
uv install
python3 pubmed-mcp.py
```
2. **Import Workflow**: Import the workflow to your n8n workflow.

### Note: MCP client only available in self hosted version of n8n.Install MCP from settings