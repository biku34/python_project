html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apache Log Analysis</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f4f4f4;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        h2 {
            text-align: center;
            color: #333;
        }
        .chart {
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .chart img {
            width: 100%;
            max-width: 800px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        .chart-title {
            margin-bottom: 10px;
            font-size: 1.5em;
            color: #555;
        }
        footer {
            text-align: center;
            margin-top: 50px;
            color: #888;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Apache Log Analysis Report</h1>
        
        <div class="chart">
            <h2>Apache Server Activity (5-Hour Intervals)</h2>
            <img src="time_activity.png" alt="Time Activity Chart">
        </div>
        
        <div class="chart">
            <h2>Top 10 Activity Count by IP Address</h2>
            <img src="top_ips.png" alt="Top IPs Chart">
        </div>
        
        <div class="chart">
            <h2>Top 10 Requested URLs</h2>
            <img src="top_urls.png" alt="Top URLs Chart">
        </div>
        
        <div class="chart">
            <h2 class="chart-title">HTTP Method Distribution</h2>
            <img src="http_method_distribution.png" alt="HTTP Method Distribution">
        </div>
        
        <div class="chart">
            <h2>HTTP Status Code Distribution</h2>
            <img src="http_status_distribution.png" alt="HTTP Status Code Distribution">
        </div>
        
        <div class="chart">
            <h2 class="chart-title">Browser Activity Distribution</h2>
            <img src="browser_distribution.png" alt="Browser Activity Distribution">
        </div>
    </div>

    <footer>
        <p>&copy; 2024 Bikram Sadhukhan. All Rights Reserved.</p>
    </footer>
</body>
</html>
"""

# Write the HTML content to a file
with open("apache_log_analysis.html", "w") as html_file:
    html_file.write(html_content)

print("HTML report generated as 'apache_log_analysis.html'")
