def attendant(wks, date, username):
    cell = wks.find(date)
    row = wks.row_values(cell.row)
    names = row[4:]
    names.append(username)
    row_number = 5
    n = ""
    for name in names:
        n += "," + name

    wks.update_cell(cell.row, row_number, n)