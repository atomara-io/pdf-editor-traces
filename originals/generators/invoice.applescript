-- usage: osascript invoice.applescript /abs/path/invoice-00-genuine.pdf
on run argv
set rowsData to {{"Bright Line Studio", ""}, {"Web design & illustration · fictional business", ""}, {"", ""}, {"INVOICE #2026-118", ""}, {"Issued: November 2, 2026", "Due: November 16, 2026"}, {"Bill to: Harbor & Pine Coffee Co.", ""}, {"", ""}, {"Description", "Amount (USD)"}, {"Logo redesign, 3 concepts", "1,200.00"}, {"Menu board illustrations (6)", "840.00"}, {"Website banner set", "300.00"}, {"TOTAL DUE", "2,340.00"}, {"", ""}, {"Payment: bank transfer within 14 days.", ""}, {"SAMPLE - NOT A VALID DOCUMENT. Generated for a research experiment.", ""}}
tell application "Numbers"
  set d to make new document
  tell table 1 of sheet 1 of d
    set name to "Invoice"
    set row count to 15
    set column count to 2
    set header row count to 0
    set header column count to 0
    set width of column 1 to 300
    set width of column 2 to 150
    repeat with i from 1 to 15
      set value of cell 1 of row i to item 1 of item i of rowsData
      set value of cell 2 of row i to item 2 of item i of rowsData
    end repeat
    set format of column 2 to text
    set alignment of column 2 to right
    set font name of cell 1 of row 1 to "HelveticaNeue-Bold"
    set font size of cell 1 of row 1 to 18
    set font name of row 4 to "HelveticaNeue-Bold"
    set font name of row 8 to "HelveticaNeue-Bold"
    set font name of row 12 to "HelveticaNeue-Bold"
    repeat with i in {9, 10, 11, 12}
      set value of cell 2 of row i to item 2 of item i of rowsData
    end repeat
  end tell
  export d to POSIX file (item 1 of argv) as PDF
  close d saving no
end tell
end run
