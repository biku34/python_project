import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime
import matplotlib.dates as mdates
from collections import Counter
import tkinter as tk
from tkinter import simpledialog, messagebox
import os

# Function to classify browsers from user agent string
def classify_browser(user_agent):
    user_agent = user_agent.lower()
    if "chrome" in user_agent and "safari" in user_agent:
        return "Chrome"
    elif "firefox" in user_agent:
        return "Firefox"
    elif "safari" in user_agent:
        return "Safari"
    elif "edge" in user_agent:
        return "Edge"
    elif "msie" in user_agent or "trident" in user_agent:
        return "Internet Explorer"
    else:
        return "Other"

# Function to load and process the log data
def load_data():
    with open("apache_logs.txt", "r") as file:
        log_lines = file.readlines()

    ip_pattern = r"(\d+\.\d+\.\d+\.\d+)"
    timestamp_pattern = r"\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}) \+\d{4}\]"
    url_pattern = r"\"[A-Z]+ (.+?) HTTP"
    method_pattern = r"\"([A-Z]+)"
    status_code_pattern = r"\" [\d]{3}"
    user_agent_pattern = r"\"[^\"]*\" \"([^\"]+)\""

    ip_addresses = [re.search(ip_pattern, line).group(1) for line in log_lines if re.search(ip_pattern, line)]
    timestamps = [re.search(timestamp_pattern, line).group(1) for line in log_lines if re.search(timestamp_pattern, line)]
    urls = [re.search(url_pattern, line).group(1) for line in log_lines if re.search(url_pattern, line)]
    http_methods = [re.search(method_pattern, line).group(1) for line in log_lines if re.search(method_pattern, line)]
    status_codes = [re.search(status_code_pattern, line).group(0).strip()[1:] for line in log_lines if re.search(status_code_pattern, line)]
    user_agents = [re.search(user_agent_pattern, line).group(1) for line in log_lines if re.search(user_agent_pattern, line)]

    # Classify user agents into browsers
    browsers = [classify_browser(ua) for ua in user_agents]

    # Convert timestamps to datetime objects
    dates = [datetime.strptime(ts, "%d/%b/%Y:%H:%M:%S") for ts in timestamps]

    # Create DataFrame for time-based activity
    df = pd.DataFrame(dates, columns=["timestamp"])
    df["count"] = 1
    df.set_index("timestamp", inplace=True)

    # Resample data to count requests every 5 hours
    activity = df.resample("5H").sum()

    # Count IP addresses activity
    ip_counts = Counter(ip_addresses)
    ip_df = pd.DataFrame(ip_counts.items(), columns=['IP Address', 'Activity Count'])

    # Count user agent activity
    user_agent_counts = Counter(user_agents)
    user_agent_df = pd.DataFrame(user_agent_counts.items(), columns=["User Agent", "Activity Count"])

    # Count browser activity
    browser_counts = Counter(browsers)
    browser_df = pd.DataFrame(browser_counts.items(), columns=["Browser", "Activity Count"])

    return activity, ip_df, ip_addresses, urls, http_methods, status_codes, user_agent_df, browser_df

def save_ip_activity(ip, ip_addresses, urls, http_methods, status_codes):
    # Filter activity data for the specified IP
    activity_data = [
        {"IP Address": ip_addr, "URL": url, "HTTP Method": method, "Status Code": status}
        for ip_addr, url, method, status in zip(ip_addresses, urls, http_methods, status_codes)
        if ip_addr == ip
    ]

    # Prepare HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Activity Log for IP: {ip}</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 10px; text-align: left; border: 1px solid #ddd; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Activity Log for IP: {ip}</h1>
        <table>
            <tr>
                <th>IP Address</th>
                <th>URL</th>
                <th>HTTP Method</th>
                <th>Status Code</th>
            </tr>
    """

    # Add rows for each activity
    for entry in activity_data:
        html_content += f"""
        <tr>
            <td>{entry['IP Address']}</td>
            <td>{entry['URL']}</td>
            <td>{entry['HTTP Method']}</td>
            <td>{entry['Status Code']}</td>
        </tr>
        """

    # Close the HTML tags
    html_content += """
        </table>
    </body>
    </html>
    """

    # Save the HTML file
    file_name = f"{ip}_activity_log.html"
    with open(file_name, "w") as html_file:
        html_file.write(html_content)

    print(f"Activity log for IP {ip} has been saved to {file_name}")


# Function to generate plots and save them
def generate_plots(ip_addresses, urls, http_methods, status_codes, user_agent_df, browser_df):
    activity, ip_df, ip_addresses, urls, http_methods, status_codes, user_agent_df, browser_df = load_data()

    # Plot Time-based Activity
    plt.figure(figsize=(10, 5))
    plt.plot(activity.index, activity["count"], color='blue', marker='o', linestyle='-')
    plt.xlabel("Time")
    plt.ylabel("Number of Requests")
    plt.title("Apache Server Activity (5-Hour Intervals)")
    plt.xticks(rotation=45)
    date_format = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=5))
    plt.tight_layout()
    plt.savefig("time_activity.png")
    plt.close()

    # Plot Top 10 IPs Activity
    top_10_ips = ip_df.nlargest(10, 'Activity Count')
    plt.figure(figsize=(10, 5))
    plt.bar(top_10_ips['IP Address'], top_10_ips['Activity Count'], color='green')
    plt.xlabel("IP Address")
    plt.ylabel("Activity Count")
    plt.title("Top 10 Activity Count by IP Address")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("top_ips.png")
    plt.close()

    # Plot Top 10 Requested URLs
    url_counts = Counter(urls).most_common(10)
    url_df = pd.DataFrame(url_counts, columns=["URL", "Request Count"])
    plt.figure(figsize=(10, 5))
    plt.barh(url_df["URL"], url_df["Request Count"], color="purple")
    plt.xlabel("Number of Requests")
    plt.ylabel("URL")
    plt.title("Top 10 Requested URLs")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("top_urls.png")
    plt.close()

    # Plot HTTP Method Distribution
    method_counts = Counter(http_methods)
    method_df = pd.DataFrame(method_counts.items(), columns=["HTTP Method", "Count"])
    plt.figure(figsize=(10, 5))
    plt.bar(method_df['HTTP Method'], method_df['Count'], color="orange")
    plt.xlabel("HTTP Method")
    plt.ylabel("Count")
    plt.title("HTTP Method Distribution")
    plt.tight_layout()
    plt.savefig("http_method_distribution.png")
    plt.close()

    # Plot HTTP Status Code Distribution
    status_code_counts = Counter(status_codes)
    status_code_df = pd.DataFrame(status_code_counts.items(), columns=["HTTP Status Code", "Count"])
    plt.figure(figsize=(10, 5))
    plt.bar(status_code_df['HTTP Status Code'], status_code_df['Count'], color="red")
    plt.xlabel("HTTP Status Code")
    plt.ylabel("Count")
    plt.title("HTTP Status Code Distribution")
    plt.tight_layout()
    plt.savefig("http_status_distribution.png")
    plt.close()

    # Plot Browser Distribution
    plt.figure(figsize=(10, 5))
    plt.bar(browser_df['Browser'], browser_df['Activity Count'], color='cyan')
    plt.xlabel("Browser")
    plt.ylabel("Activity Count")
    plt.title("Browser Activity Distribution")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("browser_distribution.png")
    plt.close()

# Function to create the tkinter window
def create_gui(ip_addresses, urls, http_methods, status_codes, user_agent_df, browser_df):
    # Create a tkinter window
    root = tk.Tk()
    root.title("Apache Log Analysis")
    root.geometry("400x300")  # Set the fixed size of the window

    # Label and Checkbox to ask about IP activity search
    label = tk.Label(root, text="Do you want to search for a specific IP activity?")
    label.pack(pady=20)

    ip_checkbox_var = tk.BooleanVar()
    ip_checkbox = tk.Checkbutton(root, text="Search for a specific IP", variable=ip_checkbox_var)
    ip_checkbox.pack()

    # Function to handle Submit button
    def on_submit():
        if ip_checkbox_var.get():  # If checkbox is checked, prompt for IP
            ip = simpledialog.askstring("Input", "Enter the IP address:", parent=root)
            if ip:
                save_ip_activity(ip, ip_addresses, urls, http_methods, status_codes)
        else:  # Else generate plots and save images
            generate_plots(ip_addresses, urls, http_methods, status_codes, user_agent_df, browser_df)
            messagebox.showinfo("Success", "Graphs have been saved as images.")
        root.quit()

    # Add a Submit button
    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.pack(pady=20)

    # Start the tkinter GUI loop
    root.mainloop()

# Main code execution
if __name__ == "__main__":
    activity, ip_df, ip_addresses, urls, http_methods, status_codes, user_agent_df, browser_df = load_data()
    
    # Create and run the tkinter GUI
    create_gui(ip_addresses, urls, http_methods, status_codes, user_agent_df, browser_df)
