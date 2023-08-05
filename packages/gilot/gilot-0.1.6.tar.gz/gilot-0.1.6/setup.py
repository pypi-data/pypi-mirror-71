# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gilot']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.3,<4.0.0',
 'argparse>=1.4.0,<2.0.0',
 'datetime>=4.3,<5.0',
 'matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.5,<2.0.0',
 'pandas>=1.0.4,<2.0.0',
 'seaborn>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['gilot = gilot.app:main']}

setup_kwargs = {
    'name': 'gilot',
    'version': '0.1.6',
    'description': 'a git log visual analyzer',
    'long_description': '# gilot\n![image](./sample/react.png)\n"gilot" is a tool to analyze and visualize git logs.\n\nOne of the most reliable records of a software project\'s activity is the history of the version control system. This information is then used to create graphs to visualize the state of the software development team in a mechanical way.\n\n"gilot"  creates four graphs.\n\n- The first graph shows the bias in the amount of code changes for a given time slot as a Gini coefficient and a Lorentz curve. The closer the Gini coefficient is to 1, the more unequal it is, and the closer it is to 0, the more perfect equality it is an indicator of economics. It tends to go down when a project has stable agility, and the more volatile and planaristic the project, the closer it is to 1.\n\n- The second graph shows a histogram of the bias in the amount of code changes in a given time slot.\n\n- The third graph shows the change in the amount of code changes per time slot. It is displayed in green when the total amount of codes is increasing and in red when the total amount of codes is decreasing.\n\n- The fourth graph shows the number of authors who committed per given time slot. The effective team size is estimated.\n\n\n\n## Installation\n\njust:\n\n    pip install gilot\nor \n\n    pip install git+https://github.com/hirokidaichi/gilot\n\n## Usage\n\n### simple way (1 liner using pipe)\n    gilot log REPO_DIR | gilot plot\n\n### 2-phase way\n\n    gilot log REPO_DIR > repo.csv\n    gilot plot -i repo.csv -o graph.png\n\n## Command \n``gilot`` has 3 commands, ``log`` and ``plot`` and ``info``\n+  ``log`` command generates a csv from the repository information\n\n+  ``plot``  command generates a graph image (or matplotlib window) from that csv.\n\n+ ``info``  command, like the plot command, takes a csv file as input and outputs only JSON format statistical information.\n\n### gilot log (generate csv)\nThe simplest way to use the ``gilot log`` command is to specify the repository directory as follows. This means saving the output as a CSV file.\n\n    gilot log REPO > REPO.csv\n    gilot log REPO -o REPO.csv\n\nThe default period is six months, but you can specify the time.\n\n    gilot log REPO --since 2020-01-20 -o REPO.csv\n    gilot log REPO --month 18 -o REPO.csv\n\nBy specifying a period of time, such as when you want to see the stability of the service after the launch, you can eliminate the impact of commits during the initial release.\n\n    gilot log REPO --branch develop -o REPO.csv\n\nYou can use the branch option to see what the development branch looks like, or to see the results for each branch. By default, ``origin/HEAD`` is specified. This is because we want to see how well we can develop in a trunk-based way.\n\nAll options are here\n\n    usage: gilot log [-h] [-b BRANCH] [-o OUTPUT] [--since SINCE] [--month MONTH]\n                    repo\n\n    positional arguments:\n    repo                  REPO must be a root dir of git repository\n\n    optional arguments:\n    -h, --help            show this help message and exit\n    -b BRANCH, --branch BRANCH\n                            target branch name. default \'origin/HEAD\'\n    -o OUTPUT, --output OUTPUT\n    --since SINCE         SINCE must be ISO format like 2020-01-01.\n    --until UNTIL         UNTIL must be ISO format like 2020-06-01.\n    --month MONTH         MONTH is how many months of log data to output. default is 6\n\n\n### gilot plot (generate graph)\n\nThe simplest way to use the ``gilot plot`` command is to take the CSV file output from the gilot log command as input and specify the name of the file you want to save as output, as shown below.\n\n\n    gilot plot -i TARGET.csv -o TARGET_REPORT.png\n    gilot plot --input TARGET.csv -o TARGET_REPORT.png\n\nAlso, since the input from the standard input is also interpreted as a CSV, it can be connected to a pipe as shown below.\n\n\n    cat target.csv | gilot plot \n    gilot repo . | gilot plot\n\nFor example, if one team is working in a *multi-repository* services, you may want to know the activity of multiple repositories as a whole, instead of focusing on one repository. In this case, you can combine multiple inputs into a graph as follows.\n\n\n    gilot log repo-a > repo-a.csv\n    gilot log repo-b > repo-b.csv\n    gilot plot -i repo*.csv\n\nAll options are here:\n\n    usage: gilot plot [-h] [-i [INPUT [INPUT ...]]] [-t TIMESLOT] [-o OUTPUT]\n                    [-n NAME]\n\n    optional arguments:\n    -h, --help            show this help message and exit\n    -i [INPUT [INPUT ...]], --input [INPUT [INPUT ...]]\n    -t TIMESLOT, --timeslot TIMESLOT\n                            resample period like 2W or 7D or 1M\n    -o OUTPUT, --output OUTPUT\n                            OUTPUT FILE\n    -n NAME, --name NAME  name\n\n### gilot info (dump statistical infomation)\n\n``info``  command, like the plot command, takes a csv file as input and outputs only JSON format statistical information.\n\n\n    # gilot info -i sample/react.csv\n    {\n        "gini": 0.42222013847205725,\n        "output": {\n            "lines": 242999,\n            "added": 70765,\n            "refactor": 0.7087848098140321\n        },\n        "since": "2019-12-03T10:53:08.000000000",\n        "until": "2020-05-30T06:34:43.000000000",\n        "timeslot": "2 Weeks",\n        "insertions": {\n            "mean": 11205.857142857143,\n            "std": 10565.324647217372,\n            "min": 781.0,\n            "25%": 3788.75,\n            "50%": 8544.0,\n            "75%": 16761.25,\n            "max": 39681.0\n        },\n        "deletions": {\n            "mean": 6151.214285714285,\n            "std": 4437.0289466743825,\n            "min": 327.0,\n            "25%": 3397.0,\n            "50%": 5076.0,\n            "75%": 9333.75,\n            "max": 13477.0\n        },\n        "lines": {\n            "mean": 17357.071428571428,\n            "std": 14236.531424279776,\n            "min": 1108.0,\n            "25%": 7383.25,\n            "50%": 12860.0,\n            "75%": 26531.75,\n            "max": 52914.0\n        },\n        "files": {\n            "mean": 377.7857142857143,\n            "std": 271.95196933718574,\n            "min": 70.0,\n            "25%": 155.75,\n            "50%": 402.0,\n            "75%": 450.0,\n            "max": 1062.0\n        },\n        "authors": {\n            "mean": 13.357142857142858,\n            "std": 4.70036238958302,\n            "min": 4.0,\n            "25%": 10.0,\n            "50%": 15.0,\n            "75%": 16.0,\n            "max": 21.0\n        },\n        "addedlines": {\n            "mean": 5054.642857142857,\n            "std": 7742.596112089604,\n            "min": -1210.0,\n            "25%": 266.5,\n            "50%": 2062.5,\n            "75%": 5770.75,\n            "max": 26448.0\n        }\n    }\nIntegration with ``jq`` command makes it easy to get only the information you need.\n\n### When only the Gini coefficient is required\n    # gilot info -i sample/react.csv | jq .gini\n    > 0.42222013847205725\n\n### If you want to find the total number of lines in all commits in a period\n\n    # gilot info -i sample/react.csv | jq .output.lines\n\n\n## Example Output\n\n### facebook/react\n![image](./sample/react.png)\n\n### tensorflow/tensorflow\n![image](./sample/tensorflow.png)\n\n### pytorch/pytorch\n![image](./sample/pytorch.png)\n\n### optuna/optuna\n![image](./sample/optuna.png)\n\n### microsoft/TypeScript\n![image](./sample/TypeScript.png)\n\n## As a package in python\n\n ',
    'author': 'hirokidaichi',
    'author_email': 'hirokidaichi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hirokidaichi/gilot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
