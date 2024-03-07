@echo off

:: Check if AutoClaimHotEvn folder exists, if not, create virtual environment
if not exist AutoClaimHotEvn (
    python -m venv AutoClaimHotEvn

    :: Activate virtual environment
    call AutoClaimHotEvn\Scripts\activate

    :: Install required packages
    pip install -r requirements.txt
) else (
    :: Activate virtual environment
    call AutoClaimHotEvn\Scripts\activate
)

:: Run the main script
python AutoClaim.py --start="10:40" --step=2