import asyncio
import os
import subprocess
import sys
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import time

load_dotenv()



async def main():
    # Check if MCP server file exists

    server_file = "Email_client.py"
    if not os.path.exists(server_file):
        print(f"Error: MCP server file '{server_file}' not found!")
        return

    # Start the server as a background process
    print(f"Starting MCP server: {server_file}")
    server_process = subprocess.Popen(
        [sys.executable, server_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait briefly to ensure server is up before connecting
    time.sleep(2)


    try:
        print("MCP Client with Groq and FastMCP")
        print("="*41)
        print("Starting MCP client...")
        print(f"Connecting to server: {server_file}")
        
        async with streamablehttp_client("http://localhost:8989/mcp/") as (read, write, _):
            print("✅ Connected to MCP server")
            
            async with ClientSession(read, write) as session:
                print("⚙️  Initializing session...")
                await session.initialize()
                print("✅ Session initialized successfully")

                # Get tools from the MCP server
                print("🔧 Loading tools...")
                tools = await load_mcp_tools(session)
                
                if not tools:
                    print("❌ No tools loaded from MCP server")
                    return
                
                print(f"✅ Loaded {len(tools)} tools: {[tool.name for tool in tools]}")

                # Initialize Groq model
                groq_api_key = os.getenv("GROQ_API_KEY")
                if not groq_api_key:
                    print("❌ Error: GROQ_API_KEY environment variable not set!")
                    return
                
                llm = ChatGroq(
                    model="gemma2-9b-it",
                    temperature=0,
                    api_key=groq_api_key
                )
                
                # Create the ReAct agent
                agent = create_react_agent(llm, tools)
                
                # Interactive loop starts here
                print("\n" + "="*60)
                print("🤖 MCP weather Agent is Ready!")
                print("\n💡 Type 'quit' or 'q' to exit")
                print("="*60)
                
                # Main interactive loop
                while True:
                    try:
                        print("\n" + "-"*50)
                        # Get user input synchronously
                        user_question = input("🧮 Enter your math question: ").strip()
                        
                        # Check for exit
                        if user_question.lower() in ['q', 'quit', 'exit']:
                            print("👋 Goodbye!")
                            break
                        
                        if not user_question:
                            print("Please enter a question or 'q' to quit.")
                            continue
                        
                        print(f"\n🔍 Processing: {user_question}")
                        print("⏳ Please wait...")
                        
                        # Create message and process
                        messages = [HumanMessage(content=user_question)]
                        response = await agent.ainvoke({"messages": messages})
                        
                        # Display results
                        print("\n✨ Results:")
                        print("-" * 20)
                        
                        if 'messages' in response:
                            tool_results = []
                            final_answer = None
                            
                            for msg in response['messages']:
                                if hasattr(msg, 'content') and msg.content:
                                    if msg.__class__.__name__ == 'ToolMessage':
                                        tool_results.append(str(msg.content))
                                    elif msg.__class__.__name__ == 'AIMessage' and msg.content.strip():
                                        final_answer = msg.content.strip()
                            
                            # Show step-by-step if we have tool results
                            if tool_results:
                                print("📊 Calculation steps:")
                                for i, result in enumerate(tool_results, 1):
                                    print(f"   Step {i}: {result}")
                            
                            # Show final answer
                            if final_answer:
                                print(f"\n🎯 Final Answer: {final_answer}")
                            elif tool_results:
                                print(f"\n🎯 Final Answer: {tool_results[-1]}")
                            else:
                                print("🤔 Could not determine the answer")
                        
                    except KeyboardInterrupt:
                        print("\n\n👋 Interrupted by user. Goodbye!")
                        break
                    except Exception as e:
                        print(f"\n❌ Error: {str(e)}")
                        print("Please try again with a simpler question.")
                        
    except Exception as e:
        print(f"❌ Failed to start MCP client: {e}")
    finally:
        # Kill the server process when client exits
        if server_process.poll() is None:
            print("🛑 Stopping MCP server...")
            server_process.terminate()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram interrupted.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Small delay for cleanup on Windows
    import time
    time.sleep(0.1)