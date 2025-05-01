import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)
server = app.server  # Needed for deployment on Render

# === Shared control style ===
control_style = {
    "fontSize": "16px",
    "height": "36px",
    "lineHeight": "36px",
    "padding": "0 8px",
    "borderRadius": "6px",
    "boxSizing": "border-box",
    "minWidth": "80px"
}

# === Figure generation ===
def generate_figure(A, f, phi_deg, t_span):
    omega = 2 * np.pi * f
    phi = np.deg2rad(phi_deg)
    t = np.linspace(0, t_span, 1000)
    z = A * np.exp(1j * omega * t + 1j * phi)
    real_z, imag_z = np.real(z), np.imag(z)

    fig = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.4],
        row_heights=[0.5, 0.5],
        specs=[
            [{"type": "scatter3d", "rowspan": 2}, {"type": "xy"}],
            [None, {"type": "xy"}]
        ],
        horizontal_spacing=0.08,
        vertical_spacing=0.15
    )

    fig.add_trace(go.Scatter3d(
        x=t, y=real_z, z=imag_z,
        mode='lines',
        line=dict(width=6, color='royalblue'),
        name="A·exp(jωt + jφ)"
    ), row=1, col=1)

    z0 = A * np.exp(1j * phi)
    fig.add_trace(go.Scatter3d(
        x=[0, 0],
        y=[0, np.real(z0)],
        z=[0, np.imag(z0)],
        mode='lines+markers',
        line=dict(color='black', width=5),
        marker=dict(size=3),
        name="Phasor A·exp(jφ)"
    ), row=1, col=1)

    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[-A * 1.2, A * 1.2], z=[0, 0],
        mode='lines',
        line=dict(color='gray', width=3, dash='dash'),
        showlegend=False
    ), row=1, col=1)

    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[-A * 1.2, A * 1.2],
        mode='lines',
        line=dict(color='gray', width=3, dash='dash'),
        showlegend=False
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=t, y=real_z,
        mode='lines',
        line=dict(color='red', width=3),
        name='Re{z(t)}'
    ), row=1, col=2)

    fig.add_trace(go.Scatter(
        x=t, y=imag_z,
        mode='lines',
        line=dict(color='green', width=3),
        name='Im{z(t)}'
    ), row=2, col=2)

    fig.update_scenes(
        camera=dict(
            eye=dict(x=1.0, y=-0.7, z=0.6),
            projection=dict(type="orthographic")
        ),
        xaxis_title="Time",
        yaxis_title="Real",
        zaxis_title="Imaginary"
    )

    fig.update_layout(
        height=575,
        autosize=True,
        margin=dict(l=10, r=10, t=10, b=10),
        annotations=[
            dict(
                text=f"f = {f:.1f} Hz<br>A = {A:.2f}<br>φ = {phi_deg:.0f}°",
                x=0.01, y=0.01,
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=14, color="gray"),
                bgcolor="rgba(255,255,255,0.7)",
                borderpad=4
            )
        ]
    )

    fig.update_xaxes(title_text="Time", row=1, col=2)
    fig.update_xaxes(title_text="Time", row=2, col=2)
    fig.update_yaxes(title_text="Real Part", row=1, col=2)
    fig.update_yaxes(title_text="Imaginary Part", row=2, col=2)

    return fig

# === Layout ===
app.layout = html.Div([
    # Title with inline LaTeX
    dcc.Markdown(
        # children=r"**3D representation of complex evolution** $z(t) = A e^{j(\omega t + \varPhi)} = A e^{j\varphi} \cdot e^{j\omega t} = A \cos(\omega t + \varPhi) + j A \sin(\omega t + \varPhi)$",
        children=r"**3D representation of complex evolution** $z(t) = A e^{j(\omega t + \varPhi)} = \underbrace{A e^{j\varphi}}_{\text{phasor}} \cdot e^{j\omega t} = A \cos(\omega t + \varPhi) + j A \sin(\omega t + \varPhi)$",
        mathjax=True,
        style={"fontSize": "20px", "textAlign": "center", "marginBottom": "10px"}
    ),

    # Control bar (centered inline)
    html.Div([
        html.Div([
            dcc.Markdown("Phase \u03C6 (°)", style={"marginRight": "5px", "fontSize": "16px", "whiteSpace": "nowrap"}),
            dcc.Input(id="phi", type="number", value=-30, step=1, style=control_style)
        ], style={"display": "flex", "alignItems": "center", "marginRight": "20px"}),

        html.Div([
            html.Label("Amplitude A", style={"marginRight": "5px", "whiteSpace": "nowrap"}),
            dcc.Dropdown(
                id="amp",
                options=[{"label": str(a), "value": a} for a in [1, 2, 3]],
                value=2,
                style=control_style
            )
        ], style={"display": "flex", "alignItems": "center", "marginRight": "20px"}),

        html.Div([
            html.Label("Frequency f (Hz)", style={"marginRight": "5px", "whiteSpace": "nowrap"}),
            dcc.Dropdown(
                id="freq",
                options=[{"label": str(f), "value": f} for f in [5, 10, 20]],
                value=10,
                style=control_style
            )
        ], style={"display": "flex", "alignItems": "center", "marginRight": "20px"}),

        html.Div([
            html.Label("Duration t (s)", style={"marginRight": "5px", "whiteSpace": "nowrap"}),
            dcc.Dropdown(
                id="time",
                options=[{"label": str(t), "value": t} for t in [0.1, 0.3, 0.5]],
                value=0.3,
                style=control_style
            )
        ], style={"display": "flex", "alignItems": "center"})
    ], style={
        "display": "flex",
        "justifyContent": "center",
        "flexWrap": "wrap",
        "padding": "10px 0 20px 0"
    }),

    dcc.Graph(
        id="complex-plot",
        config={"responsive": True},
        style={"width": "100%", "margin": "0", "padding": "0"}
    )
], style={"fontFamily": "Calibri, Segoe UI, Helvetica, sans-serif"})

# === Callback ===
@app.callback(
    Output("complex-plot", "figure"),
    Input("amp", "value"),
    Input("freq", "value"),
    Input("phi", "value"),
    Input("time", "value")
)
def update_plot(A, f, phi_deg, t):
    return generate_figure(A, f, phi_deg, t)

# === Start server ===
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
    
