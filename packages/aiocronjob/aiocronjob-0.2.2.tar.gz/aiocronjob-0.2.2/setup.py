# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aiocronjob']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.5.0,<0.6.0',
 'crontab>=0.22.8,<0.23.0',
 'fastapi>=0.55.1,<0.56.0',
 'pytz>=2020.1,<2021.0',
 'uvicorn>=0.11.5,<0.12.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.1,<2.0.0']}

setup_kwargs = {
    'name': 'aiocronjob',
    'version': '0.2.2',
    'description': 'Schedule async tasks and manage them using a REST API or WEB UI',
    'long_description': '# aiocronjob\n\nSchedule and run `asyncio` coroutines and manage them from a web interface or programmatically using the rest api.\n\n### Requires python >= 3.6\n\n### How to install\n\n```bash\npip3 install aiocronjob\n```\n\n### Usage example\n\n```python\n# examples/simple_tasks.py\n\nimport asyncio\n\nfrom aiocronjob import manager, Job\nfrom aiocronjob import run_app\n\n\nasync def first_task():\n    for i in range(20):\n        print("first task log", i)\n        await asyncio.sleep(1)\n\n\nasync def second_task():\n    for i in range(10):\n        await asyncio.sleep(1.5)\n        print("second task log", i)\n    raise Exception("second task exception")\n\n\nmanager.register(first_task, name="First task", crontab="22 * * * *")\n\nmanager.register(second_task, name="Second task", crontab="23 * * * *")\n\n\nasync def on_job_exception(job: Job, exc: BaseException):\n    print(f"An exception occurred for job {job.name}: {exc}")\n\n\nasync def on_job_cancelled(job: Job):\n    print(f"{job.name} was cancelled...")\n\n\nasync def on_startup():\n    print("The app started.")\n\n\nasync def on_shutdown():\n    print("The app stopped.")\n\n\nmanager.set_on_job_cancelled_callback(on_job_cancelled)\nmanager.set_on_job_exception_callback(on_job_exception)\nmanager.set_on_shutdown_callback(on_shutdown)\nmanager.set_on_startup_callback(on_startup)\n\nif __name__ == "__main__":\n    run_app()\n```\n\nAfter running the app, the [FastAPI](https://fastapi.tiangolo.com) server runs at `localhost:5000`.\n\n#### Web Interface\n\nOpen [localhost:5000](http://localhost:5000) in your browser:\n\n![WEBUIScreenshot](https://raw.githubusercontent.com/devtud/aiocronjob/master/examples/simple_tasks-screenshot.png)\n\n#### Rest API\n\nOpen [localhost:5000/docs](http://localhost:5000/docs) for endpoints docs.\n\n![EndpointsScreenshot](https://raw.githubusercontent.com/devtud/aiocronjob/master/examples/simple_tasks-endpoints-screenshot.png)\n\n**`curl`** example:\n \n```bash\n$ curl http://0.0.0.0:5000/api/jobs\n```\n```json\n[\n  {\n    "name": "First task",\n    "next_run_in": "3481.906931",\n    "last_status": "pending",\n    "enabled": "True",\n    "crontab": "22 * * * *",\n    "created_at": "2020-06-06T10:20:25.118630+00:00",\n    "started_at": null,\n    "stopped_at": null\n  },\n  {\n    "name": "Second task",\n    "next_run_in": "3541.904723",\n    "last_status": "error",\n    "enabled": "True",\n    "crontab": "23 * * * *",\n    "created_at": "2020-06-06T10:20:25.118661+00:00",\n    "started_at": "2020-06-06T10:23:00.000906+00:00",\n    "stopped_at": "2020-06-06T10:23:15.004351+00:00"\n  }\n]\n```\n',
    'author': 'devtud',
    'author_email': 'devtud@gmail.com',
    'maintainer': 'devtud',
    'maintainer_email': 'devtud@gmail.com',
    'url': 'https://github.com/devtud/aiocronjob',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
