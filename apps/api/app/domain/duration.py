from datetime import date

def parse_month(value:str,evaluation_as_of:date)->int:
    if value.lower()=="present": return evaluation_as_of.year*12+evaluation_as_of.month
    parts=value.split("-")
    if len(parts)!=2: raise ValueError("Year-only or ambiguous dates cannot establish months")
    year,month=map(int,parts)
    if not 1<=month<=12: raise ValueError("Invalid month")
    return year*12+month-1

def merged_months(intervals:list[tuple[str,str]],evaluation_as_of:date)->int:
    normalized=sorted((parse_month(a,evaluation_as_of),parse_month(b,evaluation_as_of)) for a,b in intervals)
    if any(b<=a for a,b in normalized): raise ValueError("Interval end must follow start")
    merged:list[list[int]]=[]
    for start,end in normalized:
        if merged and start<=merged[-1][1]: merged[-1][1]=max(end,merged[-1][1])
        else: merged.append([start,end])
    return sum(end-start for start,end in merged)
