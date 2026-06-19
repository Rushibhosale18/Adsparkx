@echo off
echo ========================================================
echo Adsparkx AI - Persona-Adaptive Customer Support Agent
echo ========================================================
echo.
echo Please wait while we install the necessary Python dependencies...
echo (This may take several minutes depending on your internet speed)
echo.
pip install -r requirements.txt
echo.
echo Dependencies installed successfully!
echo.
echo Initializing Knowledge Base and Vector Database...
python ingest.py
echo.
echo Starting the Streamlit Web Application...
echo.
streamlit run app.py
pause
