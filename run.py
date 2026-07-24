"""
KleanFlow Laundry Management System Entry Point.
Run this script to start the development server.
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
