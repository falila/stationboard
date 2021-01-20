from app import create_app
from app.model import Trip, Station, Bus
app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'Trip': Trip, 'Station': Station, 'Bus': Bus}
