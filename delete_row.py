import sqlite3

con = sqlite3.connect("opportunities.db")

count = con.execute("SELECT COUNT(*) FROM opportunities").fetchone()[0]
print("Rows before delete:", count)

con.execute("DELETE FROM opportunities")
con.execute("DELETE FROM sqlite_sequence WHERE name = 'opportunities'")  # reset id numbering
con.commit()
con.close()
print("All rows deleted.")
