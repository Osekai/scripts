def createSql(data: dict, table):
    sqls = []
    for val in data:
        keys = val.keys()
        sql = "insert into " + table + "(" + ",".join(keys) + ") values ("
        values = []
        for key in keys:
            if isinstance(val[key], str):
                values.append('"' + val[key] + '"')
            else:
                values.append(str(val[key]))
        sql+=",".join(values) + ") on duplicate key update "
        duplicateVals = [(key + "=" + values[i]) for i, key in enumerate(keys)]
        sql+=",".join(duplicateVals)
        sqls.append(sql)
    return sqls