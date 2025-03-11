from sumservice import sumservice
import clam.clamservice
application = clam.clamservice.run_wsgi(sumservice)