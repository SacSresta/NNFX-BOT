import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np  # Import numpy for np.where function

def create_figure_sig(sig):
    # Initialize figure with subplots
    fig_ssl = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05)

    # Candlestick chart
    fig_ssl.add_trace(go.Candlestick(
        x=sig['Time'],
        open=sig['Open'],
        high=sig['High'],
        low=sig['Low'],
        close=sig['Close'],
        name='Candlestick',
        line=dict(width=1),
        opacity=1,
        increasing_fillcolor='#24A06B',
        decreasing_fillcolor="#CC2E3C",
        increasing_line_color='#2EC886',
        decreasing_line_color='#FF3A4C'
    ), row=1, col=1)

    #TP and SL adder
    fig_ssl.add_trace(go.Scatter(

    ))

    # SSLUp, SSLDown, Baseline traces
    fig_ssl.add_trace(go.Scatter(
        x=sig['Time'],
        y=sig['sslUp'],
        name='sslUp',
        mode='lines',
        line=dict(color='green', width=2)
    ), row=1, col=1)

    fig_ssl.add_trace(go.Scatter(
        x=sig['Time'],
        y=sig['sslDown'],
        name='sslDown',
        mode='lines',
        line=dict(color='red', width=2)
    ), row=1, col=1)

    fig_ssl.add_trace(go.Scatter(
        x=sig['Time'],
        y=sig['baseline'],
        name='Baseline',
        mode='lines',
        line=dict(color='yellow', width=2)
    ), row=1, col=1)

    # Buy and Sell signals
    fig_ssl.add_trace(go.Scatter(
        x=sig[sig['FINAL_SIGNAL'] == "BUY"]['Time'],
        y=sig[sig['FINAL_SIGNAL'] == "BUY"]['Open'],
        name='BUY_ARROW',
        mode='markers',
        marker=dict(color='yellow', symbol='triangle-up', size=10)
    ), row=1, col=1)

    fig_ssl.add_trace(go.Scatter(
        x=sig[sig['FINAL_SIGNAL'] == "SELL"]['Time'],
        y=sig[sig['FINAL_SIGNAL'] == "SELL"]['Open'],
        name='SELL_ARROW',
        mode='markers',
        marker=dict(color='red', symbol='triangle-down', size=10)
    ), row=1, col=1)

    # WAE chart
    fig_ssl.add_trace(go.Bar(
        x=sig['Time'],
        y=sig['trendUp'],
        marker_color=np.where(sig['trendUp'] < sig['trendUp'].shift(1), 'lime', 'green'),
        name='UpTrend',
        width=0.04,
        marker_line_color='rgba(0,0,0,0)',
        marker_line_width=0,
    ), row=2, col=1)

    fig_ssl.add_trace(go.Bar(
        x=sig['Time'],
        y=sig['trendDown'],
        marker_color=np.where(sig['trendDown'] < sig['trendDown'].shift(1), 'orange', 'red'),
        name='DownTrend',
        width=0.04,
        marker_line_color='rgba(0,0,0,0)',
        marker_line_width=0,
    ), row=2, col=1)

    fig_ssl.add_trace(go.Scatter(
        x=sig['Time'],
        y=sig['e1'],
        mode='lines',
        name='ExplosionLine',
        line=dict(color='#A0522D', width=2)
    ), row=2, col=1)

    # Update layout for the entire figure
    fig_ssl.update_layout(
        title='Candlestick Chart with WAE',
        xaxis_title='Time',
        yaxis_title='Price',
        height=800,
        width=1200,
        margin=dict(l=50, r=50, b=50, t=100),
        paper_bgcolor="#1e1e1e",
        plot_bgcolor="#1e1e1e",
        font=dict(size=10, color="#e1e1e1"),
        showlegend=True,
        legend=dict(x=0, y=1.1, orientation='h')
    )

    # Show gridlines
    fig_ssl.update_xaxes(
        gridcolor="#1f292f",
        showgrid=True,
        fixedrange=True,
        rangeslider=dict(visible=True)
    )

    fig_ssl.update_yaxes(
        gridcolor="#1f292f",
        showgrid=True
    )

    return fig_ssl


