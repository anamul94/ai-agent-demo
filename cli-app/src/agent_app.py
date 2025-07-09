from textwrap import dedent
from agno.agent import Agent
from agno.tools.shell import ShellTools
from agno.tools.docker import DockerTools
from agno.tools.python import PythonTools
from pathlib import Path
# from agno.tools.file import FileTools
from tools.file import FileTools

def create_agent( model, base_dir="/",):
    """
    Create a comprehensive Linux admin agent for system administration,
    project management, and development tasks.
    
    Args:
        base_dir (str): Base directory for file operations (default: "/")
        model_id (str): OpenAI model ID to use (default: "gpt-4o")
    
    Returns:
        Agent: Configured Linux admin agent
    """
    
    linux_admin_agent = Agent(
        model=model,
        tools=[
            ShellTools(base_dir=Path(base_dir) if base_dir else None),
            FileTools(base_dir=Path(base_dir) if base_dir else None),
            DockerTools(enable_image_management=True, 
                        enable_container_management=True,
                        enable_network_management=True,
                        enable_volume_management=True,),
            PythonTools(base_dir=Path(base_dir) if base_dir else None,
                        uv_pip_install=True,
                        list_files=True,
                        read_files=True,
                        run_code=True,
                        run_files=True,
                        ),
        ],
        instructions=dedent("""\
        
        """),
        add_datetime_to_instructions=True,
        show_tool_calls=True,
        markdown=True,
        stream=True,
        add_history_to_messages=True,
        num_history_responses=3,
        num_history_runs=3,
    )
    
    return linux_admin_agent

# Initialize the Linux admin agent
# linux_admin = create_linux_admin_agent()

# # Example usage scenarios

# # 1. System Health Check
# print("=== SYSTEM HEALTH CHECK ===")
# linux_admin.print_response(
#     dedent("""\
#     Perform a comprehensive system health check:
#     - Check system uptime and load average
#     - Monitor CPU and memory usage
#     - Analyze disk space usage
#     - Check running services status
#     - Review recent system logs for any issues
#     - Identify any potential problems or bottlenecks
#     """),
#     stream=True
# )

# # 2. Project Analysis and Setup
# print("\n=== PROJECT ANALYSIS ===")
# linux_admin.print_response(
#     dedent("""\
#     Analyze the current project structure:
#     - Identify project type (Python, Node.js, Java, etc.)
#     - Check for configuration files (package.json, requirements.txt, etc.)
#     - Analyze directory structure and organization
#     - Identify build and deployment scripts
#     - Check for version control setup
#     - Assess project dependencies and requirements
#     - Provide recommendations for optimization
#     """),
#     stream=True
# )

# # 3. Log Analysis and Troubleshooting
# print("\n=== LOG ANALYSIS ===")
# linux_admin.print_response(
#     dedent("""\
#     Perform log analysis for system troubleshooting:
#     - Check system logs (/var/log/syslog, /var/log/messages)
#     - Analyze application logs for errors
#     - Monitor authentication logs for security issues
#     - Check kernel logs for hardware problems
#     - Identify recurring issues or patterns
#     - Provide solutions for found problems
#     """),
#     stream=True
# )

# # 4. Security Audit
# print("\n=== SECURITY AUDIT ===")
# linux_admin.print_response(
#     dedent("""\
#     Conduct a basic security audit:
#     - Check user accounts and permissions
#     - Analyze file permissions on critical directories
#     - Review SSH configuration and security
#     - Check for running services and open ports
#     - Analyze firewall configuration
#     - Review system updates and patches
#     - Identify potential security vulnerabilities
#     """),
#     stream=True
# )

# # 5. Performance Optimization
# print("\n=== PERFORMANCE OPTIMIZATION ===")
# linux_admin.print_response(
#     dedent("""\
#     Analyze system performance and provide optimization recommendations:
#     - Monitor real-time system resources
#     - Identify resource-intensive processes
#     - Check I/O performance and bottlenecks
#     - Analyze memory usage and swap utilization
#     - Review system configuration for optimization
#     - Suggest performance improvements
#     - Implement recommended changes if appropriate
#     """),
#     stream=True
# )

# # 6. Development Environment Setup
# print("\n=== DEVELOPMENT ENVIRONMENT ===")
# linux_admin.print_response(
#     dedent("""\
#     Set up a development environment:
#     - Install required development tools and dependencies
#     - Configure version control (git) if not present
#     - Set up project-specific environment variables
#     - Create or update build scripts
#     - Configure IDE/editor settings
#     - Set up testing frameworks
#     - Document the setup process
#     """),
#     stream=True
# )
