pyinstaller `
  --onefile `
  --name xml-generator `
  --add-data "src\models;src\models" `
  --add-data "src\routes;src\routes" `
  --add-data "src\static;src\static" `
  --add-data "src\database;src\database" `
  src\main.py
