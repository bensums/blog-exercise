Simple blog written for potato. Uses djappengine: <https://github.com/potatolondon/djappengine>.

Run development server with

    ./serve.sh

View at <http://localhost:8080>.

To deploy, first change application name in `app.yaml` to an app you are a developer for. Then run

    appcfg.py update .
