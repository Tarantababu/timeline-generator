# 📅 Project Timeline Generator

A professional Streamlit web application for creating interactive project timelines with enhanced date visibility and team management.

## 🌟 Features

- **Interactive Task Management**: Add, edit, and manage project tasks through a user-friendly interface
- **Tag-based Team Selection**: Easy team selection with autocomplete and custom team creation
- **Inline Task Editing**: Edit tasks directly in the table with double-click functionality
- **Enhanced Date Visibility**: Clear start (blue) and end (red) date markers on each task
- **Dynamic Team Colors**: Automatic color assignment for new teams, predefined colors for common teams
- **CSV Import/Export**: Upload existing project data or export your timeline data
- **Professional Visualizations**: High-quality timeline charts with week numbers and duration indicators
- **Real-time Updates**: Live timeline generation as you add or modify tasks
- **Milestone Support**: Special markers for single-day tasks and project milestones

## 🚀 Live Demo

Deploy this app on Streamlit Cloud by connecting your GitHub repository.

## 🛠️ Installation

### Option 1: Streamlit Cloud (Recommended)
1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Deploy the app using `app.py` as the main file

### Option 2: Local Development
1. Clone the repository:
```bash
git clone https://github.com/your-username/project-timeline-generator.git
cd project-timeline-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## 📋 Usage

### Adding Tasks
1. **Manual Entry**: Use the form in the main interface to add tasks one by one
2. **Sample Data**: Click "Load Sample Data" in the sidebar to see an example
3. **CSV Upload**: Upload a CSV file with your existing project data

### CSV Format
Your CSV file should contain these columns:
- `Task Name`: Name of the task
- `Start Date`: Start date in YYYY-MM-DD format (e.g., 2025-08-01)
- `End Date`: End date in YYYY-MM-DD format (e.g., 2025-08-15)
- `Team`: Team assigned to the task

Example CSV:
```csv
Task Name,Start Date,End Date,Team
OASIS S.Verif. Endpoint,2025-07-21,2025-09-03,A-Team
TVS RAS integration,2025-08-18,2025-09-05,Ninjas
Release Planning,2025-09-15,2025-09-15,All Teams
```

### Timeline Features
- **Start Dates**: Displayed in blue boxes to the left of task bars
- **End Dates**: Displayed in red boxes to the right of task bars
- **Duration**: Shown in parentheses below each task
- **Today Marker**: Red dashed line indicates the current date
- **Week Numbers**: Calendar weeks displayed at the top of the chart
- **Milestones**: Diamond markers for single-day tasks

## 🎨 Team Management

### Predefined Teams
The app comes with pre-configured team colors for common team names:
- A-Team (Red) - Ninjas (Teal) - Mavericks (Blue) - Challengers (Green)
- 5G (Yellow) - All Teams (Plum) - Alchemist (Orange) - Phoenix (Pink)
- Spartans (Lavender) - Wizards (Light Green)

### Custom Teams
- Enter any team name when adding tasks
- Colors are automatically generated for new teams using a consistent algorithm
- Team colors remain consistent throughout your project
- View all active teams and their colors in the sidebar

## 📁 Project Structure

```
project-timeline-generator/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
├── .gitignore         # Git ignore rules
└── sample_data.csv    # Sample project data
```

## 🔧 Customization

### Adding Teams
You can either:
1. **Select existing teams**: Choose from teams already used in your project
2. **Create new teams**: Enter any custom team name
3. **Mix and match**: Use both predefined and custom team names

The app will automatically assign colors to new teams and maintain consistency across your project.

### Modifying Plot Appearance
Adjust the `create_timeline_plot()` function parameters:
- Figure dimensions
- Color schemes
- Font sizes
- Grid styles

## 📊 Export Options

- **PNG Timeline**: Download high-resolution timeline image
- **CSV Data**: Export your task data for backup or sharing
- **Print-Ready**: Generated timelines are optimized for presentations and reports

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Issues & Support

If you encounter any issues or have suggestions for improvements:
1. Check the [existing issues](https://github.com/your-username/project-timeline-generator/issues)
2. Create a new issue with detailed information about the problem
3. Include sample data and screenshots when possible

## 🔄 Updates & Changelog

### v1.0.0
- Initial release
- Basic timeline functionality
- CSV import/export
- Team color coding
- Enhanced date visibility

---

**Made with ❤️ using Streamlit**

For more information about Streamlit, visit [streamlit.io](https://streamlit.io)
