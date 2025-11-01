"""
Script to install required NLP models for Matrix of Truth backend
"""
import subprocess
import sys

def install_spacy_model():
    """Install the spaCy English model"""
    print("="*70)
    print("Installing spaCy English Model (en_core_web_sm)")
    print("="*70)
    print("\nThis may take a few minutes...\n")
    
    try:
        # Try to download using spacy download command
        result = subprocess.run(
            [sys.executable, "-m", "spacy", "download", "en_core_web_sm"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✓ spaCy model installed successfully!")
            return True
        else:
            print("✗ Failed to install using spacy download command")
            print(f"Error: {result.stderr}")
            
            # Try alternative installation method
            print("\nTrying alternative installation method...")
            result = subprocess.run(
                [
                    sys.executable, "-m", "pip", "install",
                    "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl"
                ],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✓ spaCy model installed successfully!")
                return True
            else:
                print("✗ Failed to install spaCy model")
                print(f"Error: {result.stderr}")
                return False
                
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def verify_installation():
    """Verify that the model is properly installed"""
    print("\n" + "="*70)
    print("Verifying Installation")
    print("="*70 + "\n")
    
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("✓ spaCy model loaded successfully!")
        
        # Test the model
        doc = nlp("This is a test sentence.")
        print(f"✓ Model test passed! Found {len(doc)} tokens.")
        
        return True
    except Exception as e:
        print(f"✗ Verification failed: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("Matrix of Truth - NLP Model Installation")
    print("="*70 + "\n")
    
    print("This script will install the required spaCy model for NLP analysis.")
    print("The model is approximately 12MB in size.\n")
    
    response = input("Do you want to continue? (y/n): ").lower()
    
    if response != 'y':
        print("Installation cancelled.")
        return
    
    print()
    
    # Install the model
    if install_spacy_model():
        # Verify installation
        if verify_installation():
            print("\n" + "="*70)
            print("Installation Complete!")
            print("="*70)
            print("\nYou can now use the NLP analysis endpoint.")
            print("Start the server with: python start_server.py")
        else:
            print("\n" + "="*70)
            print("Installation completed but verification failed")
            print("="*70)
            print("\nPlease try running manually:")
            print("  python -m spacy download en_core_web_sm")
    else:
        print("\n" + "="*70)
        print("Installation Failed")
        print("="*70)
        print("\nPlease try running manually:")
        print("  python -m spacy download en_core_web_sm")
        print("\nOr install directly from wheel:")
        print("  pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl")

if __name__ == "__main__":
    main()
