Project Description and Work Plan
=================================================
HUMAN WRITTEN SECTION - DO NOT MODIFY

1. Project Overview
This project is a photo-editing application. 
Eventual Capabilites:
- Import and export images in various formats (JPEG, PNG, BMP, etc.)
- Basic editing features (crop, rotate, resize)
- Advanced editing features (filters, color correction, layers)
- User-friendly interface with drag-and-drop functionality
- Paintlike features (brushes, shapes, text)

2. Work Plan
 Work stages:
 1. File open and display
 2. Basic editing features:
    - Crop
    - Rotate/Flip
    - Resize
    - Save
 3. Intermediate editing features:
    - Filters
    - Color correction,changes,BW
 4. Paint Features:
    - Brushes
    - Shapes
    - Text
 5. User interface enhancements:
    - Drag-and-drop functionality
    - Toolbars and menus for easy access to features
    - zoom and pan functionality
 6. Advanced features:
    - Layer management
    - Advanced selection tools
    - Warp/morph brush tools
    - Non-destructive editing

Architecutre:
- Written in Python, employ libraries
- Written in modular fashion with clean code principles
- Small classes and functions
- minimal comments, ( only 'why' comments, not 'what' comments as clean code is self-documenting )

/////////////////////////////////////////////

AI AGENT WRITTEN SECTION - NOTES and Readme from AI to User go here

Current Work Stage:
  Stage 3 - In Progress (UI restructuring + filters/adjustments)

What is implemented now:
- Stage 2 features retained (Open/Save, Rotate/Flip, Resize)
- Initial Stage 3: Filters (grayscale, sepia, invert, blur) and adjustments (brightness, contrast, saturation, sharpness)
- Improved UI layout: top toolbar + menus, and a left sidebar with grouped sections (Adjustments, Quick Filters)
- Code modularization: filter logic in `photoedit/filters.py`

How to run:
- Ensure Python 3.10+ is installed
- Install dependency: `pip install -r requirements.txt`
- Run: `python main.py`

Notes on UI organization:
- Sidebar and menus enable scalable growth without cluttering with button rows
- Future: add tabs or collapsible sections for Layers, History, and Tools

Next steps:
- Implement Crop tool with rubber-band selection
- Add undo/redo history to support non-destructive workflow
- Add more filters (BW with sliders) and live preview pipeline

/////////////////////////////////////////////