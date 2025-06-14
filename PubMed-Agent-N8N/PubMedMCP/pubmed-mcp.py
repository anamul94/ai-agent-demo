from mcp.server.fastmcp import FastMCP
from langchain_community.tools.pubmed.tool import PubmedQueryRun

mcp = FastMCP("PubMed-MCP")


@mcp.tool(
    name="PubMed-Query-Tool",
    description="Query PubMed ",
)
def pubmed_query(query: str) -> str:
    """
    Query PubMed
    Args:
        query: The query to search PubMed
    """
    print(query)
    tool = PubmedQueryRun()
    return tool.run(query)


if __name__ == "__main__":
    mcp.run(transport="sse")
