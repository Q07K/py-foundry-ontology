import pandas as pd


def parse_excel_file(file_path: str, sheet_name: str) -> pd.DataFrame:
    """Excel 파일을 읽어 DataFrame으로 반환

    Parameters
    ----------
    file_path : str
        Excel 파일 경로
    sheet_name : str
        읽어올 시트 이름

    Returns
    -------
    pd.DataFrame
        Excel 파일의 데이터
    """
    return pd.read_excel(io=file_path, sheet_name=sheet_name)
