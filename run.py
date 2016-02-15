# Launch dev server
from app import app as application

application.run(host='0.0.0.0', port=8080, debug=True)
