# Construction Progress Monitoring System

## Overview
The Construction Progress Monitoring System is a machine learning-based solution designed to automate the tracking of construction activities using site images and a building plan. By uploading a building plan and periodic site images, the system compares actual progress against planned construction stages and generates detailed reports or alerts for any discrepancies.
Though it is not complete the work is still going on.

## Features
- **Building Plan Upload**: Allows the user to upload a building plan for analysis.
- **Image Upload**: Users can upload images from the construction site for progress monitoring.
- **Feature Extraction**: The system analyzes key structural elements such as walls, floors, and columns from both the building plan and site images.
- **Progress Monitoring**: Compares site images with the building plan and determines the construction stage.
- **Alerts and Reports**: Generates progress reports or raises alerts in case of discrepancies between the plan and actual construction.

## System Architecture
The system is composed of four key blocks:

1. **Input Block**:
   - *Building Plan Upload Block*: Accepts and processes the building plan for feature extraction.
   - *Image Upload Block*: Accepts site images for comparison.
   
2. **Processing Block**:
   - *Building Plan Processing*: Extracts key features and construction milestones from the building plan.
   - *Image Preprocessing*: Normalizes site images and extracts relevant features.
   
3. **Comparison Block**:
   - *Feature Matching*: Compares features extracted from the site images with those from the building plan.
   - *Stage Identification*: Determines the current construction stage based on the comparison.
   
4. **Output Block**:
   - *Progress Report*: Provides a detailed report of construction progress.
   - *Alert Block*: Raises an alert if discrepancies are detected.

## Workflow
1. **Upload Building Plan**: The project manager or owner uploads the building plan in a compatible format.
2. **Upload Construction Site Images**: Users periodically upload images of the site.
3. **Feature Extraction & Comparison**: The system extracts key features from both the building plan and the images, compares them, and identifies the current construction stage.
4. **Reports & Alerts**: Generates a progress report or raises alerts if construction is not proceeding as per the plan.

## Output
- **Progress Report**: A detailed report that includes the current construction stage, similarity score (how closely the actual construction matches the plan), and a timeline of stage completion.
- **Discrepancy Alert**: If deviations are detected, the system raises an alert and highlights the areas of discrepancy.
- **Annotated Images**: Highlights parts of the construction that match or deviate from the plan (green for matched, red for discrepancies).
- **Dashboard**: Provides an interactive dashboard to view progress over time, stage completion, and discrepancies.
- **CSV/Excel Reports**: Downloadable reports in CSV or Excel format for further analysis.

## Example Output
- **Text-Based Report**:
  - Project: ABC Building
  - Uploaded Image Date: 2024-09-11
  - Current Stage: Superstructure in progress
  - Similarity Score: 87% (Plan vs. Actual)
  - No discrepancies detected.

- **CSV/Excel Report Example**:
  | Date       | Construction Stage | Similarity Score | Discrepancy                 |
  |------------|--------------------|------------------|-----------------------------|
  | 2024-09-01 | Foundation          | 95%              | None                        |
  | 2024-09-18 | Superstructure      | 87%              | Discrepancy in column alignment |

