"""
Main entry point for the MikroTik Router Monitoring System.

This application demonstrates a clean layered architecture with:
- Domain Layer: Core business entities and repository interfaces
- Application Layer: Use cases and business logic orchestration  
- Infrastructure Layer: External service implementations (MikroTik API)
- Presentation Layer: Controllers and user interface
"""

import asyncio
from src.presentation.controllers import main as presentation_main


def main():
    """Main entry point using layered architecture."""
    print("🚀 Starting MikroTik Router Monitoring System")
    print("="*60)
    
    # Run the presentation layer main function
    asyncio.run(presentation_main())


if __name__ == "__main__":
    main()
