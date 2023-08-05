# pandashape: a simpleish Python package for easy data cleanup and preparation of Pandas dataframes

I made `pandashape` because I've been finding I do a lot of the same repetitive cleanup for simple modeling with scikit-learn.
I've intentionally designed it to make data preparation expressive, concise, and easily repeatable - just put your use of 

## Getting started

Just install with pip!

`pip install pandashape`

## Using pandashape
Create your dataframe however you choose - from a CSV, `.txt.` file, random generation, whatever. Then wrap your frame in a `PandaShaper`. 

```python
# import packages
import numpy as np
import pandas as pd
from pandashape import PandaShaper, Columns
from pandashape.transformers import CategoricalEncoder, NullColumnsDropper

# create your frame
my_df = pd.read_csv('./my_data.csv')

# wrap it in a shaper
shaper = PandaShaper(my_df)
```

From here, you can use PandaShape to inspect and transform your data.

### Data inspection

PandaShape provides an automatic `.describe()` method similar to the one provided by `pandas`, but with more feature richness
and extensibility.

```python
shaper.describe()
```

```
########### PANDASHAPE REPORT ###########

*** General frame info ***
Shape: (1000, 10)
Columns with one or more null values: ['History']
Columns of type "object" (may need label encoding): ['Age' 'Gender' 'OwnHome' 'Married' 'Location' 'History']
These columns are skewed beyond the threshold of 1 +/- 0.4. You may want to scale them somehow.
 - Salary (0.41909498781999727)
 - Catalogs (0.0920540150758884)
 - AmountSpent (1.4692769120373967)

[1000 rows x 8 columns]]
[     Salary  Children  Catalogs  AmountSpent  Salary_scaled  Children_scaled  Catalogs_scaled  AmountSpent_scaled
0     47500         0         6          755      10.768485             -inf         1.791759            6.626718
1     63600         0         6         1318      11.060369             -inf         1.791759            7.183871
2     13500         0        18          296       9.510445             -inf         2.890372            5.690359
3     85600         1        18         2436      11.357441         0.000000         2.890372            7.798113
4     68400         0        12         1304      11.133128             -inf         2.484907            7.173192
..      ...       ...       ...          ...            ...              ...              ...                 ...
995   19400         1        18          384       9.873028         0.000000         2.890372            5.950643
996   40500         1        18         1073      10.609057         0.000000         2.890372            6.978214
997   44800         0        24         1417      10.709963             -inf         3.178054            7.256297
998   79000         2        18          671      11.277203         0.693147         2.890372            6.508769
999   53600         1        24          973      10.889304         0.000000         3.178054            6.880384

[1000 rows x 8 columns]]
```

If you have questions that you often ask about your datasets, you can encapsulate them in classes that inherit PandaShape's `Describer` for reuse. See the wiki for documentation.

### Data transformation

PandaShape's data preparation and cleanup features are where it really shines. It provides an expressive syntax that you can use to describe, order, and even dynamically modify transformations to your data:

```python
# import packages
import numpy as np
import pandas as pd
from pandashape import PandaShaper, Columns
from pandashape.transformers import 
    CategoricalEncoder,
    MassScaler, 
    NullColumnsDropper

# create your frame
my_df = pd.read_csv('./my_data.csv')

# wrap it in a shaper
shaper = PandaShaper(my_df)

# create a pipeline of transform operations (these will happen in order)
# and assign the output to a new (transformed) frame!
transformed_df = shaper.transform(
    {
        # drop columns that have 80% or less null data
        'columns': Columns.All,
        'transformers': [
            NullColumnsDropper(null_values=[np.nan, None, ''], threshold=0.8),
            MassScaler()
        ]
    },
    {
        # CategoricalEncoder one-hot-encodes targeted categorical columns if they
        # have a number of values ≥ the breakpoint or label encodes them normally 
        'columns': ['Education', 'SES'], 
        'transformers': CategoricalEncoder(label_encoding_breakpoint=4)
    }
)

# inspect the new frame to see the fruits of your labors!
transformed_df.head()
```

