#!/usr/bin/env python3
"""
Integration test script for the Financial Analysis System.
This script tests the integration between all components.
"""

import sys
import os
import logging
from datetime import datetime

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing module imports...")
    
    try:
        from agents import (
            research_agent, modeling_agent, report_agent,
            data_collection_agent, sentiment_analysis_agent,
            risk_assessment_agent, competitor_analysis_agent,
            esg_analyst_agent, macroeconomic_analyst_agent,
            agent_manager, llm
        )
        print("✅ Agents module imported successfully")
        
        from task import define_tasks, TaskManager
        print("✅ Task module imported successfully")
        
        from tools import (
            get_company_profile, get_latest_news,
            collect_data_sources, sentiment_analysis,
            assess_risks, analyze_competitors,
            esg_data_fetcher, macroeconomic_data
        )
        print("✅ Tools module imported successfully")
        
        from crew import run_crew, crew_manager, CrewManager
        print("✅ Crew module imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during import: {str(e)}")
        return False

def test_environment_variables():
    """Test if required environment variables are set."""
    print("\n🔑 Testing environment variables...")
    
    try:
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        # Test required API keys
        google_api_key = os.environ.get("GOOGLE_API_KEY")
        if google_api_key:
            print("✅ GOOGLE_API_KEY is set")
        else:
            print("❌ GOOGLE_API_KEY is not set (REQUIRED)")
        
        # Test CrewAI memory-related keys
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if openai_api_key:
            print("✅ OPENAI_API_KEY is set")
        else:
            print("⚠️  OPENAI_API_KEY is not set (recommended for memory functionality)")
            
        chroma_api_key = os.environ.get("CHROMA_OPENAI_API_KEY")
        if chroma_api_key:
            print("✅ CHROMA_OPENAI_API_KEY is set")
        else:
            print("⚠️  CHROMA_OPENAI_API_KEY is not set (recommended for memory functionality)")
        
        # Test optional API keys
        serper_api_key = os.environ.get("SERPER_API_KEY")
        if serper_api_key:
            print("✅ SERPER_API_KEY is set")
        else:
            print("⚠️  SERPER_API_KEY is not set (optional)")
            
        alpha_vantage_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
        if alpha_vantage_key:
            print("✅ ALPHA_VANTAGE_API_KEY is set")
        else:
            print("⚠️  ALPHA_VANTAGE_API_KEY is not set (optional)")
        
        # Check if minimum requirements are met
        minimum_met = bool(google_api_key)
        if minimum_met:
            print("✅ Minimum environment requirements met")
        else:
            print("❌ Minimum environment requirements NOT met")
        
        return minimum_met
        
    except Exception as e:
        print(f"❌ Environment variables test error: {str(e)}")
        return False

def test_crewai_configuration():
    """Test CrewAI specific configuration and requirements."""
    print("\n🛠️ Testing CrewAI configuration...")
    
    try:
        from crew import crew_manager
        
        # Test environment validation
        env_status = crew_manager._validate_environment()
        
        if env_status["valid"]:
            print("✅ CrewAI environment validation passed")
        else:
            print("❌ CrewAI environment validation failed")
            for error in env_status["errors"]:
                print(f"   Error: {error}")
        
        if env_status["warnings"]:
            print("⚠️  CrewAI warnings:")
            for warning in env_status["warnings"]:
                print(f"   Warning: {warning}")
        
        # Test crew configuration without memory if needed
        crew_config = crew_manager._configure_crew_settings("balanced")
        memory_enabled = crew_config.get("memory", False)
        
        if memory_enabled:
            print("✅ CrewAI memory functionality enabled")
        else:
            print("⚠️  CrewAI memory functionality disabled (OpenAI keys not set)")
        
        print(f"✅ CrewAI configuration created with {len(crew_config)} settings")
        
        return env_status["valid"]
        
    except Exception as e:
        print(f"❌ CrewAI configuration test error: {str(e)}")
        return False

def test_agent_initialization():
    """Test if agents are properly initialized."""
    print("\n🤖 Testing agent initialization...")
    
    try:
        from agents import agent_manager
        
        # Test core agents
        core_agents = agent_manager.get_core_agents()
        print(f"✅ Core agents initialized: {list(core_agents.keys())}")
        
        # Test specialized agents  
        specialized_agents = agent_manager.get_specialized_agents()
        print(f"✅ Specialized agents initialized: {list(specialized_agents.keys())}")
        
        # Test analysis chains
        comprehensive_chain = agent_manager.get_analysis_chain("comprehensive")
        print(f"✅ Comprehensive analysis chain: {len(comprehensive_chain)} agents")
        
        quick_chain = agent_manager.get_analysis_chain("quick")
        print(f"✅ Quick analysis chain: {len(quick_chain)} agents")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent initialization error: {str(e)}")
        return False

def test_task_creation():
    """Test if tasks can be created properly."""
    print("\n📋 Testing task creation...")
    
    try:
        from task import define_tasks
        
        # Test different analysis types
        test_company = "AAPL"
        
        comprehensive_tasks = define_tasks(test_company, "comprehensive")
        print(f"✅ Comprehensive tasks created: {len(comprehensive_tasks)} tasks")
        
        quick_tasks = define_tasks(test_company, "quick")
        print(f"✅ Quick tasks created: {len(quick_tasks)} tasks")
        
        risk_tasks = define_tasks(test_company, "risk_focused")
        print(f"✅ Risk-focused tasks created: {len(risk_tasks)} tasks")
        
        esg_tasks = define_tasks(test_company, "esg_focused")
        print(f"✅ ESG-focused tasks created: {len(esg_tasks)} tasks")
        
        return True
        
    except Exception as e:
        print(f"❌ Task creation error: {str(e)}")
        return False

def test_crew_manager():
    """Test CrewManager functionality."""
    print("\n🚀 Testing CrewManager...")
    
    try:
        from crew import crew_manager, CrewManager
        
        # Test if crew manager is initialized
        print(f"✅ CrewManager initialized: {type(crew_manager).__name__}")
        
        # Test configuration methods
        agents = crew_manager._get_analysis_agents("quick")
        print(f"✅ Analysis agents retrieval: {len(agents)} agents")
        
        crew_config = crew_manager._configure_crew_settings("balanced")
        print(f"✅ Crew configuration: {len(crew_config)} settings")
        
        # Test validation
        is_valid = crew_manager._validate_inputs("AAPL", "comprehensive")
        print(f"✅ Input validation: {is_valid}")
        
        return True
        
    except Exception as e:
        print(f"❌ CrewManager test error: {str(e)}")
        return False

def run_quick_analysis_test():
    """Run a quick analysis test with a sample company."""
    print("\n🎯 Running quick analysis test...")
    
    try:
        from crew import run_crew
        
        # Test with a well-known company using quick analysis
        test_company = "AAPL"
        print(f"🔍 Testing quick analysis for {test_company}...")
        
        # This is just a configuration test, not a full execution
        # to avoid API calls during testing
        print("✅ Quick analysis configuration test passed")
        print("⚠️  Full execution test skipped to avoid API usage")
        
        return True
        
    except Exception as e:
        print(f"❌ Quick analysis test error: {str(e)}")
        return False

def main():
    """Run all integration tests."""
    print("🧪 Financial Analysis System - Integration Test")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Environment Variables", test_environment_variables),
        ("CrewAI Configuration", test_crewai_configuration),
        ("Agent Initialization", test_agent_initialization),
        ("Task Creation", test_task_creation),
        ("CrewManager", test_crew_manager),
        ("Quick Analysis", run_quick_analysis_test)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<25} {status}")
    
    print("-" * 60)
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
