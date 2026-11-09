from pathlib import Path
import json
import json5
from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell


# 파이썬 파일과 같은 폴더의 data.js 읽기
folder = Path(__file__).resolve().parent
input_file = folder / "data.js"
output_file = folder / "output.xlsx"

if not input_file.exists():
    raise FileNotFoundError(f"파일을 찾을 수 없습니다: {input_file}")

print(f"읽는 파일: {input_file}")

text = input_file.read_text(encoding="utf-8-sig").strip()

# DATA_STORAGE 변수에 들어 있는 배열만 추출
variable_name = "DATA_STORAGE"
variable_pos = text.find(variable_name)

if variable_pos == -1:
    raise ValueError("DATA_STORAGE 변수를 찾지 못했습니다.")

equals_pos = text.find("=", variable_pos + len(variable_name))
start = text.find("[", equals_pos + 1)
end = text.rfind("]")

if equals_pos == -1 or start == -1 or end < start:
    raise ValueError("DATA_STORAGE 배열의 시작과 끝을 찾지 못했습니다.")

print("데이터 분석 중...")
data = json5.loads(text[start:end + 1])


# 중첩 배열을 펼치되 항목 순서와 중복은 유지
def flatten_records(value):
    if isinstance(value, dict):
        return [value]

    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(flatten_records(item))
        return result

    raise ValueError(
        f"배열 안에 예상하지 못한 값이 있습니다: {value!r}"
    )


records = flatten_records(data)

if not records:
    raise ValueError("변환할 데이터가 없습니다.")

# 모든 항목에서 열 이름 수집
all_columns = list(dict.fromkeys(
    key
    for item in records
    for key in item
))

# 주요 열을 먼저 배치하고 나머지 열도 보존
preferred = ["계급", "직렬", "지역", "부대", "임용예정일"]

columns = [
    key for key in preferred
    if key in all_columns
]

columns += [
    key for key in all_columns
    if key not in columns
]

if len(records) + 1 > 1048576:
    raise ValueError("데이터가 엑셀 시트의 최대 행 수를 초과합니다.")

if len(columns) > 16384:
    raise ValueError("데이터가 엑셀 시트의 최대 열 수를 초과합니다.")

# 엑셀 생성
wb = Workbook(write_only=True)
ws = wb.create_sheet("데이터")


def make_cell(value):
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False)

    if isinstance(value, str):
        if len(value) > 32767:
            raise ValueError(
                "한 셀에 들어갈 문자열이 32,767자를 초과합니다."
            )

        # 문자열은 수식이 아닌 텍스트로 저장
        cell = WriteOnlyCell(ws, value=value)
        cell.data_type = "s"
        return cell

    return value


ws.append([make_cell(key) for key in columns])

print(f"엑셀 작성 중: {len(records):,}개 항목")

for number, item in enumerate(records, start=1):
    ws.append([
        make_cell(item.get(key))
        for key in columns
    ])

    if number % 1000 == 0:
        print(f"  {number:,}개 작성 완료")

try:
    wb.save(output_file)
except PermissionError:
    raise PermissionError(
        "output.xlsx가 엑셀에서 열려 있으면 닫고 다시 실행하세요. "
        "닫혀 있다면 폴더의 쓰기 권한을 확인하세요."
    )

print()
print(f"변환 완료: {len(records):,}개 항목")
print(f"열 개수: {len(columns)}개")
print(f"저장 위치: {output_file}")