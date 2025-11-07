@echo off
echo =====================================================
echo Faculty Survey Dashboard Deployment Script
echo =====================================================
echo.

:: Check if repository exists
if not exist "%USERPROFILE%\abijan96.github.io" (
    echo Repository not found. Cloning...
    cd %USERPROFILE%
    git clone https://github.com/abijan96/abijan96.github.io.git
    cd abijan96.github.io
) else (
    echo Repository found. Updating...
    cd %USERPROFILE%\abijan96.github.io
    git pull origin main
)

echo.
echo Creating dashboard folder...
if not exist "faculty-survey-dashboard" mkdir faculty-survey-dashboard

echo.
echo Copying files...
xcopy /Y "%~dp0index.html" "faculty-survey-dashboard\"
xcopy /Y "%~dp0dashboard.js" "faculty-survey-dashboard\"
xcopy /Y "%~dp0faculty_survey_data.csv" "faculty-survey-dashboard\"
xcopy /Y "%~dp0README.md" "faculty-survey-dashboard\"

echo.
echo Staging changes...
git add faculty-survey-dashboard/

echo.
echo Committing changes...
git commit -m "Add interactive faculty survey dashboard with 8 visualizations"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo =====================================================
echo Deployment Complete!
echo =====================================================
echo.
echo Your dashboard will be available in 1-3 minutes at:
echo https://abijan96.github.io/faculty-survey-dashboard/
echo.
echo Press any key to exit...
pause >nul
