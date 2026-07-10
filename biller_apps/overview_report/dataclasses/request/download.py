from dataclasses import dataclass
from datetime import datetime
from biller_apps.common.dataclasses.download import GenerateExcelPDF

@dataclass
class OverviewReportDownload(GenerateExcelPDF):
    page_num: int
    limit: int
    start_date: datetime
    end_date: datetime


    def __post_init__(self):
        self.values_list = []
