import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.utils import parse_time


class PredictionDataset(APIObject):

    """ A dataset uploaded to make predictions

    Typically created via `project.upload_dataset`

    Attributes
    ----------
    id : str
        the id of the dataset
    project_id : str
        the id of the project the dataset belongs to
    created : str
        the time the dataset was created
    name : str
        the name of the dataset
    num_rows : int
        the number of rows in the dataset
    num_columns : int
        the number of columns in the dataset
    forecast_point : datetime.datetime or None
        For time series projects only. This is the default point relative to which predictions will
        be generated, based on the forecast window of the project.  See the time series
        :ref:`predictions documentation <time_series_predict>` for more information.
    predictions_start_date : datetime.datetime or None, optional
        For time series projects only. The start date for bulk predictions. Note that this
        parameter is for generating historical predictions using the training data. This parameter
        should be provided in conjunction with ``predictions_end_date``. Can't be provided with the
        ``forecast_point`` parameter.
    predictions_end_date : datetime.datetime or None, optional
        For time series projects only. The end date for bulk predictions, exclusive. Note that this
        parameter is for generating historical predictions using the training data. This parameter
        should be provided in conjunction with ``predictions_start_date``. Can't be provided with
        the ``forecast_point`` parameter.
    relax_known_in_advance_features_check : bool, optional
        (New in version v2.15) For time series projects only. If True, missing values in the
        known in advance features are allowed in the forecast window at the prediction time.
        If omitted or False, missing values are not allowed.
    data_quality_warnings : dict, optional
        (New in version v2.15) A dictionary that contains available warnings about potential
        problems in this prediction dataset. Empty if no warnings.
    forecast_point_range : list[datetime.datetime] or None, optional
        (New in version v2.20) For time series projects only. Specifies the range of dates available
        for use as a forecast point.
    data_start_date : datetime.datetime or None, optional
        (New in version v2.20) For time series projects only. The minimum primary date of this
        prediction dataset.
    data_end_date : datetime.datetime or None, optional
        (New in version v2.20) For time series projects only. The maximum primary date of this
        prediction dataset.
    max_forecast_date : datetime.datetime or None, optional
        (New in version v2.20) For time series projects only. The maximum forecast date of this
        prediction dataset.
    """

    _path_template = 'projects/{}/predictionDatasets/{}/'

    _converter = t.Dict({
        t.Key('id'): t.String(),
        t.Key('project_id'): t.String(),
        t.Key('created'): t.String(),
        t.Key('name'): t.String(),
        t.Key('num_rows'): t.Int(),
        t.Key('num_columns'): t.Int(),
        t.Key('forecast_point', optional=True): parse_time,
        t.Key('predictions_start_date', optional=True): parse_time,
        t.Key('predictions_end_date', optional=True): parse_time,
        t.Key('relax_known_in_advance_features_check', optional=True): t.Bool(),
        t.Key('data_quality_warnings'): t.Dict({
            t.Key('has_kia_missing_values_in_forecast_window'): t.Bool()
        }).allow_extra('*'),
        t.Key('forecast_point_range', optional=True): t.List(parse_time),
        t.Key('data_start_date', optional=True): parse_time,
        t.Key('data_end_date', optional=True): parse_time,
        t.Key('max_forecast_date', optional=True): parse_time,
    }).allow_extra('*')

    def __init__(
            self, project_id, id, name, created, num_rows, num_columns, forecast_point=None,
            predictions_start_date=None, predictions_end_date=None,
            relax_known_in_advance_features_check=None, data_quality_warnings=None,
            forecast_point_range=None, data_start_date=None, data_end_date=None,
            max_forecast_date=None
    ):
        self.project_id = project_id
        self.id = id
        self.name = name
        self.created = created
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.forecast_point = forecast_point
        self.predictions_start_date = predictions_start_date
        self.predictions_end_date = predictions_end_date
        self.relax_known_in_advance_features_check = relax_known_in_advance_features_check
        self.data_quality_warnings = data_quality_warnings
        self.forecast_point_range = forecast_point_range
        self.data_start_date = data_start_date
        self.data_end_date = data_end_date
        self.max_forecast_date = max_forecast_date
        self._path = self._path_template.format(project_id, id)

    def __repr__(self):
        return 'PredictionDataset({!r})'.format(self.name)

    @classmethod
    def get(cls, project_id, dataset_id):
        """
        Retrieve information about a dataset uploaded for predictions

        Parameters
        ----------
        project_id:
            the id of the project to query
        dataset_id:
            the id of the dataset to retrieve

        Returns
        -------
        dataset: PredictionDataset
            A dataset uploaded to make predictions
        """
        path = cls._path_template.format(project_id, dataset_id)
        return cls.from_location(path)

    def delete(self):
        """ Delete a dataset uploaded for predictions

        Will also delete predictions made using this dataset and cancel any predict jobs using
        this dataset.
        """
        self._client.delete(self._path)
