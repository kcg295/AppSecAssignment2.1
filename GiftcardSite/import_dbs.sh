sqlite3 db.sqlite3 << END_COMMANDS
.mode csv
.import products.csv LegacySite_product
.import users.csv LegacySite_user
END_COMMANDS
