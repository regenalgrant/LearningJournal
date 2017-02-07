# LearningJournal  

## My WebSite URL  
- https://regenal-learning-journal.herokuapp.com/

## Getting Started

- git clone repo
- $VENV/bin/activate
- cd LearningJournal/learning_journal_basic
- pip install -e .
- pserve development.ini

## Navigating

- path to get to home page --> /
- path to get to detail page --> /journal/{id:\d+}
- path to get to create page --> /journal/new-entry
- path to get to update page --> /journal/{id:\d+}/edit-entry

## Links

- Home button is located on each page, returns to lists view.
- New-entry button is located on each page, returns to create view.
- title are links that take you to the detail page


## Coverage Reports  

### coverage report step1

        ---------- coverage: platform darwin, python 2.7.10-final-0 ----------
        Name                                         Stmts   Miss  Cover   Missing
        --------------------------------------------------------------------------
        learning_journal_basic/__init__.py               9      7    22%   7-13
        learning_journal_basic/models/__init__.py       22      0   100%
        learning_journal_basic/models/meta.py            5      0   100%
        learning_journal_basic/models/mymodel.py         8      0   100%
        learning_journal_basic/routes.py                 5      5     0%   1-6
        learning_journal_basic/scripts/__init__.py       0      0   100%
        learning_journal_basic/views/__init__.py         0      0   100%
        learning_journal_basic/views/default.py         30      6    80%   35, 41, 49, 51-53
        learning_journal_basic/views/notfound.py         4      4     0%   1-7
        --------------------------------------------------------------------------
        TOTAL                                           83     22    73%

        5 passed in 1.43 seconds

        ---------- coverage: platform darwin, python 3.5.2-final-0 -----------
        Name                                         Stmts   Miss  Cover   Missing
        --------------------------------------------------------------------------
        learning_journal_basic/__init__.py               9      7    22%   7-13
        learning_journal_basic/models/__init__.py       22      0   100%
        learning_journal_basic/models/meta.py            5      0   100%
        learning_journal_basic/models/mymodel.py         8      0   100%
        learning_journal_basic/routes.py                 5      5     0%   1-6
        learning_journal_basic/scripts/__init__.py       0      0   100%
        learning_journal_basic/views/__init__.py         0      0   100%
        learning_journal_basic/views/default.py         30      6    80%   35, 41, 49, 51-53
        learning_journal_basic/views/notfound.py         4      4     0%   1-7
        --------------------------------------------------------------------------
        TOTAL                                           83     22    73%

        5 passed in 1.23 seconds

### coverage report step2  

        ---------- coverage: platform darwin, python 2.7.10-final-0 ----------
        Name                                         Stmts   Miss  Cover   Missing
        --------------------------------------------------------------------------
        learning_journal_basic/__init__.py               9      0   100%
        learning_journal_basic/models/__init__.py       22      0   100%
        learning_journal_basic/models/meta.py            5      0   100%
        learning_journal_basic/models/mymodel.py         8      0   100%
        learning_journal_basic/routes.py                 5      0   100%
        learning_journal_basic/scripts/__init__.py       0      0   100%
        learning_journal_basic/scripts/entry.py          1      0   100%
        learning_journal_basic/views/__init__.py         0      0   100%
        learning_journal_basic/views/default.py         30      6    80%   35, 41, 49, 51-53
        learning_journal_basic/views/notfound.py         4      2    50%   6-7
        --------------------------------------------------------------------------
        TOTAL                                           84      8    90%

        9 passed in 1.81 seconds


        ---------- coverage: platform darwin, python 3.5.2-final-0 -----------
        Name                                         Stmts   Miss  Cover   Missing
        --------------------------------------------------------------------------
        learning_journal_basic/__init__.py               9      0   100%
        learning_journal_basic/models/__init__.py       22      0   100%
        learning_journal_basic/models/meta.py            5      0   100%
        learning_journal_basic/models/mymodel.py         8      0   100%
        learning_journal_basic/routes.py                 5      0   100%
        learning_journal_basic/scripts/__init__.py       0      0   100%
        learning_journal_basic/scripts/entry.py          1      0   100%
        learning_journal_basic/views/__init__.py         0      0   100%
        learning_journal_basic/views/default.py         30      6    80%   35, 41, 49, 51-53
        learning_journal_basic/views/notfound.py         4      2    50%   6-7
        --------------------------------------------------------------------------
        TOTAL                                           84      8    90%

        9 passed in 2.29 seconds



