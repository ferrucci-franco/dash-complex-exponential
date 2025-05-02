import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output, ctx, no_update
import webbrowser

app = Dash(__name__)
server = app.server

# === Global style and config ===
color_z_3d = "royalblue"
color_z_real = "royalblue"
color_z_imag = "royalblue"
color_z_phasor = "royalblue"
color_dz_dt_3d = "darkorange"
color_dz_dt_real = "darkorange"
color_dz_dt_imag = "darkorange"
color_dz_dt_phasor = "darkorange"
color_int_z_3d = "purple"
color_int_z_real = "purple"
color_int_z_imag = "purple"
color_int_z_phasor = "purple"

thickness_3d = 6
thickness_2d = 3
thickness_phasor = 6

control_style = {
    "fontSize": "16px",
    "fontFamily": "Calibri, sans-serif",
    "height": "36px",
    "lineHeight": "36px",
    "padding": "0 8px",
    "borderRadius": "6px",
    "boxSizing": "border-box",
    "width": "80px",
}

compare_style = control_style.copy()
compare_style["width"] = "250px"

label_style = {"marginRight": "5px", "whiteSpace": "nowrap", "fontFamily": "Calibri, sans-serif"}

box_style = {"display": "flex", "alignItems": "center", "marginRight": "20px"}

phasor_dash_style = "longdashdot"


def generate_figure(A, omega, phi_deg, n_periods, compare):
    t_span = n_periods * (2 * np.pi / omega)
    phi = np.deg2rad(phi_deg)
    t = np.linspace(0, t_span, 1000)

    z = A * np.exp(1j * omega * t + 1j * phi)
    z_deriv = 1j * omega * z
    z_integ = z / (1j * omega)

    fig = make_subplots(
        rows=2,
        cols=2,
        column_widths=[0.6, 0.4],
        row_heights=[0.5, 0.5],
        specs=[[{"type": "scatter3d", "rowspan": 2}, {"type": "xy"}], [None, {"type": "xy"}]],
        horizontal_spacing=0.08,
        vertical_spacing=0.15,
    )

    fig.add_trace(
        go.Scatter3d(
            x=t,
            y=np.real(z),
            z=np.imag(z),
            mode="lines",
            line=dict(width=thickness_3d, color=color_z_3d),
            name="z(t)",
        ),
        row=1,
        col=1,
    )

    z0 = A * np.exp(1j * phi)
    fig.add_trace(
        go.Scatter3d(
            x=[0, 0],
            y=[0, np.real(z0)],
            z=[0, np.imag(z0)],
            mode="lines+markers",
            line=dict(color=color_z_phasor, width=thickness_phasor, dash=phasor_dash_style),
            marker=dict(size=3),
            name="Phasor z(t)",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=t,
            y=np.real(z),
            mode="lines",
            line=dict(color=color_z_real, width=thickness_2d),
            name="Re{z(t)}",
        ),
        row=1,
        col=2,
    )
    fig.add_trace(
        go.Scatter(
            x=t,
            y=np.imag(z),
            mode="lines",
            line=dict(color=color_z_imag, width=thickness_2d),
            name="Im{z(t)}",
        ),
        row=2,
        col=2,
    )

    if compare in ["dz/dt", "all"]:
        fig.add_trace(
            go.Scatter3d(
                x=t,
                y=np.real(z_deriv),
                z=np.imag(z_deriv),
                mode="lines",
                line=dict(width=thickness_3d, color=color_dz_dt_3d),
                name="dz/dt",
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter3d(
                x=[0, 0],
                y=[0, np.real(z_deriv[0])],
                z=[0, np.imag(z_deriv[0])],
                mode="lines+markers",
                line=dict(color=color_dz_dt_phasor, width=thickness_phasor, dash=phasor_dash_style),
                marker=dict(size=3),
                name="Phasor dz/dt",
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=t,
                y=np.real(z_deriv),
                mode="lines",
                line=dict(color=color_dz_dt_real, width=thickness_2d),
                name="Re{dz/dt}",
            ),
            row=1,
            col=2,
        )
        fig.add_trace(
            go.Scatter(
                x=t,
                y=np.imag(z_deriv),
                mode="lines",
                line=dict(color=color_dz_dt_imag, width=thickness_2d),
                name="Im{dz/dt}",
            ),
            row=2,
            col=2,
        )

    if compare in ["int(z)", "all"]:
        fig.add_trace(
            go.Scatter3d(
                x=t,
                y=np.real(z_integ),
                z=np.imag(z_integ),
                mode="lines",
                line=dict(width=thickness_3d, color=color_int_z_3d),
                name="∫z(t)",
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter3d(
                x=[0, 0],
                y=[0, np.real(z_integ[0])],
                z=[0, np.imag(z_integ[0])],
                mode="lines+markers",
                line=dict(color=color_int_z_phasor, width=thickness_phasor, dash=phasor_dash_style),
                marker=dict(size=3),
                name="Phasor ∫z(t)",
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=t,
                y=np.real(z_integ),
                mode="lines",
                line=dict(color=color_int_z_real, width=thickness_2d),
                name="Re{∫z(t)}",
            ),
            row=1,
            col=2,
        )
        fig.add_trace(
            go.Scatter(
                x=t,
                y=np.imag(z_integ),
                mode="lines",
                line=dict(color=color_int_z_imag, width=thickness_2d),
                name="Im{∫z(t)}",
            ),
            row=2,
            col=2,
        )

    fig.add_trace(
        go.Scatter3d(
            x=[0, 0],
            y=[-A * 1.2, A * 1.2],
            z=[0, 0],
            mode="lines",
            line=dict(color="gray", width=3),
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter3d(
            x=[0, 0],
            y=[0, 0],
            z=[-A * 1.2, A * 1.2],
            mode="lines",
            line=dict(color="gray", width=3),
            showlegend=False,
        ),
        row=1,
        col=1,
    )

    fig.update_scenes(
        camera=dict(eye=dict(x=1.0, y=-0.7, z=0.6), projection=dict(type="orthographic")),
        xaxis_title="Time",
        yaxis_title="Real",
        zaxis_title="Imaginary",
    )
    fig.update_layout(height=570, autosize=True, margin=dict(l=10, r=10, t=10, b=10))
    fig.update_xaxes(title_text="Time", row=1, col=2)
    fig.update_xaxes(title_text="Time", row=2, col=2)
    fig.update_yaxes(title_text="Real Part", row=1, col=2)
    fig.update_yaxes(title_text="Imaginary Part", row=2, col=2)
    return fig


# === Layout ===
popup_latex = r"""
**Differentiating and integrating complex exponential**

The rules for differentiating and integrating eᶻ with complex z = σ + jω are the same as for real exponentials.

$$
\frac{d}{dt} \left( e^{z(t)} \right) = z'(t) \cdot e^{z(t)} \quad \text{(as in the real case)}
$$

$$
\frac{d}{dt} \left( e^{(\sigma + j\omega)t} \right) 
= (\sigma + j\omega) e^{(\sigma + j\omega)t} 
= (\sigma + j\omega) \cdot e^{\sigma t} \cdot e^{j\omega t}
$$

---

$\mathbf{Evolution}\text{ }\mathbf{of}\text{ }\frac{dz}{dt}$

$$
\frac{dz}{dt} 
= j \omega A e^{j(\omega t + \varphi)} 
= \underbrace{A e^{j\varphi}}_{\text{phasor of } z(t)} \cdot \omega e^{j90^\circ} \cdot e^{j\omega t} 
= -\omega A \sin(\omega t + \varphi) + j \omega A \cos(\omega t + \varphi)
$$

$$
\left( A e^{j\varphi} \cdot \omega e^{j90^\circ} \right)
: \text{phasor of } \frac{dz}{dt} = \text{phasor of } z(t) 
\text{ , rotated } 90^\circ \text{ and scaled by } \omega
$$

---

$\mathbf{Evolution}\text{ }\mathbf{of}\text{ }\int{z(t)dt}$


$$
\int z(t)\,dt = \frac{A}{j\omega} e^{j(\omega t + \varphi)} 
= \frac{1}{\omega} e^{-j90^\circ} \cdot \underbrace{A e^{j\varphi}}_{\text{phasor of } z(t)} \cdot e^{j\omega t} 
= \frac{A}{\omega} [\sin(\omega t + \varphi) - j \cos(\omega t + \varphi)]
$$

$$
\left( \frac{1}{\omega} e^{-j90^\circ} \cdot A e^{j\varphi} \right)
: \text{phasor of } \int z(t) = \text{phasor of } z(t) 
\text{ , rotated } -90^\circ \text{ and scaled by } \frac{1}{\omega}
$$
"""


app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Markdown(
                    children=r"""**3D representation of complex function z(t)**  
$$
z(t) = A e^{j(\omega t + \varphi)} = \underbrace{A e^{j\varphi}}_{\text{phasor}} \cdot e^{j\omega t} = A \cos(\omega t + \varphi) + j A \sin(\omega t + \varphi)
$$""",
                    mathjax=True,
                    style={"fontSize": "20px", "textAlign": "center", "marginBottom": "5px"},
                ),
                html.Div(
                    "Click here for more information",
                    id="info-link",
                    style={
                        "textAlign": "center",
                        "cursor": "pointer",
                        "color": "blue",
                        "fontSize": "16px",
                        "marginBottom": "10px",
                    },
                ),
            ]
        ),
        html.Div(
            id="popup",
            children=[
                html.Div(
                    [
                        dcc.Markdown(popup_latex, mathjax=True),
                        html.Button("Close", id="close-popup", style={"marginTop": "10px"}),
                    ],
                    style={
                        "backgroundColor": "#f0f0f0",
                        "padding": "20px",
                        "border": "1px solid gray",
                        "borderRadius": "8px",
                        "width": "600px",
                        "margin": "auto",
                        "textAlign": "left",
                    },
                )
            ],
            style={"display": "none"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Phase φ (°)", style=label_style),
                        dcc.Input(id="phi", type="number", value=-30, step=1, style=control_style),
                    ],
                    style=box_style,
                ),
                html.Div(
                    [
                        html.Label("Amplitude A", style=label_style),
                        dcc.Dropdown(
                            id="amp",
                            options=[{"label": str(a), "value": a} for a in [1, 2, 3]],
                            value=1,
                            style=control_style,
                        ),
                    ],
                    style=box_style,
                ),
                html.Div(
                    [
                        html.Label("ω (rad/s)", style=label_style),
                        dcc.Dropdown(
                            id="omega",
                            options=[{"label": str(w), "value": w} for w in [0.75, 1.0, 1.25]],
                            value=1.0,
                            style=control_style,
                        ),
                    ],
                    style=box_style,
                ),
                html.Div(
                    [
                        html.Label("Duration (periods)", style=label_style),
                        dcc.Dropdown(
                            id="time",
                            options=[{"label": str(p), "value": p} for p in [1, 2, 3]],
                            value=1,
                            style=control_style,
                        ),
                    ],
                    style=box_style,
                ),
                html.Div(
                    [
                        html.Label("Compare with", style=label_style),
                        dcc.Dropdown(
                            id="compare",
                            options=[
                                {"label": "Only z(t)", "value": "none"},
                                {"label": "z(t) and derivative", "value": "dz/dt"},
                                {"label": "z(t) and integral", "value": "int(z)"},
                                {"label": "z(t), deriv. and integr.", "value": "all"},
                            ],
                            value="none",
                            style=compare_style,
                        ),
                    ],
                    style={"display": "flex", "alignItems": "center"},
                ),
            ],
            style={
                "display": "flex",
                "flexWrap": "wrap",
                "justifyContent": "center",
                "paddingBottom": "20px",
            },
        ),
        dcc.Graph(id="complex-plot", config={"responsive": True}, style={"width": "100%"}),
    ]
)


@app.callback(
    Output("complex-plot", "figure"),
    Input("amp", "value"),
    Input("omega", "value"),
    Input("phi", "value"),
    Input("time", "value"),
    Input("compare", "value"),
)
def update_plot(A, omega, phi_deg, n_periods, compare):
    return generate_figure(A, omega, phi_deg, n_periods, compare)


@app.callback(
    Output("popup", "style"),
    Input("info-link", "n_clicks"),
    Input("close-popup", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_popup(n_info, n_close):
    if ctx.triggered_id == "info-link":
        return {"display": "block"}
    elif ctx.triggered_id == "close-popup":
        return {"display": "none"}
    return no_update

# === Start server ===
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
    
