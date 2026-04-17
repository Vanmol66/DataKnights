def export_dashboard(fig, name="dashboard"):
    fig.write_html(f"{name}.html")
    fig.write_image(f"{name}.png")
    