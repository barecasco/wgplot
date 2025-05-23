import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.graph_objects as go
import base64
import io
import subprocess
import os
import tempfile
from datetime import datetime

# Initialize the Dash app with custom CSS
app = dash.Dash(__name__)

# Add custom CSS as external stylesheets
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { box-sizing: border-box; }
            body { margin: 0; background-color: #f8fafc; }
            
            .upload-area:hover {
                border-color: #3b82f6 !important;
                background-color: #eff6ff !important;
                color: #3b82f6 !important;
            }
            
            .custom-button:hover {
                background-color: #2563eb !important;
                transform: translateY(-1px);
                box-shadow: 0 6px 12px -2px rgba(59, 130, 246, 0.4) !important;
            }
            
            .custom-button:active {
                transform: translateY(0);
            }
            
            textarea:focus {
                border-color: #3b82f6 !important;
                outline: none;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            }
            
            .details-summary {
                cursor: pointer;
                padding: 8px 0;
                font-weight: 600;
                color: #374151;
            }
            
            .details-summary:hover {
                color: #3b82f6;
            }
            
            @media (max-width: 768px) {
                .container { padding: 16px !important; }
                .card { padding: 20px !important; margin-bottom: 20px !important; }
                .upload-area { line-height: 100px !important; min-height: 100px !important; }
                .textarea { min-height: 150px !important; font-size: 13px !important; }
                .button { padding: 10px 24px !important; font-size: 15px !important; }
            }
            
            @media (max-width: 480px) {
                .container { padding: 12px !important; }
                .card { padding: 16px !important; }
                .upload-area { line-height: 80px !important; min-height: 80px !important; font-size: 14px !important; }
                .textarea { min-height: 120px !important; font-size: 12px !important; padding: 12px !important; }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Define custom CSS styles
custom_styles = {
    'container': {
        'maxWidth': '1200px',
        'margin': '0 auto',
        'padding': '20px',
        'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        'backgroundColor': '#f8fafc',
        'minHeight': '100vh'
    },
    'header': {
        'textAlign': 'center',
        'marginBottom': '40px',
        'color': '#1e293b',
        'fontSize': 'clamp(24px, 5vw, 36px)',
        'fontWeight': '700',
        'letterSpacing': '-0.025em'
    },
    'card': {
        'backgroundColor': '#ffffff',
        'borderRadius': '12px',
        'boxShadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'padding': '24px',
        'marginBottom': '24px',
        'border': '1px solid #e2e8f0'
    },
    'sectionTitle': {
        'fontSize': 'clamp(18px, 4vw, 24px)',
        'fontWeight': '600',
        'color': '#334155',
        'marginBottom': '16px',
        'display': 'flex',
        'alignItems': 'center',
        'gap': '8px'
    },
    'uploadArea': {
        'width': '100%',
        'minHeight': '120px',
        # 'lineHeight': '120px',
        'borderWidth': '2px',
        'borderStyle': 'dashed',
        'borderColor': '#cbd5e1',
        'borderRadius': '8px',
        'textAlign': 'center',
        'backgroundColor': '#f8fafc',
        'cursor': 'pointer',
        'transition': 'all 0.3s ease',
        'fontSize': '16px',
        'color': '#64748b'
    },
    'uploadAreaHover': {
        'borderColor': '#3b82f6',
        'backgroundColor': '#eff6ff',
        'color': '#3b82f6'
    },
    'textarea': {
        'width': '100%',
        'minHeight': '180px',
        'paddingLeft': '10px',
        'paddingTop': '10px',
        'border': '2px solid #e2e8f0',
        'borderRadius': '8px',
        'fontSize': '14px',
        'fontFamily': '"Fira Code", "Consolas", monospace',
        'resize': 'vertical',
        'transition': 'border-color 0.3s ease',
        'lineHeight': '1.5'
    },
    'button': {
        'backgroundColor': '#3b82f6',
        'color': 'white',
        'padding': '12px 32px',
        'border': 'none',
        'borderRadius': '8px',
        'cursor': 'pointer',
        'fontSize': '16px',
        'fontWeight': '600',
        'transition': 'all 0.3s ease',
        'boxShadow': '0 4px 6px -1px rgba(59, 130, 246, 0.3)',
        'minWidth': '160px'
    },
    'buttonContainer': {
        'textAlign': 'center',
        'marginBottom': '32px'
    },
    'successMessage': {
        'color': '#059669',
        'backgroundColor': '#d1fae5',
        'padding': '12px 16px',
        'borderRadius': '8px',
        'border': '1px solid #a7f3d0',
        'margin': '16px 0'
    },
    'errorMessage': {
        'color': '#dc2626',
        'backgroundColor': '#fee2e2',
        'padding': '12px 16px',
        'borderRadius': '8px',
        'border': '1px solid #fecaca',
        'margin': '16px 0'
    },
    'previewContainer': {
        'backgroundColor': '#f8fafc',
        'padding': '16px',
        'borderRadius': '8px',
        'border': '1px solid #e2e8f0',
        'overflow': 'auto',
        'fontSize': '12px',
        'fontFamily': '"Fira Code", "Consolas", monospace'
    },
    'plotContainer': {
        'textAlign': 'center',
        'padding': '20px 0'
    },
    'plotImage': {
        'maxWidth': '100%',
        'height': 'auto',
        'borderRadius': '8px',
        'boxShadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        'border': '1px solid #e2e8f0'
    },
    'icon': {
        'fontSize': '20px',
        'marginRight': '8px'
    }
}

# Define the app layout
app.layout = html.Div([

    
    html.Div([
        # Header
        html.H1("📊 Gnuplot on Server", style=custom_styles['header']),
        
        # CSV File Upload Section
        html.Div([
            html.H3(["📁 ", "Upload Text File"], style=custom_styles['sectionTitle']),
            html.P("Select your text data file to visualize with gnuplot", 
                   style={'color': '#64748b', 'marginBottom': '16px', 'fontSize': '14px'}),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    html.Div("📤", style={'fontSize': '32px', 'marginBottom': '8px'}),
                    html.Div(['Drag and Drop or ', html.Strong('Click to Select', style={'color': '#3b82f6'})]),
                    html.Div("text files only", style={'fontSize': '12px', 'color': '#94a3b8', 'marginTop': '4px'})
                ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'justifyContent': 'center'}),
                style={**custom_styles['uploadArea'], 'className': 'upload-area'},
                multiple=False,
                className='upload-area'
            ),
            html.Div(id='upload-status'),
        ], style=custom_styles['card']),
        
        # Gnuplot Command Input Section
        html.Div([
            html.H3(["⚙️ ", "Gnuplot Commands"], style=custom_styles['sectionTitle']),
            html.P("Write your gnuplot commands below. Use 'data.txt' to reference your uploaded file.", 
                   style={'color': '#64748b', 'marginBottom': '16px', 'fontSize': '14px'}),
            html.Details([
                html.Summary("💡 Example Commands", className='details-summary', 
                           style={'fontWeight': '600', 'color': '#374151', 'cursor': 'pointer', 'marginBottom': '12px'}),
                html.Div([
                    html.Pre("""
set terminal png size 800,600 # set image resolution here
set output "plot.png" # do not change
set datafile separator "," # for csv file
set title "Data Visualization"
set xlabel "X Values"
set ylabel "Y Values"
plot "data.csv" using 1:2 with lines title "Data"

# Scatter plot with points
plot "data.csv" using 1:2 with points pointtype 7 pointsize 1.5

# Multiple columns
plot "data.csv" using 1:2 with lines title "Series 1", \\
     "data.csv" using 1:3 with lines title "Series 2" """, 
                           style={'backgroundColor': '#1e293b', 'color': '#e2e8f0', 'padding': '16px', 
                                  'borderRadius': '6px', 'fontSize': '12px', 'overflow': 'auto'})
                ])
            ], style={'marginBottom': '16px'}),
            dcc.Textarea(
                id='gnuplot-command',
                placeholder='Enter your gnuplot commands here...\n\nExample:\nset terminal png size 800,600\nset output "plot.png"\nset title "My Plot"\nplot "data.txt" using 1:2 with lines',
                style=custom_styles['textarea'],
                value='set terminal png size 800,600\nset output "plot.png"\nset title "Data Visualization"\nset xlabel "X Values"\nset ylabel "Y Values"\nset datafile separator ","\nplot "data.txt" using 1:2 with lines title "Data"'
            ),
        ], style=custom_styles['card']),
        
        # Submit Button
        html.Div([
            html.Button(['🚀 ', 'Generate Plot'], id='submit-button', n_clicks=0,
                       style=custom_styles['button'],
                       className='custom-button'),
        ], style=custom_styles['buttonContainer']),
        
        # Output Section
        html.Div(id='error-message'),
        html.Div(id='plot-output'),
        
        # Footer
        html.Div([
            html.Hr(style={'margin': '40px 0', 'border': 'none', 'borderTop': '1px solid #e2e8f0'}),
            html.P("Built with Dash & Gnuplot | Agra Barecasco", 
                   style={'textAlign': 'center', 'color': '#94a3b8', 'fontSize': '14px'})
        ])
        
    ], style=custom_styles['container'], className='container')
])

# Global variable to store uploaded data
uploaded_data = None

@app.callback(
    Output('upload-status', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_upload_status(contents, filename):
    global uploaded_data
    
    if contents is not None:
        try:
            # Parse the uploaded file
            content_type, content_string = contents.split(',')
            decoded    = base64.b64decode(content_string)
            filestream = io.StringIO(decoded.decode('utf-8'))

            with open(f'data.txt', 'w', encoding='utf-8') as f:
                f.write(decoded.decode('utf-8'))   

            return html.Div([
                html.Div([
                    html.Span("✅ ", style={'fontSize': '18px'}),
                    html.Span(f"Successfully uploaded: {filename}")
                ], style=custom_styles['successMessage']),
                html.Details([
                    html.Summary("Data Preview (first 5 rows)", 
                               style={'cursor': 'pointer', 'fontWeight': '600', 'color': '#374151', 'margin': '8px 0'}),
                    html.Div([
                    html.Pre('\n'.join(filestream.getvalue().split('\n')[:5]), 
                            style=custom_styles['previewContainer'])
                    ])
                ])
            ])
            
        except Exception as e:
            uploaded_data = None
            return html.Div([
                html.Div([
                    html.Span("❌ ", style={'fontSize': '18px'}),
                    html.Span(f"Error reading file: {str(e)}")
                ], style=custom_styles['errorMessage'])
            ])
    
    return html.Div()

@app.callback(
    [Output('plot-output', 'children'),
     Output('error-message', 'children')],
    Input('submit-button', 'n_clicks'),
    State('gnuplot-command', 'value')
)
def generate_plot(n_clicks, gnuplot_command):
    global uploaded_data
    is_using_csv = True

    if n_clicks == 0:
        return html.Div(), html.Div()
    
    if uploaded_data is None:
        is_using_csv = False
        # Allow execution without CSV for testing purposes
    
    if not gnuplot_command or gnuplot_command.strip() == '':
        return html.Div(), html.Div([
            html.Div([
                html.Span("⚠️ ", style={'fontSize': '18px'}),
                html.Span("Please enter gnuplot commands.")
            ], style=custom_styles['errorMessage'])
        ])
    
    try:
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save CSV data to temporary file
            if is_using_csv:
                csv_path = os.path.join(temp_dir, 'data.csv')
                uploaded_data.to_csv(csv_path, index=False)
            
            # Create gnuplot script file
            script_path = './script.gp'
            output_path = './plot.png'
            
            # Modify the gnuplot command to ensure PNG output
            modified_command = gnuplot_command.replace('"plot.png"', f'"{output_path}"')
            if 'set output' not in modified_command:
                modified_command = f'set terminal png\nset output "{output_path}"\n' + modified_command
            
            with open(script_path, 'w') as f:
                f.write(modified_command)
            
            # Execute gnuplot
            result = subprocess.run(['gnuplot', script_path], 
                                  capture_output=True, text=True, cwd=".")
            
            if result.returncode != 0:
                error_msg = result.stderr if result.stderr else "Unknown gnuplot error"
                return html.Div(), html.Div([
                    html.Div([
                        html.Span("🚫 ", style={'fontSize': '18px'}),
                        html.Span("Gnuplot execution failed:")
                    ], style=custom_styles['errorMessage']),
                    html.Pre(error_msg, style={
                        **custom_styles['previewContainer'],
                        'color': '#dc2626',
                        'backgroundColor': '#fee2e2',
                        'border': '1px solid #fecaca'
                    })
                ])
            
            # Check if output file was created
            if not os.path.exists(output_path):
                return html.Div(), html.Div([
                    html.Div([
                        html.Span("⚠️ ", style={'fontSize': '18px'}),
                        html.Span("Plot file was not generated. Check your gnuplot commands.")
                    ], style=custom_styles['errorMessage'])
                ])
            
            # Read the generated image
            with open(output_path, 'rb') as f:
                image_data = f.read()
            
            # Encode image for display
            encoded_image = base64.b64encode(image_data).decode()
            
            return html.Div([
                html.Div([
                    html.H3(["🎨 ", "Generated Plot"], style=custom_styles['sectionTitle']),
                    html.Div([
                        html.Img(src=f'data:image/png;base64,{encoded_image}',
                                style=custom_styles['plotImage'])
                    ], style=custom_styles['plotContainer']),
                    html.P(f"Plot generated successfully at {datetime.now().strftime('%H:%M:%S')}", 
                           style={'textAlign': 'center', 'color': '#059669', 'fontWeight': '500', 'marginTop': '16px'})
                ], style=custom_styles['card'])
            ]), html.Div()
            
    except FileNotFoundError:
        return html.Div(), html.Div([
            html.Div([
                html.Span("🔧 ", style={'fontSize': '18px'}),
                html.Span("Gnuplot is not installed or not found in PATH.")
            ], style=custom_styles['errorMessage']),
            html.P("Install gnuplot:", style={'fontWeight': '600', 'marginTop': '12px'}),
            html.Ul([
                html.Li("Ubuntu/Debian: sudo apt-get install gnuplot"),
                html.Li("macOS: brew install gnuplot"),
                html.Li("Windows: Download from gnuplot.info")
            ], style={'marginLeft': '20px', 'color': '#374151'})
        ])
    except Exception as e:
        return html.Div(), html.Div([
            html.Div([
                html.Span("❌ ", style={'fontSize': '18px'}),
                html.Span(f"Error generating plot: {str(e)}")
            ], style=custom_styles['errorMessage'])
        ])

if __name__ == '__main__':
    app.run(debug=True)