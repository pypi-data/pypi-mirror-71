'''
    The hub of datup libraries
'''

from datup.io.api import (
    download_csv,
    download_csvm,
    upload_csv,
    profiling_report,
    upload_model,
    upload_log,
    download_excel
)
from datup.preparation.api import (
    col_cast,
    featureselection_correlation,
    Error,
    CorrelationError,
    remove_chars_metadata,
    to_lowercase_metadata,
    profile_dataset,
    replace_categorical_na,
    replace_numeric_na 
)

from datup.timeseries.api import (
    compute_mae,
    compute_maep,
    compute_mape,
    compute_mase,
    compute_rmse
)

from datup.utils.api import (
    filter_by_list, 
    antifilter_by_list,
    reorder_columns,
    check_data_format,
    count_na
)

from datup.core.api import (Datup)