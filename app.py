# File: app.py (Main Streamlit application)
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import defaultdict
import numpy as np
from io import BytesIO

# Set page config
st.set_page_config(
    page_title="Project Timeline Generator",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_team_color(team_name):
    """Get color for a team, generate random color for new teams"""
    if team_name in TEAM_COLORS:
        return TEAM_COLORS[team_name]
    else:
        # Generate a consistent color based on team name hash
        import hashlib
        hash_object = hashlib.md5(team_name.encode())
        hex_dig = hash_object.hexdigest()
        # Use the first 6 characters to create a color
        return f"#{hex_dig[:6]}"
TEAM_COLORS = {
    "A-Team": "#FF6B6B",        # Red
    "Ninjas": "#4ECDC4",        # Teal
    "Mavericks": "#45B7D1",     # Blue
    "Challengers": "#96CEB4",   # Green
    "5G": "#FFEAA7",            # Yellow
    "All Teams": "#DDA0DD",     # Plum
    "Alchemist": "#FFB347",     # Orange
    "Phoenix": "#FF8C94",       # Pink
    "Spartans": "#C7CEEA",      # Lavender
    "Wizards": "#B4F8C8"        # Light Green
}

def create_timeline_plot(tasks_data, figure_width=18, figure_height=12):
    """Create the enhanced timeline plot with better date visibility"""
    
    # Group tasks by team for y-axis arrangement
    team_tasks = defaultdict(list)
    for _, row in tasks_data.iterrows():
        start_dt = pd.to_datetime(row['Start Date']).to_pydatetime()
        end_dt = pd.to_datetime(row['End Date']).to_pydatetime()
        team_tasks[row['Team']].append((row['Task Name'], start_dt, end_dt))

    teams = list(team_tasks.keys())
    
    if not teams:
        return None

    # Create enhanced plot
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(figure_width, figure_height))

    # Set background color
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#F8F9FA')

    # Add grid for better readability
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5, color='gray')
    ax.set_axisbelow(True)

    # Plot each team's tasks with enhanced styling and better date visibility
    for i, team in enumerate(teams):
        y_base = i
        color = get_team_color(team)

        for idx, (name, start, end) in enumerate(team_tasks[team]):
            y_offset = y_base + (idx * 0.3)
            duration = (end - start).days
            bar_height = 0.25

            # Draw the task bar
            ax.barh(y_offset, duration, left=start, height=bar_height,
                   color=color, alpha=0.8, edgecolor='white', linewidth=2)

            # Calculate text positioning
            mid_point = start + (end - start) / 2

            # Determine optimal text placement and size based on bar width
            bar_width_days = duration

            # Truncate task names based on available space
            if bar_width_days < 3:
                display_name = name[:8] + "..." if len(name) > 8 else name
                font_size = 7
            elif bar_width_days < 5:
                display_name = name[:15] + "..." if len(name) > 15 else name
                font_size = 8
            else:
                display_name = name[:30] + "..." if len(name) > 30 else name
                font_size = 9

            # Text color selection
            light_colors = ['#FFEAA7', '#96CEB4', '#B4F8C8', '#DDA0DD', '#C7CEEA']
            if any(color.upper() == light_color.upper() for light_color in light_colors):
                text_color = 'black'
            else:
                # Check if color is light using RGB values
                hex_color = color.lstrip('#')
                if len(hex_color) == 6:
                    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                    # Calculate brightness using relative luminance
                    brightness = (r * 0.299 + g * 0.587 + b * 0.114)
                    text_color = 'black' if brightness > 127 else 'white'
                else:
                    text_color = 'white'

            # Position task name on the bar
            ax.text(mid_point, y_offset, display_name,
                   ha='center', va='center', fontsize=font_size, fontweight='bold',
                   color=text_color, clip_on=True, zorder=10)

            # Add start date at the beginning of the bar
            start_date_str = start.strftime("%m/%d")
            ax.text(start - timedelta(days=0.5), y_offset, start_date_str,
                   ha='right', va='center', fontsize=8, fontweight='bold',
                   color='darkblue',
                   bbox=dict(boxstyle="round,pad=0.2", facecolor='lightcyan',
                            edgecolor='darkblue', linewidth=1, alpha=0.9))

            # Add end date at the end of the bar
            end_date_str = end.strftime("%m/%d")
            ax.text(end + timedelta(days=0.5), y_offset, end_date_str,
                   ha='left', va='center', fontsize=8, fontweight='bold',
                   color='darkred',
                   bbox=dict(boxstyle="round,pad=0.2", facecolor='mistyrose',
                            edgecolor='darkred', linewidth=1, alpha=0.9))

            # Add duration indicator
            duration_text = f"({duration}d)" if duration > 0 else "(1d)"
            ax.text(mid_point, y_offset - 0.15, duration_text,
                   ha='center', va='center', fontsize=7,
                   color='darkgray', fontweight='bold', style='italic')

            # Add milestone markers for single-day tasks
            if duration == 0:
                ax.plot(start, y_offset, marker='D', markersize=12, 
                       color='red', markeredgecolor='darkred', markeredgewidth=2,
                       zorder=15)

    # Y-axis setup
    max_tasks_per_team = max(len(team_tasks[team]) for team in teams)
    y_spacing = max(0.6, max_tasks_per_team * 0.3)

    ax.set_yticks(range(len(teams)))
    ax.set_yticklabels(teams, fontsize=12, fontweight='bold')
    ax.set_ylim(-0.4, len(teams) - 0.6 + y_spacing)

    # X-axis date formatting
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    ax.xaxis.set_minor_locator(mdates.DayLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d\n%Y"))
    plt.xticks(rotation=45, ha='right', fontsize=10)

    # Add today's date marker
    today = datetime.now()
    start_date = min(pd.to_datetime(tasks_data['Start Date']).min(), today)
    if today >= start_date:
        ax.axvline(today, color='red', linestyle='--', linewidth=3, alpha=0.8, 
                   label=f'Today ({today.strftime("%m/%d/%Y")})', zorder=5)

    # Labels and title
    ax.set_xlabel("Timeline (Month/Day)", fontsize=14, fontweight='bold', labelpad=25)
    ax.set_ylabel("Development Teams", fontsize=14, fontweight='bold', labelpad=20)
    ax.set_title("Project Delivery Plan Timeline\nTeam Workload & Dependencies\n(Start Dates in Blue | End Dates in Red)",
                fontsize=16, fontweight='bold', pad=40)

    # Week numbers on top
    ax3 = ax.twiny()
    ax3.set_xlim(ax.get_xlim())

    start_date = pd.to_datetime(tasks_data['Start Date']).min().to_pydatetime()
    end_date = pd.to_datetime(tasks_data['End Date']).max().to_pydatetime()

    week_dates = []
    current_date = start_date - timedelta(days=start_date.weekday())
    while current_date <= end_date + timedelta(days=7):
        week_dates.append(current_date)
        current_date += timedelta(days=7)

    ax3.set_xticks(week_dates)
    week_labels = [f"Week {d.isocalendar()[1]}" for d in week_dates]
    ax3.set_xticklabels(week_labels, fontsize=10, fontweight='bold')
    ax3.set_xlabel("Calendar Weeks", fontsize=12, fontweight='bold', labelpad=15)

    # Legend
    legend_elements = []
    legend_labels = []

    for team in teams:
        color = get_team_color(team)
        legend_elements.append(plt.Rectangle((0,0),1,1, facecolor=color, alpha=0.8, 
                                           edgecolor='black', linewidth=1))
        legend_labels.append(team)

    legend_elements.extend([
        plt.Rectangle((0,0),1,1, facecolor='lightcyan', edgecolor='darkblue', linewidth=1),
        plt.Rectangle((0,0),1,1, facecolor='mistyrose', edgecolor='darkred', linewidth=1)
    ])
    legend_labels.extend(['Start Date', 'End Date'])

    ax.legend(legend_elements, legend_labels, loc='lower right',
             bbox_to_anchor=(0.98, 0.02), ncol=2, frameon=True, fancybox=True,
             shadow=True, facecolor='white', edgecolor='black', fontsize=10)

    plt.tight_layout()
    return fig

def main():
    st.title("📅 Project Timeline Generator")
    st.markdown("Create professional project timelines with team assignments and date visibility")

    # Initialize session state for tasks FIRST
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []

    # Sidebar for inputs
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Team Management Section
        st.subheader("👥 Team Management")
        if st.session_state.tasks:
            unique_teams = list(set([task["Team"] for task in st.session_state.tasks]))
            st.write(f"**Active Teams ({len(unique_teams)}):**")
            for team in sorted(unique_teams):
                team_color = get_team_color(team)
                st.markdown(
                    f"<div style='display:flex; align-items:center; margin:2px 0;'>"
                    f"<span style='display:inline-block; width:12px; height:12px; "
                    f"background-color:{team_color}; border-radius:2px; margin-right:8px;'></span>"
                    f"<span style='font-size:14px;'>{team}</span></div>",
                    unsafe_allow_html=True
                )
        else:
            st.info("No teams yet. Add tasks to see teams here.")
        
        st.markdown("---")
        
        # Plot dimensions
        st.subheader("📊 Plot Settings")
        figure_width = st.slider("Figure Width", 12, 24, 18)
        figure_height = st.slider("Figure Height", 8, 16, 12)
        
        st.markdown("---")
        
        # Sample data option
        if st.button("🔄 Load Sample Data"):
            st.session_state.sample_loaded = True

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Task Input")
        
        # Sample data loading (moved here after session state initialization)
        # Load sample data if requested
        if 'sample_loaded' in st.session_state and st.session_state.sample_loaded:
            st.session_state.tasks = [
                {"Task Name": "OASIS S.Verif. Endpoint", "Start Date": "2025-07-21", "End Date": "2025-09-03", "Team": "A-Team"},
                {"Task Name": "TVS RAS integration under CPS-2684", "Start Date": "2025-08-18", "End Date": "2025-09-05", "Team": "Ninjas"},
                {"Task Name": "RAS integration", "Start Date": "2025-08-12", "End Date": "2025-09-03", "Team": "Challengers"},
                {"Task Name": "Games Oasis Related Messages", "Start Date": "2025-08-25", "End Date": "2025-08-29", "Team": "5G"},
                {"Task Name": "E2E & PLAB testing", "Start Date": "2025-09-08", "End Date": "2025-09-15", "Team": "All Teams"},
                {"Task Name": "Release", "Start Date": "2025-09-15", "End Date": "2025-09-15", "Team": "All Teams"},
            ]
            st.session_state.sample_loaded = False
            st.rerun()
        
        # Task input form
        with st.form("task_input_form"):
            st.write("**Add New Task:**")
            col_task, col_team = st.columns(2)
            col_start, col_end = st.columns(2)
            
            with col_task:
                task_name = st.text_input("Task Name", placeholder="Enter task name...")
            with col_team:
                # Get existing teams from current tasks
                existing_teams = list(set([task.get("Team", "") for task in st.session_state.tasks if task.get("Team")]))
                available_teams = list(TEAM_COLORS.keys()) + [team for team in existing_teams if team not in TEAM_COLORS.keys()]
                # Remove duplicates while preserving order
                available_teams = list(dict.fromkeys(available_teams))
                
                # Team selection with custom input option
                team_option = st.radio(
                    "Team Selection:",
                    ["Select from existing", "Enter new team"],
                    horizontal=True,
                    help="Choose from existing teams or create a new one"
                )
                
                # Initialize team variable
                team = ""
                
                if team_option == "Select from existing":
                    # Show dropdown for existing teams
                    if available_teams:
                        team = st.selectbox(
                            "📋 Choose Existing Team", 
                            [""] + available_teams,  # Add empty option at top
                            key="team_dropdown_existing",
                            help="Select from predefined or previously used teams",
                            index=0
                        )
                    else:
                        # If no teams exist, show message and empty text input
                        st.info("ℹ️ No existing teams found. Switch to 'Enter new team' to create your first team.")
                        st.selectbox(
                            "📋 Choose Existing Team", 
                            ["No teams available"], 
                            key="team_dropdown_empty",
                            disabled=True
                        )
                        team = ""
                        
                elif team_option == "Enter new team":
                    # Show text input for new team
                    team = st.text_input(
                        "✏️ Enter New Team Name", 
                        value="",
                        placeholder="Type your team name here...", 
                        key="team_text_input_new",
                        help="Create a new team with any name you want"
                    )
            with col_start:
                start_date = st.date_input("Start Date", value=datetime.now().date())
            with col_end:
                end_date = st.date_input("End Date", value=datetime.now().date() + timedelta(days=7))
            
            submitted = st.form_submit_button("➕ Add Task")
            
            if submitted and task_name and team:
                if start_date <= end_date:
                    new_task = {
                        "Task Name": task_name,
                        "Start Date": start_date.strftime("%Y-%m-%d"),
                        "End Date": end_date.strftime("%Y-%m-%d"),
                        "Team": team.strip()
                    }
                    st.session_state.tasks.append(new_task)
                    st.success(f"Task '{task_name}' added successfully to team '{team}'!")
                    st.rerun()
                else:
                    st.error("End date must be after or equal to start date!")
            elif submitted and task_name and not team:
                st.error("Please select or enter a team name!")

    with col2:
        st.subheader("📊 Current Tasks")
        
        if st.session_state.tasks:
            # Display current tasks with team management
            df = pd.DataFrame(st.session_state.tasks)
            
            # Show team summary
            team_counts = df['Team'].value_counts()
            st.write("**Team Summary:**")
            for team, count in team_counts.items():
                team_color = get_team_color(team)
                st.markdown(
                    f"<span style='display:inline-block; width:12px; height:12px; "
                    f"background-color:{team_color}; border-radius:2px; margin-right:5px;'></span>"
                    f"**{team}**: {count} task{'s' if count != 1 else ''}",
                    unsafe_allow_html=True
                )
            
            st.markdown("---")
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Bulk operations
            col_clear, col_download = st.columns(2)
            with col_clear:
                if st.button("🗑️ Clear All", type="secondary"):
                    st.session_state.tasks = []
                    st.rerun()
            
            with col_download:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name="project_tasks.csv",
                    mime="text/csv"
                )
        else:
            st.info("No tasks added yet. Add tasks using the form on the left or load sample data.")

    # File upload section
    st.markdown("---")
    st.subheader("📁 Upload Tasks from CSV")
    
    uploaded_file = st.file_uploader(
        "Upload a CSV file with columns: Task Name, Start Date, End Date, Team",
        type=['csv'],
        help="CSV should have columns: 'Task Name', 'Start Date' (YYYY-MM-DD), 'End Date' (YYYY-MM-DD), 'Team'"
    )
    
    if uploaded_file is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_file)
            required_columns = ['Task Name', 'Start Date', 'End Date', 'Team']
            
            if all(col in uploaded_df.columns for col in required_columns):
                # Validate dates
                try:
                    pd.to_datetime(uploaded_df['Start Date'])
                    pd.to_datetime(uploaded_df['End Date'])
                    
                    st.session_state.tasks = uploaded_df.to_dict('records')
                    st.success(f"Successfully loaded {len(uploaded_df)} tasks from CSV!")
                    st.rerun()
                except:
                    st.error("Invalid date format in CSV. Please use YYYY-MM-DD format.")
            else:
                st.error(f"CSV must contain these columns: {required_columns}")
        except Exception as e:
            st.error(f"Error reading CSV file: {str(e)}")

    # Generate timeline
    if st.session_state.tasks:
        st.markdown("---")
        st.subheader("📈 Generated Timeline")
        
        # Create DataFrame from tasks
        tasks_df = pd.DataFrame(st.session_state.tasks)
        
        # Generate plot
        with st.spinner("Generating timeline..."):
            fig = create_timeline_plot(tasks_df, figure_width, figure_height)
            
            if fig:
                st.pyplot(fig)
                
                # Download plot
                buffer = BytesIO()
                fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight',
                           facecolor='white', edgecolor='none')
                buffer.seek(0)
                
                st.download_button(
                    label="📥 Download Timeline (PNG)",
                    data=buffer.getvalue(),
                    file_name="project_timeline.png",
                    mime="image/png"
                )
                plt.close(fig)  # Close figure to free memory
            else:
                st.error("Unable to generate timeline. Please check your data.")
    
    # Instructions
    with st.expander("ℹ️ How to Use"):
        st.markdown("""
        **Getting Started:**
        1. **Add Tasks Manually**: Use the form on the left to add individual tasks
        2. **Load Sample Data**: Click the button in the sidebar to see an example
        3. **Upload CSV**: Upload a CSV file with your project data
        
        **CSV Format:**
        Your CSV should have these columns:
        - `Task Name`: Name of the task
        - `Start Date`: Start date in YYYY-MM-DD format
        - `End Date`: End date in YYYY-MM-DD format  
        - `Team`: Team assigned to the task
        
        **Features:**
        - 📅 **Date Visibility**: Start dates (blue) and end dates (red) are clearly marked
        - 🎨 **Dynamic Team Colors**: Each team gets a unique color (predefined or auto-generated)
        - 🏷️ **Flexible Team Names**: Add custom team names or select from existing ones
        - 📊 **Duration Display**: Task duration shown in days
        - 🎯 **Milestones**: Single-day tasks shown as diamond markers
        - 📈 **Week Numbers**: Calendar weeks displayed at the top
        - 📍 **Today Marker**: Red dashed line shows current date
        - 👥 **Team Management**: View active teams and their colors in the sidebar
        """)

if __name__ == "__main__":
    main()
