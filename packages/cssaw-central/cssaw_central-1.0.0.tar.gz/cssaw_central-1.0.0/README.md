# CSSAW_Central

## Installation
``` Bash
pip install CSSAW-Central
```

## Usage

Session object acts as a wrapper for sqlalchemy connection. The connection is created and stored in the Session object at initialization, and any results can be taken from the self.conn object or, if using execute_sql(), can be taken from the returned results python list.

### Example:
```Python
from cssaw_central import Session

sess = Session('test','test', 'localhost', db='Test')

sess.create_table('test_table', ['column1', 'column2', 'column3'], \ 
                    ['int', 'int', 'int'], ['True', 'False', 'False'])

sess.insert('test_table', ['column1', 'column2', 'column3'], [0, 1, 2])
print(sess.execute_SQL('./queries/test.sql'))
```

The above script will create a connection to the Test database at localhost:3306 (assuming that it exists), insert the given values into their appropriate columns in test_table, and then execute test.sql from the queries file, which in this case selects the first value in column1 that has just been added.

# To Do:
- Stripped implementation of SELECT
- Stripped implementation of UPDATE
- Stripped implementation of JOIN

# License
[MPL-2.0](https://opensource.org/licenses/MPL-2.0)